const readline = require('readline');
const WebSocket = require('ws');

// Create a new WebSocket.
const socket = new WebSocket('ws://localhost:8080');

// Create readline interface for console input
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Function to send messages to the server
const sendMessage = async (msg) => {
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(msg);
    } else {
        console.error("WebSocket is not open.");
    }
};

// Function to receive messages from the server
socket.addEventListener('message', function (event) {
    console.log('Message from server:', event.data);
});

// Function to asynchronously ask for input
const askQuestion = (query) => new Promise(resolve => rl.question(query, resolve));

// Main function to handle input and WebSocket events
const main = async () => {
    while (true) {
        const message = await askQuestion("Enter message to send: ");
        await sendMessage(message);
    }
};

// Start the main function
main();
