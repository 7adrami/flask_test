from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gestion_presence'
app.secret_key = 'your_secret_key'  # Used for session management

mysql = MySQL(app)

@app.route('/')
def index():

    cur = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM absences"
    cur.execute(query)
    total_absences = cur.fetchone()[0]
    cur.close()
    return render_template('index.html', total_absences=total_absences)


@app.route('/ajoute_absence', methods=['GET', 'POST'])
def ajoute_absence():
    if request.method == 'POST':
        matricule = request.form['matricule']
        mail_prof = request.form['mail_prof']
        date_absence = request.form['date_absence']
        id_sn = request.form['id_sn']
        id_semestre = request.form['id_semestre']
        statut_just = request.form['statut_just']

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO absences (matricule, mail_prof, date_absence, id_sn, id_semestre, statut_just)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (matricule, mail_prof, date_absence, id_sn, id_semestre, statut_just))
        mysql.connection.commit()
        cur.close()

        flash("Absence ajoutée avec succès", "success")
        return redirect(url_for('view_absences'))

    return render_template('ajoute_absence.html')

@app.route('/view_absences')
def view_absences():
    cur = mysql.connection.cursor()
    query = """
    SELECT id_absence, matricule, date_absence, mail_prof, id_semestre, id_sn, statut_just
    FROM absences
    """
    cur.execute(query)
    absences = cur.fetchall()
    cur.close()
    return render_template('view_absences.html', absences=absences)

def insert_user(mail_prof, plain_password):
    hashed_password = generate_password_hash(plain_password)
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO enseignants (mail_prof, mot_de_passe) VALUES (%s, %s)", (mail_prof, hashed_password))
    mysql.connection.commit()
    cur.close()

if __name__ == '__main__':
    app.run(debug=True)
