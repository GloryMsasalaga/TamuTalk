document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("chat-form");
    const inputElement = document.getElementById("message");
    const chatBox = document.getElementById("chatBox");

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        try {
            const userMessage = inputElement.value.trim();

            if (!userMessage) {
                alert("Please type a message.");
                return;
            }
            
            // Display the user's message in the chat box
            addMessage(userMessage, true);

            console.log("User message:", userMessage);

            // Send the message to the server
            fetch('http://127.0.0.1:5000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage }),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log("Server response:", data);

                // Assuming server sends { response: "English..", swahili: "Swahili.." }
                const botResponse = data.swahili || data.response;
                addMessage(botResponse, false);
            })
            .catch(error => {
                console.error("An error occurred while sending the message:", error.message);
                addMessage("Error: Unable to communicate with the server.", false);
            });
        } catch (error) {
            console.error("An error occurred:", error.message);
        }

        inputElement.value = ""; // Clear input field
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
    });

    function addMessage(text, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user-message' : 'server-message');
        messageDiv.textContent = isUser ? `You: ${text}` : `TamuTalk: ${text}`;
        chatBox.appendChild(messageDiv);
    }
});