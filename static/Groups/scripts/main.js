import { formManager } from "./formManager.js"
import { showExtras } from "./showGroupExtras.js"
import { editGroup, deleteGroup, leaveGroup } from "./extrasMenu.js"

const dialogCreateOpenButton = document.querySelector('.create-button')
const dialogCreateCloseButton = document.querySelector('.closeDialogCreate')
const dialogCreateSubmitButton = document.querySelector('.submitDialogCreate')
const dialogCreate = document.querySelector('.createGroup')
const formCreateInputs = document.getElementsByClassName('inputTextCreate')
const formCreateError = document.getElementById('formCreateError')

const dialogEdit = document.querySelector('.editGroup')
const dialogEditCloseButton = document.querySelector('.closeDialogEdit')
const dialogEditSubmitButton = document.querySelector('.submitDialogEdit')
const formEditInputs = document.getElementsByClassName('inputTextEdit')
const formEditError = document.getElementById('formEditError')
let groupEditId

const extrasButtons = document.getElementsByClassName('more')
const editGroupButtons = document.getElementsByClassName('edit')
const deleteGroupButtons = document.getElementsByClassName('delete')
const leaveGroupButtons = document.getElementsByClassName('leave')


try {
    dialogCreateOpenButton.addEventListener('click', () => {
        dialogCreate.showModal()
    })

    dialogCreateCloseButton.addEventListener('click', () => {
        for (let input of formCreateInputs) {
            input.value = ''
        }
        formCreateError.style.display = 'none'
        dialogCreate.close()
    })

    dialogCreateSubmitButton.addEventListener('click', () => {
        formManager('create')
    })


    for (let button of editGroupButtons) {
        button.addEventListener('click', (event) => {
            groupEditId = event.target.parentNode.id
            dialogEdit.showModal()
        })
    }

    dialogEditCloseButton.addEventListener('click', () => {
        for (let input of formEditInputs) {
            input.value = ''
        }
        formEditError.style.display = 'none'
        dialogEdit.close()
    })

    dialogEditSubmitButton.addEventListener('click', () => {
        editGroup(groupEditId)
    })

    for (let button of deleteGroupButtons) {
        button.addEventListener('click', deleteGroup)
    }
}
catch {}

for (let button of extrasButtons) {
    button.addEventListener('click', showExtras)
}

for (let button of leaveGroupButtons) {
    button.addEventListener('click', leaveGroup)
}

