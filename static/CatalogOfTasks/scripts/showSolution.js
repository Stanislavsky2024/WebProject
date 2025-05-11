export let showSolution = (infoObject) => {
    const children = infoObject.solutionSection.children
    if (infoObject.isActive === 'false') {
        fetch('/task_service/get_solution', {
            method: 'POST',
            body: infoObject.id
        })
        .then(response => {
            if (response.ok) {
                return response.text()
            }
        })
        .then(solution => {
            children[0].innerHTML = 'Решение задания'
            children[1].innerHTML = solution
            infoObject.button.name = 'true'
            infoObject.solutionSection.style.display = ''
        })
    } else {
        children[0].innerHTML = ''
        children[1].innerHTML = ''
        infoObject.button.name = 'false'
        infoObject.solutionSection.style.display = 'none'
    }
}