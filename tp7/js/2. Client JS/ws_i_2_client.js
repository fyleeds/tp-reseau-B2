

const WebSocket = require('ws');

// Créer une nouvelle instance WebSocket
var socket = new WebSocket("ws://localhost:8080");

// Écouter l'événement d'ouverture de la connexion
socket.onopen = function() {
    console.log("Connexion établie");

    // Envoyer un message au serveur
    socket.send("Bonjour, serveur !");
};

// Écouter les messages entrants
socket.onmessage = function(event) {
    console.log("Message reçu :", event.data);
};

// Gérer les erreurs
socket.onerror = function(error) {
    console.error("Erreur WebSocket :", error);
};

// Écouter la fermeture de la connexion
socket.onclose = function(event) {
    console.log("Connexion fermée", event);
};
