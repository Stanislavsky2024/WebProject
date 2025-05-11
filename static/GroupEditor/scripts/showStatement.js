const dialog = document.getElementById('task-statement-dialog')


export function getStatement(event) {
    const id = event.target.parentNode.parentNode.id.split('.')[0]
    fetch('/task_service/get_task_by_id', {
        method: 'POST',
        body: id
    })
    .then(response => {
        if (response.ok) {
            return response.json()
        }
    })
    .then(data => {
        showStatement(data, event.target.parentNode.parentNode.id.split('.')[1])
    })
    .catch(console.log.bind(console))
}

function showStatement(data, i) {
    dialog.showModal()
    console.log(data)
    document.getElementById('header-text').innerHTML = `Условие задания ${data['number']}.${i}`
    document.getElementById('type-text').innerHTML = data['type']
    document.getElementById('difficulty-text').innerHTML = data['difficulty']
    document.getElementById('statement-text1').innerHTML = data['text1']
    if (data['image']) {
        document.getElementById('statement-img').style.display = ''
        document.getElementById('statement-img').src = data['image']
        document.getElementById('statement-text2').style.display = ''
        document.getElementById('statement-text2').innerHTML = data['text2']
    }
    document.getElementById('answer-text').innerHTML = 'Ответ: ' + data['answer']
}







