let currentPressed = undefined

export function showExtras(event) {
    const groupId = event.target.name
    let frame
    if (event.target.id === 'more1') {
        frame = document.getElementById(`extras1-${groupId}`)
    } else {
        frame = document.getElementById(`extras2-${groupId}`)
    }

    if (frame.style.display == 'none') {
        frame.style.display = ''
        if (currentPressed) {
            currentPressed.style.display = 'none'
        }
        currentPressed = frame
    } else {
        frame.style.display = 'none'
        currentPressed = undefined
    }
}