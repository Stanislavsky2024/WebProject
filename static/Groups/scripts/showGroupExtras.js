let currentPressed = undefined

export function showExtras(event) {
    const groupId = event.target.name
    const frame = document.getElementById(groupId)

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