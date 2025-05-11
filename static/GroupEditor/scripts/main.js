import { getTask } from "./getTasks.js"
import { addTask } from "./taskManager.js"
import { changeSelectors } from "./changeSelectors.js"
import { finishAnnouncement, finishWork } from "./finishSettings.js"

const selectors = [document.querySelector('.dropdown1'), document.querySelector('.dropdown2'), document.querySelector('.dropdown3')]
const dialog = document.getElementById('task-statement-dialog')
const dialogClose = document.querySelector('.close')
const finishAnnouncementButton = document.getElementById('apply-announcement')
const finishWorkButton = document.getElementById('apply-work')
const addCustomTaskButton = document.getElementById('apply-custom-task')
const radiosOptions = document.getElementsByClassName('options')
const radioAnnouncement = document.getElementById('announcement')
const radioTasks = document.getElementById('tasks')

for (let selector of selectors) {
    selector.addEventListener('change', checkSelectors)
}
for (let radio of radiosOptions) {
    radio.addEventListener('click', changeOption)
}

dialogClose.addEventListener('click', () => {dialog.close()})
finishAnnouncementButton.addEventListener('click', finishAnnouncement)
finishWorkButton.addEventListener('click', finishWork)
addCustomTaskButton.addEventListener('click', prepareCustomTask)
radioAnnouncement.addEventListener('click', changeSection)
radioTasks.addEventListener('click', changeSection)


function checkSelectors(event) {
    const selector = event.target
    if (selector.id === 'dropdown1') {
        changeSelectors(selectors[0], selectors[2])
    }
    for (let selector of selectors) {
        const text = selector[selector.selectedIndex].text
        if (text[text.length - 1] === '.') {
            return
        }
    }
    getTask(selectors)
}


function prepareCustomTask() {
    const statement = document.getElementById('create-statement').value
    const answer = document.getElementById('create-answer').value
    const errorMessage = document.getElementById('create-error')
    if (!statement || !answer) {
        errorMessage.innerHTML = 'Условие и ответ не могут быть пустыми'
        return
    }
    errorMessage.innerHTML = ''
    addCustomTaskButton.task = {
        'text1': document.getElementById('create-statement').value, 
        'answer': document.getElementById('create-answer').value
    }
    addTask(addCustomTaskButton)
}


function changeOption(event) {
    const radio = event.target
    const chooseDiv = document.querySelector('.choose')
    const createDiv = document.querySelector('.create')
    if (radio.innerHTML === 'Выбрать из существующих') {
        chooseDiv.style.display = ''
        createDiv.style.display = 'none'
    } else {
        chooseDiv.style.display = 'none'
        createDiv.style.display = ''
    }
}


function changeSection(event) {
    const radio = event.target
    const announcementDiv = document.querySelector('.announcement-section')
    const tasksDiv = document.querySelector('.tasks-section')
    if (radio.id === 'announcement') {
        announcementDiv.style.display = ''
        tasksDiv.style.display = 'none'
    } else {
        announcementDiv.style.display = 'none'
        tasksDiv.style.display = ''
    }
}



