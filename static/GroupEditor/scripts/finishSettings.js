export function finishAnnouncement() {
    const errorMessage = document.getElementById('announcement-error')
    const data = {
        'title': document.getElementById('title').value, 
        'text': document.getElementById('text').value,
        'group_id': document.querySelector('.content-section').id.split('/')[2]
    }
    if (!data['title'] || !data['text']) {
        errorMessage.innerHTML = 'У объявления должен быть заголовок и текст'
        return
    }
    errorMessage.innerHTML = ''
    fetch('/group_service/add_announcement', {
        method: 'POST',
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            location.replace(`/groups/${data['group_id']}`)
        }
    })
    .catch(console.log.bind(console))
}


export function finishWork() {
    const tableBody = document.getElementById('work').tBodies[0]
    const name = document.getElementById('work-name').value
    const errorMessage = document.getElementById('tasks-section-error')
    const tasks = []
    for (let row of tableBody.rows) {
        tasks.push(row.task)
    }
    if (!name) {
        errorMessage.innerHTML = 'У добавляемой работы должно быть название'
        return
    }
    if (tasks.length < 6) {
        errorMessage.innerHTML = 'У добавляемой работы должно быть минимум 6 заданий'
        return
    }
    const data = {
        'name': name, 
        'tasks': tasks, 
        'group_id': document.querySelector('.content-section').id.split('/')[2]
    }
    errorMessage.innerHTML = ''
    fetch('/group_service/add_group_work', {
        method: 'POST',
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            location.replace(`/groups/${data['group_id']}`)
        }
    })
    .catch(console.log.bind(console))
}







