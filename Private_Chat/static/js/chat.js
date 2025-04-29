const roomName = "general/first";  // Replace with the actual room name
const protocol = window.location.protocol === "https:" ? "wss://" : "ws://";  // Use wss:// for HTTPS
const chatSocket = new WebSocket(
    `${protocol}${window.location.host}/chat/${roomName}/`  // Match WebSocket paths without /ws/
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log("Message received:", data.message);
};

chatSocket.onclose = function(e) {
    console.error("WebSocket closed unexpectedly");
};
