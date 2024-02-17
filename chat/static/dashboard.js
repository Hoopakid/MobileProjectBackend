document.addEventListener('DOMContentLoaded', function () {
    // Get the room name from the HTML data attribute
    const roomName = document.getElementById('chat').dataset.room;
    const chatInput = document.getElementById('chat-input');
    const chatForm = document.getElementById('chat-form');

    // Establish WebSocket connection
    const socket = new WebSocket(`ws://${window.location.host}/ws/chat/${roomName}/`);

    // Event handler for successful WebSocket connection
    socket.onopen = function (event) {
        console.log('WebSocket connection opened:', event);
    };

    // Event handler for incoming WebSocket messages
    socket.onmessage = function (event) {
        const message = JSON.parse(event.data);
        console.log('WebSocket message received:', message);

        // Handle incoming messages by appending them to the chat window
        appendMessage(message.message);
    };

    // Event handler for WebSocket connection closure
    socket.onclose = function (event) {
        console.log('WebSocket connection closed:', event);
    };

    // Event listener for form submission
    chatForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const message = chatInput.value.trim();

        if (message !== '') {
            // Send the message to the server
            socket.send(JSON.stringify({
                'message': message
            }));

            // Optionally, append the message to the chat window immediately
            appendMessage(message);

            // Clear the input field
            chatInput.value = '';
        }
    });

    // Function to append a message to the chat window
    function appendMessage(message) {
        const chatWindow = document.getElementById('chat-window');
        const messageElement = document.createElement('div');
        messageElement.textContent = message;
        chatWindow.appendChild(messageElement);
    }
});
