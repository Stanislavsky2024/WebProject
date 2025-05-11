import { changeSelectors } from './changeSelectors.js'
import { showSolution } from './showSolution.js'
import { checkAnswer } from './checkAnswer.js'
import { getTasks } from './showTasks.js'

function changeSelectorsManager(event) {
    const selector = event.target
    const selectors = document.querySelectorAll('select')
    if (selector.id === 'dropdown1') {
        changeSelectors(selectors[0], selectors[2])
    }
}

function showTasksManager() {
    setTimeout(getTasks, 50)
    setTimeout(rechargeEventListeners, 100)
}

function showSolutionManager(event) {
    const solutionButton = event.target
    const infoObject = {
        button: solutionButton,
        id: solutionButton.parentNode.parentNode.id,
        isActive: solutionButton.name,
        solutionSection: solutionButton.parentNode.parentNode.getElementsByClassName("solution-section")[0]
    }
    showSolution(infoObject)
}

function checkAnswerManager(event) {
    const checkButton = event.target
    const infoObject = {
        id: checkButton.parentNode.parentNode.parentNode.id,
        answerInput: checkButton.parentNode.children[0]
    }
    checkAnswer(infoObject)
}

function rechargeEventListeners() {
    const selectors = document.querySelectorAll('select')
    for (let selector of selectors) {
        selector.addEventListener('change', changeSelectorsManager)
        selector.addEventListener('change', showTasksManager)
    }

    const solutionButtons = document.getElementsByClassName('solution')
    for (let button of solutionButtons) {
        button.addEventListener('click', showSolutionManager)
    }

    const checkButtons = document.getElementsByClassName('submit')
    for (let button of checkButtons) {
        button.addEventListener('click', checkAnswerManager)
    }
}

document.addEventListener("DOMContentLoaded", rechargeEventListeners)

