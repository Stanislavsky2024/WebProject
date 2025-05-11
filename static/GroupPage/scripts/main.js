const removeButtons = document.getElementsByClassName('remove')
const solveButtons = document.getElementsByClassName('solve')


for (let button of removeButtons) {
    button.addEventListener('click', removeWork)
}


function removeWork(event) {
    const id = event.target.parentNode.parentNode.id
    fetch('/group_service/remove_group_work', {
        method: 'POST',
        body: JSON.stringify({
            'work_id': id, 
            'group_id': document.querySelector('.content-section').id.split('-')[0]
        })
    })
    .then(response => {
        if (response.ok) {
            tableChanger(id)
        }
    })
    .catch(console.log.bind(console))
}


function tableChanger(id) {
    const tableBody = document.querySelector('.group-tasks').tBodies[0]
    const row = document.getElementById(id)
    const removedNumber = Number(row.cells[0].innerHTML)
    tableBody.removeChild(row)
    for (let i = 0; i < tableBody.rows.length; i++) {
        if (Number(tableBody.rows[i].cells[0].innerHTML) > removedNumber) {
            tableBody.rows[i].cells[0].innerHTML = String(Number(tableBody.rows[i].cells[0].innerHTML) - 1)
        }
    }
}

