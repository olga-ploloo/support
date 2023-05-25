import useWebSocket, {ReadyState} from "react-use-websocket";
import React, {useEffect, useState} from "react";
import * as constants from "../constatns/ticketConstans";
import {useParams} from "react-router-dom";

const ChatComponent = () => {
    const {id} = useParams()
    const [message, setMessage] = useState("");
    const [messageHistory, setMessageHistory] = useState([]);

    // console.log(localStorage.access)
    const socketUrl = `ws://${constants.HOST}/ws/chat/${id}/?token=${localStorage.access}`;
    const [welcomeMessage, setWelcomeMessage] = useState("");
    const socket = useWebSocket(socketUrl);



const handleSubmit = () => {
    socket.sendJsonMessage({
        name: "chat_message",
        message: message,
    });
    setMessage("");
};
//
// useEffect(() => {
//     if (lastMessage !== null) {
//         setReceivedMessages(prevMessages => [...prevMessages, lastMessage]);
//     }
// }, [lastMessage]);
//
// return (
//     <div>
//         <h1>Chat</h1>
//         <div>
//             {receivedMessages.map((msg, index) => (
//                 <p key={index}>{msg.data}</p>
//             ))}
//         </div>
//         <input
//             type="text"
//             value={message}
//             onChange={(e) => setMessage(e.target.value)}
//         />
//         <button onClick={handleSendMessage}>Send</button>
//     </div>
// );
// const {readyState} = useWebSocket(socketUrl,);


// console.log(socket)
    socket.onopen= () => {
        console.log("Connected!");
    };
socket.onclose = () => {
    console.log("Disconnected!");
}

//     onMessage: (e) => {
//         const data = JSON.parse(e.data);
//         switch (data.type) {
//             case "welcome_message":
//                 setWelcomeMessage(data.message);
//                 break;
//             default:
//                 console.log("Unknown message type!");
//                 break;
//         }
//     },

// console.log(readyState)
//
// const connectionStatus = {
//     [ReadyState.CONNECTING]: "Connecting",
//     [ReadyState.OPEN]: "Open",
//     [ReadyState.CLOSING]: "Closing",
//     [ReadyState.CLOSED]: "Closed",
//     [ReadyState.UNINSTANTIATED]: "Uninstantiated"
// }[readyState];

return (
    <>
        <span>The WebSocket is currently </span>
        <p>{welcomeMessage}</p>
        <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}/>
        <button
            className="bg-gray-300 px-3 py-1"
            onClick={handleSubmit}>
            Submit
        </button>
    </>
);
}
;

export default ChatComponent;