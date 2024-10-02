// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to fetch response from the chatbot backend
async function fetchChatbotResponse(userMessage) {
    try {
        const response = await fetch('/chatbot/', {  // Ensure there is a trailing slash here
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),  // Include CSRF token if needed
            },
            body: JSON.stringify({ message: userMessage })
        });

        if (response.ok) {
            const data = await response.json();
            return data.reply; // Assuming the response has a 'reply' key
        } else {
            console.error('Server error:', response.status);
            return "Sorry, I couldn't get a response from the bot.";
        }
    } catch (error) {
        console.error('Fetch error:', error);
        return "Sorry, I couldn't get a response from the bot.";
    }
}

// Function to send user's message and display bot's response
async function sendMessage() {
    const userInput = document.getElementById("user_input");
    const userMessage = userInput.value;

    if (userMessage.trim() === "") return; // Don't send empty messages

    // Display user's message
    appendMessage("You: " + userMessage, 'user-message-container');

    // Fetch bot's response
    const botResponse = await fetchChatbotResponse(userMessage);
    appendMessage(botResponse, 'bot-response');

    // Clear input field
    userInput.value = "";
}

// Function to append messages to chat log
function appendMessage(message, type) {
    const chatlog = document.getElementById("chatlog");
    const messageContainer = document.createElement("div");
    messageContainer.className = type;
    messageContainer.innerHTML = `
        <div class="${type === 'bot-response' ? 'bot-avatar' : 'user-avatar'}"></div>
        <div class="${type === 'bot-response' ? 'bot-response-text' : 'user-message'}">${message}</div>
    `;
    chatlog.appendChild(messageContainer);
    chatlog.scrollTop = chatlog.scrollHeight;  // Scroll to the bottom of the chat log
}

// Optional: Add event listener for Enter key
document.getElementById("user_input").addEventListener("keypress", function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});