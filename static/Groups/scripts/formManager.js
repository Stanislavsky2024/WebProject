const formCreateInputs = document.getElementsByClassName('inputTextCreate')
const formCreateError = document.getElementById('formCreateError')

const formEditInputs = document.getElementsByClassName('inputTextEdit')
const formEditError = document.getElementById('formEditError')


export function formManager(key, groupId) {
    if (inputValidationChecker(key) === 'fail') {
        return
    }
    if (key == 'create') {
        createGroup()
    } 
    else if (key == 'edit') {
        editGroup(groupId)
    }
}

function inputValidationChecker(key) {
    if (key == 'create') {
        if (formCreateInputs[0].value == '' || formCreateInputs[1].value == '') {
            formCreateError.style.display = ''
            formCreateError.innerHTML = 'Заполните все поля формы'
            return 'fail'
        } else if (formCreateInputs[0].value.length > 20) {
            formCreateError.style.display = ''
            formCreateError.innerHTML = 'Длина названия не должна превышать 20 символов'
            return 'fail'
        } else if (formCreateInputs[1].value.length > 30) {
            formCreateError.style.display = ''
            formCreateError.innerHTML = 'Длина описания не должна превышать 30 символов'
            return 'fail'
        }
    } else if (key == 'edit') {
        if (formEditInputs[0].value == '' || formEditInputs[1].value == '') {
            formEditError.style.display = ''
            formEditError.innerHTML = 'Заполните все поля формы'
            return 'fail'
        } else if (formEditInputs[0].value.length > 20) {
            formEditError.style.display = ''
            formEditError.innerHTML = 'Длина названия не должна превышать 20 символов'
            return 'fail'
        } else if (formEditInputs[1].value.length > 30) {
            formEditError.style.display = ''
            formEditError.innerHTML = 'Длина описания не должна превышать 30 символов'
            return 'fail'
        }
    }
    return 'ok'
}

function createGroup() {
    fetch('/group_service/check_group_name_validation', {
        method: 'POST',
        body: formCreateInputs[0].value
    })
    .then(response => {
        if (response.ok) {
            return response.text()
        }
    })
    .then(status => {
        if (status == 'failed') {
            formCreateError.style.display = ''
            formCreateError.innerHTML = 'Названия всех Ваших групп не должны повторяться'
            return false
        }
        return true
    })
    .then(result => {
        if (result) {
            fetch('/group_service/group_creator', {
                method: 'POST',
                body: JSON.stringify({
                    'name': formCreateInputs[0].value,
                    'description': formCreateInputs[1].value
                })
            })
            .then(response => {
                if (response.ok) {
                    return response.text()
                }
            })
            .then(status => {
                if (status == 'ok') {
                    for (let input of formCreateInputs) {
                        input.value = ''
                    }
                    formCreateError.style.display = 'none'
                    location.reload()
                }
            })
            .catch(console.log.bind(console))
        }
    })
    .catch(console.log.bind(console))
}

function editGroup(groupId) {
    fetch('/group_service/check_group_name_validation', {
        method: 'POST',
        body: formEditInputs[0].value
    })
    .then(response => {
        if (response.ok) {
            return response.text()
        }
    })
    .then(status => {
        if (status == 'failed') {
            formEditError.style.display = ''
            formEditError.innerHTML = 'Названия всех Ваших групп не должны повторяться'
            return false
        }
        return true
    })
    .then(result => {
        if (result) {
            fetch('/group_service/group_editor', {
                method: 'POST',
                body: JSON.stringify({
                    'name': formEditInputs[0].value,
                    'description': formEditInputs[1].value,
                    'group_id': groupId
                })
            })
            .then(response => {
                if (response.ok) {
                    return response.text()
                }
            })
            .then(status => {
                if (status == 'ok') {
                    for (let input of formEditInputs) {
                        input.value = ''
                    }
                    formEditError.style.display = 'none'
                    location.reload()
                }
            })
            .catch(console.log.bind(console))
        }
    })
    .catch(console.log.bind(console))
}


