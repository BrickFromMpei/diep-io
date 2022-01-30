window.addEventListener("DOMContentLoaded", () => {
  const websocket = new WebSocket("ws://localhost:6789/");
  websocket.send("Hi")
});