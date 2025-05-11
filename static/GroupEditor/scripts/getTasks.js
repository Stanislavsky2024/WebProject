import { getStatement } from "./showStatement.js"
import { addTask } from "./taskManager.js"


export function getTask(selectors) {
    fetch('/task_service/get_tasks', {
        method: 'POST',
        body: JSON.stringify(
            {'options': 
                [selectors[0][selectors[0].selectedIndex].text.split(' ')[1], 
                selectors[1][selectors[1].selectedIndex].text,
                selectors[2][selectors[2].selectedIndex].text
            ]})
    })
    .then(response => {
        if (response.ok) {
            return response.json()
        }
    })
    .then(data => {
        changeTable(data['tasks'])
    })
    .catch(console.log.bind(console))
}


function changeTable(tasks) {
    const table = document.getElementById('task')
    let tableBody = table.tBodies[0]
    var newTableBody = document.createElement('tbody')
    table.replaceChild(newTableBody, tableBody)
    tableBody = table.tBodies[0]

    for (let i = 0; i < tasks.length; i++) {
        const row = document.createElement('tr')
        const task = [
            String(i + 1), 
            tasks[i]['difficulty'], 
            tasks[i]['type'],
            createButtons(tasks[i]),
            tasks[i]['id']
        ]
        for (let j = 0; j < 4; j++) {
            const cell = document.createElement('td')
            if (j === 3) {
                const cellPart = task[j]
                cell.append(cellPart[0]), cell.append(cellPart[1])
            } else {
                const cellPart = document.createTextNode(task[j])
                cell.append(cellPart)
            }
            row.append(cell)
        }
        row.id = task[4] + '.' + task[0]
        tableBody.append(row)
    }
}


function createButtons(task) {
    const buttonAdd = document.createElement('button')
    buttonAdd.className = 'add'
    buttonAdd.innerHTML = 'Добавить'
    buttonAdd.task = task
    buttonAdd.addEventListener('click', addTask)
    const buttonState = document.createElement('button')
    buttonState.className = 'statement'
    buttonState.innerHTML = 'Условие'
    buttonState.addEventListener('click', getStatement)
    return [buttonAdd, buttonState]
}



