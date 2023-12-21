const WebSocket = require('ws');

// Créer un serveur WebSocket sur le port 8080
const wss = new WebSocket.Server({ port: 8765 });

wss.on('connection', function connection(ws) {
    console.log('Un client est connecté');

    // Envoyer un message de bienvenue au client
    ws.send('Bienvenue sur le serveur WebSocket!');

    // Écouter les messages du client
    ws.on('message', function incoming(message) {
        console.log('Message reçu:', message.toString("utf-8"));

        // Vous pouvez ici répondre au client ou traiter le message
    });

    // Écouter la fermeture de la connexion
    ws.on('close', function() {
        console.log('Client déconnecté');
    });
});

console.log('Serveur WebSocket démarré sur ws://localhost:8765');
