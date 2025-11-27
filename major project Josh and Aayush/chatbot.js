function sendMessage() {
    var userInput = document.getElementById("user-input").value;
    var chatMessages = document.getElementById("chat-messages");
    
    // Display user's message
    var userMessageElement = document.createElement("div");
    userMessageElement.className = "user-message";
    userMessageElement.textContent = "You: " + userInput;
    chatMessages.appendChild(userMessageElement);

    // Simulate chatbot response (you can replace this with actual chatbot logic)
    var chatbotResponseElement = document.createElement("div");
    chatbotResponseElement.className = "chatbot-message";
    chatbotResponseElement.textContent = "Chatbot: Thank you for your message! I will get back to you shortly.";
    chatMessages.appendChild(chatbotResponseElement);

    // Clear input field
    document.getElementById("user-input").value = "";
}
