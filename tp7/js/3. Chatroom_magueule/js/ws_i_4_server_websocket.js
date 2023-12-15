const redis = require('redis');
const WebSocket = require('ws');

// Create a Redis client
const client = redis.createClient({
    url: 'redis://10.1.2.254:6379'  // Replace with your Redis server URL
});

client.on('error', (err) => {
    console.error('Redis Client Error', err);
});

// Connect to Redis
client.connect().catch(console.error);

// Create a WebSocket server listening on port 8080
const wss = new WebSocket.Server({ port: 8080 });

// Handle WebSocket connection events
wss.on("connection", (ws) => {
    ws.on("message", async (message) => {
        // Store the message with a timestamp in Redis
        const timestamp = new Date().toISOString();
        await client.set(`message:${timestamp}`, message);

        // Broadcast the message to all clients except the sender
        wss.clients.forEach(async (otherClient) => {
            if (otherClient !== ws && otherClient.readyState === WebSocket.OPEN) {
                try {
                    const storedMessage = await client.get(`message:${timestamp}`);
                    otherClient.send(storedMessage, { binary: false });
                } catch (error) {
                    console.error('Error retrieving message from Redis:', error);
                }
            }
        });
    });

    ws.on('close', () => {
        console.log('Client disconnected');
    });
});

console.log('WebSocket server started on ws://localhost:8080');
