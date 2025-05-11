import { formManager } from "./formManager.js"

export function editGroup(groupId) {
    formManager('edit', groupId)
}

export function deleteGroup(event) {
    const groupId = event.target.parentNode.id
    fetch('/group_service/group_remover', {
        method: 'POST',
        body: groupId
    })
    .then(response => {
        if (response.ok) {
            location.reload()
        }
    })
    .catch(console.log.bind(console))
}

export function leaveGroup(event) {
    const groupId = event.target.parentNode.id
    fetch('/user_service/leave_group', {
        method: 'POST',
        body: groupId
    })
    .then(response => {
        if (response.ok) {
            location.reload()
        }
    })
    .catch(console.log.bind(console))
}