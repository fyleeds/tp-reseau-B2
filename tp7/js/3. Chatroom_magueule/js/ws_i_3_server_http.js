const express = require("express");
const app = express();
const path = require('path');
const WebSocket = require("ws");
const http = require("http");

const server = http.createServer(app);

// Creating the WebSocket server
const ws_server = new WebSocket.Server({ server });

ws_server.on("connection", (ws) => {
    ws.on("message", (message) => {
        // Broadcast the message to all clients except the sender
        ws_server.clients.forEach((client) => {
            if (client !== ws && client.readyState === WebSocket.OPEN) {
                console.log("message to send : "+ message);
                client.send(message,{ binary: false });
            }
        });
    });

    ws.on('close', () => {
        console.log('Client disconnected');
    });
});

app.get("/", (req, res) => {
    let parentDir = path.join(__dirname, '..');
    let htmlPath = path.join(parentDir, 'index2.html');
    res.sendFile(htmlPath);
});

server.listen(8080, () => {
    console.log(`Server listening on port 8080`);
});
