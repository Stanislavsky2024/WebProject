let answers = {}
globalThis.btnText = '1'

const elementsList = {
    imageElement: document.getElementById('img'),
    text1Element: document.getElementById('text1'),
    text2Element: document.getElementById('text2'),
    inputElement: document.getElementById('answer'),
    finishElement: document.getElementById('finish'),
    taskElement: document.getElementById('task'),
    savedElement: document.getElementById('saved')
}
const buttonsList = [
    document.getElementById('btn2'), document.getElementById('btn3'), document.getElementById('btn4'), 
    document.getElementById('btn5'), document.getElementById('btn6'), document.getElementById('btn7')
]


function getInteractedButtons(buttonsList, letter) {
    let interactedButtons = {
        'pressed': [],
        'solved': []
    }
    for (let button of buttonsList) {
        button.className = ''
        if (button.innerHTML === letter && button.innerHTML !== '...') {
            interactedButtons.pressed.push(button)
        } else if (answers[button.innerHTML] && button.innerHTML !== '...') {
            interactedButtons.solved.push(button)
        }
    }
    return interactedButtons
}

function changeElementsAppearance(interactedButtons, task) {
    elementsList.savedElement.style.display = 'none'
    elementsList.imageElement.src = task['image']
    elementsList.text1Element.innerHTML = task['text1']
    elementsList.text2Element.innerHTML = task['text2']
    if (task['image']) {
        elementsList.imageElement.style.display = 'flex'
        elementsList.text2Element.style.display = 'flex'
    } else {
        elementsList.imageElement.style.display = 'none'
        elementsList.text2Element.style.display = 'none'
    }
    for (let button of interactedButtons.pressed) {
        button.className = 'pressed'
        if (button.id === 'btn7') {
            elementsList.finishElement.style.display = 'block'
        } else {
            elementsList.finishElement.style.display = 'none'
        }
        elementsList.taskElement.innerHTML = `Задание ${button.innerHTML}`
    }
    for (let button of interactedButtons.solved) {
        button.className = 'solved'
    }
    if (!answers[globalThis.btnText]) {
        elementsList.inputElement.value = ''
    } else {
        elementsList.inputElement.value = answers[globalThis.btnText]
    }
}

function changeButtonsAppearance(letter) {
    if (letter === 'v' && buttonsList[4].innerHTML === '...') {
        for (let i = 0; i < buttonsList.length - 1; i++) {
            buttonsList[i].innerHTML = String(Number(buttonsList[i].innerHTML) + 1)
            if (i === 4 && buttonsList[3].innerHTML === String(Number(buttonsList[5].innerHTML) - 2)) {
                buttonsList[i].innerHTML = String(Number(buttonsList[5].innerHTML) - 1)
            } else if (i === 4) {
                buttonsList[i].innerHTML = '...'
            }
        }
    } 
    else if (letter === 'ʌ' && buttonsList[0].innerHTML !== '1')  {
        for (let i = 0; i < buttonsList.length - 1; i++) {
            buttonsList[i].innerHTML = String(Number(buttonsList[i].innerHTML) - 1)
            if (i === 4 && buttonsList[3].innerHTML !== String(Number(buttonsList[5].innerHTML) - 2)) {
                buttonsList[i].innerHTML = '...'
            }
        }
    }
    for (let button of buttonsList) {
        if (button.innerHTML === globalThis.btnText) {
            button.className = 'pressed'
        } else if (answers[button.innerHTML]) {
            button.className = 'solved'
        } else {
            button.className = ''
        }
    }
}

function appearanceChangeManager(letter, task, key) {
    if (key === 1) {
        const interactedButtons = getInteractedButtons(buttonsList, letter)
        globalThis.btnText = letter
        changeElementsAppearance(interactedButtons, task)
    } else if (key === 2) {
        changeButtonsAppearance(letter)
    }
}

function saveAnswer() {
    const taskNum = document.getElementsByClassName('pressed')[0].innerHTML
    if (elementsList.inputElement.value) {
        answers[taskNum] = elementsList.inputElement.value
        elementsList.savedElement.style.display = 'block'
    }
}

function finishVariant() {
    fetch('/variant_service/get_answers', {
        method: 'POST',
        body: JSON.stringify({
            'answers': answers,
            'var': document.querySelector('.content-section').id
        })
    })
    .then(response => {
        if (response.ok) {
            if (document.querySelector('.content-section').id.split('-')[1] === 'variant') {
                location.replace('/variants/results')
            } else {
                location.replace('/groups/results')
            }
        }
    })
    .catch(console.log.bind(console))
}

function center(event) {
    let text = event.target.innerHTML
    if (text.length < 3 && text !== 'ʌ' && text !== 'v') {
        const task = globalThis.tasks[Number(text) - 1]
        appearanceChangeManager(text, task, 1)
    } else if (text === 'ʌ' || text === 'v') {
        appearanceChangeManager(text, undefined, 2)
    } else if (text === 'Сохранить') {
        saveAnswer()
    } else if (text === 'Завершить вариант' || text === 'Завершить работу') {
        finishVariant()
    }

}

function main() {
    fetch('/variant_service/get_tasks', {
        method: 'POST',
        body: document.getElementsByClassName('content-section')[0].id
    })
    .then(response => {
        if (response.ok) {
            return response.json()
        }
    })
    .then(tasks => {
        globalThis.tasks = tasks
    })
    .catch(console.log.bind(console))
    for (let button of document.querySelectorAll('button')) {
        button.addEventListener('click', center)
    }
}

setTimeout(main, 10)