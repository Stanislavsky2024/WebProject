export let getTasks = () => {
    const option1 = document.getElementById('dropdown1')[document.getElementById('dropdown1').selectedIndex].text
    const option2 = document.getElementById('dropdown2')[document.getElementById('dropdown2').selectedIndex].text
    const option3 = document.getElementById('dropdown3')[document.getElementById('dropdown3').selectedIndex].text

    fetch('/task_service/get_tasks', {
        method: "POST",
        body: JSON.stringify({'options':[option1.split(' ')[1], option2, option3]})
    })
    .then(response => {
        if (response.ok) {
            return response.json()
        }
    })
    .then(data => {
        showTasks(data['tasks'], data['solved'].split(';'))
    })
    .catch(console.log.bind(console))
}

function showTasks(data, solved) {
    const tasksSection = document.getElementsByClassName('tasks-section')[0]
    let taskId
    let taskType
    let taskDifficulty
    let taskImage
    let taskText1
    let taskText2
    let id
    let isSolvedImage
    const taskNumber = document.getElementById('dropdown1')[document.getElementById('dropdown1').selectedIndex].text.split(' ')[1]
    
    while (tasksSection.children.length > 0) {
        tasksSection.removeChild(tasksSection.firstChild)
    }
    for (let i = 0; i < data.length; i++) {
        id = data[i].id
        taskId = data[i].task_id
        taskType = data[i].type
        taskDifficulty = data[i].difficulty
        if (data[i].image) {
            taskImage = data[i].image
            taskText1 = data[i].text1
            taskText2 = data[i].text2
        } else {
            taskImage = ''
            taskText2 = ''
            taskText1 = data[i].text1
        }
        tasksSection.insertAdjacentHTML("beforeend", 
            `<article class="task${i + 1}" id="${id}">
                <div class="info-section">
                    <div class="header-section">
                        <h1>Задание ${taskNumber}.${i + 1}</h1>
                        <img id="${id}_isSolved" style="display: none;" src="/static/cards/greenmark.png" alt="">
                    </div>
                    <div class="stats-section">
                        <div class="type">${taskType}</div>
                        <div class="difficulty">${taskDifficulty}</div>
                    </div>
                </div>
                <p style="white-space: pre-wrap">${taskText1}</p>
                <img name="image" src="${taskImage}" alt="">
                <p name="text2" style="white-space: pre-wrap">${taskText2}</p>
                <div class="interface-section">
                    <div class="input-answer">
                        <input type="text" name="answer" placeholder="Введите ответ" autocomplete="off">
                        <button class="submit">Проверить</button>
                    </div>
                    <button class="solution" name="false">Решение</button>
                </div>
                <p>Источник: <a style="padding-left: 10px;" target="_blank" href="https://oge.fipi.ru/bank/index.php?proj=74676951F093A0754D74F2D6E7955F06">Сайт ФИПИ</a></p>
                <div class="solution-section" style="display: none;">
                    <h1 class="solution-h1"></h1>
                    <p style="white-space: pre-wrap"></p>
                </div>
            </article>`
        )
        if (!solved) {
            continue
        }
        isSolvedImage = document.getElementById(`${id}_isSolved`)
        for (let solved_id of solved) {
            if (id == solved_id) {
                isSolvedImage.style.display = 'flex'
            }
        }
    }
    displayElements(taskImage)
}

function displayElements(isImage) {
    for (let element of document.getElementsByName('image')) {
        if (!isImage) {
            element.style.display = 'none'
        }
    }
    for (let element of document.getElementsByName('text2')) {
        if (!isImage) {
            element.style.display = 'none'
        }
    }
}





