window.addEventListener("DOMContentLoaded", () => {
    const websocket = new WebSocket("ws://localhost:6789/");
    setTimeout(() => {   websocket.send("Hi") }, 3000);

    websocket.onmessage = ({ data }) => {
        console.log(data)
    }
});