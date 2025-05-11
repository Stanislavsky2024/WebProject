export let checkAnswer = (infoObject) => {
    fetch('/task_service/get_answers', {
        method: 'POST',
        body: JSON.stringify({'id':infoObject.id, 'answer':infoObject.answerInput.value})
    })
    .then(response => {
        if (response.ok) {
            return response.text()
        }
    })
    .then(data => {
        if (data === 'ok') {
            modifyInputElem(true, infoObject.answerInput, infoObject.id)
        } else {
            modifyInputElem(false, infoObject.answerInput, infoObject.id)
        }
    })
    .catch(console.log.bind(console))
}

function modifyInputElem(result, input, id) {
    input.value = ''
    if (result) {
        input.placeholder = 'Ответ верный'
        input.style.background = 'rgb(139, 237, 130)'
        fetch('/task_service/make_solved', {
            method: 'POST',
            body: id
        })
        .then(response => {
            if (response.ok) {
                return response.text()
            }
        })
        .then(result => {
            if (result === 'ok') {
                const image = input.parentNode.parentNode.parentNode.querySelector('.info-section').querySelector('.header-section').children[1]
                image.style.display = ''
            }
        })
        .catch(console.log.bind(console))
    } else {
        input.placeholder = 'Ответ неверный'
        input.style.background = 'rgb(252, 179, 179)'
    }
}


