const photoLoader = document.getElementById('photo-loader')
const photoContainer = document.getElementById('avatar-upload')
const avatar = document.getElementById('avatar-image')
photoContainer.addEventListener("change", sendPhoto)


function sendPhoto() {
    const image = photoContainer.files[0]
    fetch('user_service/avatar_loader', {
        method: 'POST',
        body: image
    }).then(response => {
            if (response.ok) {
                response.text().then(src => {
                    avatar.src = src
                    location.reload()
                })
            }
    })
}


