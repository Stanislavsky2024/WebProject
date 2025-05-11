export function addTask(event) {
    let button
    if (event.target) {
        button = event.target
    } else {
        button = event
    }
    const table = document.getElementById('work')
    const tableBody = table.tBodies[0]
    const row = document.createElement('tr')

    const data = [String(tableBody.rows.length + 1)]
    if (button.className === 'add') {
        data.push('Выбрано')
    } else {
        data.push('Создано')
    }
    data.push(createButton())
    for (let i = 0; i < 3; i++) {
        const cell = document.createElement('td')
        if (i === 2) {
            cell.append(data[i])
        } else {
            const cellPart = document.createTextNode(data[i])
            cell.append(cellPart)
        }
        row.append(cell)
    }
    row.task = button.task
    tableBody.append(row)
}


function createButton() {
    const button = document.createElement('button')
    button.innerHTML = 'Удалить'
    button.addEventListener('click', deleteTask)
    return button
}


function deleteTask(event) {
    const table = document.getElementById('work')
    const tableBody = table.tBodies[0]
    const row = event.target.parentNode.parentNode
    const removedNumber = Number(row.cells[0].innerHTML)
    tableBody.removeChild(row)
    for (let i = 0; i < tableBody.rows.length; i++) {
        if (Number(tableBody.rows[i].cells[0].innerHTML) > removedNumber) {
            tableBody.rows[i].cells[0].innerHTML = String(Number(tableBody.rows[i].cells[0].innerHTML) - 1)
        }
    }
}


