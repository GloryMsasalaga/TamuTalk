document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("chat-form");
    const inputElement = document.getElementById("message");
    const chatBox = document.getElementById("chatBox");
    //const message = document.getElementById("message-container");

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        try {
            const userMessage = inputElement.value.trim();

            if (!userMessage) {
                alert("Please type a message.");
                return;
            }
            
            //display the user's message in the chat box
            
            appendMessage(userMessage, "user");

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

                //assuming server sends { response" "English..", swahili: "swahili.."}
                const botResponse = data.swahili || data.response;
                appendMessage("bot", botResponse);
            })
            .catch(error => {
                console.error("An error occurred while sending the message:", error.message);
            });
        } catch (error) {
            console.error("An error occurred:", error.message);
        }

        inputElement.value = ""; // Clear input field
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
    });

    function appendMessage(sender, text) {
        const msgDiv = document.createElement("div");
        msgDiv.className = sender === "user" ? "user-message" : sender === "bot" ? "bot-message" : "error-message";
        msgDiv.textContent = sender === "user" ? `You: ${text}` : sender === "bot" ? `TamuTalk: ${text}` : text;
        //message.appendChild(msgDiv);
        message.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
    }
});


/*
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("chat-form");
    const inputElement = document.getElementById("message");

    if (!form || !inputElement) {
        console.error("Form or input element not found!");
        return;
    }

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        try {
            const userMessage = inputElement.value.trim();

            if (!userMessage) {
                alert("Please type a message.");
                return;
            }

            console.log("User message:", userMessage);
            inputElement.value = "";
        } catch (error) {
            console.error("An error occurred:", error.message);
        }
    });
});
*/