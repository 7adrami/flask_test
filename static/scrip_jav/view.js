document.getElementById('absenceForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const data = {
        matricule: document.getElementById('matricule').value,
        date_absence: document.getElementById('date_absence').value,
        id_sn: document.getElementById('id_sn').value,
        statut_just: document.getElementById('statut_just').value
    };

    const response = await fetch('/add_absence', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    alert(result.message);
    if (result.status === 'success') {
        document.getElementById('absenceForm').reset();
    }
});
