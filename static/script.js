function sendMessage() {
    const message = document.getElementById("message").value;
    const status = document.getElementById("status").value;

    fetch(`/update/${currentUser}`, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status, message })
    });

    document.getElementById("message").value = "";
}

function updateStatusOnly() {
    const status = document.getElementById("status").value;

    fetch(`/update/${currentUser}`, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status, message: "" })
    });
}

function fetchPartnerData() {
    fetch(`/get/${currentUser}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("partnerStatus").innerText = data.status;
            displayMessages(data.messages);
        });
}

function displayMessages(messages) {
    const messagesContainer = document.getElementById("messages");
    messagesContainer.innerHTML = "";

    messages.forEach(msg => {
        const messageDiv = document.createElement("div");
        messageDiv.innerHTML = `<strong>${msg.timestamp}:</strong> ${msg.text}`;
        messagesContainer.appendChild(messageDiv);
    });
}

document.getElementById("status").addEventListener("change", updateStatusOnly);
document.getElementById("bgColor").addEventListener("change", (e) => {
    document.body.style.backgroundColor = e.target.value;
});
document.getElementById("fontFamily").addEventListener("change", (e) => {
    document.body.style.fontFamily = e.target.value;
});

setInterval(fetchPartnerData, 3000);