const WebSocket = require("ws");

// Créer une nouvelle instance WebSocket
var socket = new WebSocket("ws://127.0.0.1:8080");

// Écouter l'événement d'ouverture de la connexion
socket.onopen = function() {
    console.log("Connexion établie");
    MessageAdd('<div class="message green">You have entered the chat room.</div>');
    // Envoyer un message au serveur
    socket.send("Bonjour, serveur !");
};

// Écouter les messages entrants
socket.onmessage = function(event) {
	var data = JSON.parse(event.data);

	if (data.type == "message") {
		MessageAdd('<div class="message">' + data.username + ': ' + data.message + '</div>');
 	}
};

// Gérer les erreurs
socket.onerror = function(error) {

    MessageAdd(`<div class="message red">Connection to chat failed with error: ${error}.</div>`);
    
    console.error("Erreur WebSocket :", error);
};

// Écouter la fermeture de la connexion
socket.onclose = function(event) {
    MessageAdd('<div class="message blue">You have been disconnected.</div>');
    console.log("Connexion fermée", event);
};


function Username() {
	var username = window.prompt("Enter your username:", "");

	if (username.toString().length > 2) {
		localStorage.setItem("username", username);
	}
	else {
		alert("Your username must be at least two characters.");
		Username();
	}
}

Username();

// chat form
document.getElementById("chat-form").addEventListener("submit", function(event) {
	event.preventDefault();

	var message_element = document.getElementsByTagName("input")[0];
	var message = message_element.value;

	if (message.toString().length) {
		var username = localStorage.getItem("username");

		var data = {
			type: "message",
			username: username,
			message: message
		};

		websocket.send(JSON.stringify(data));
		message_element.value = "";
	}
}, false);


function MessageAdd(message) {
	var chat_messages = document.getElementById("chat-messages");
    console.log("Message reçu :", message);
    // Ajouter le message au chat avant le dernier élément
	chat_messages.insertAdjacentHTML("beforeend", message);
	// automatic scroll that adjust to the minimum height required from all the messages to display
    chat_messages.scrollTop = chat_messages.scrollHeight;
}