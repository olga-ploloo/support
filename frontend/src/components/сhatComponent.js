import useWebSocket, {ReadyState} from "react-use-websocket";
import React, {useEffect, useState} from "react";
import * as constants from "../constatns/ticketConstans";
import {useParams} from "react-router-dom";
import axios from "axios";
import {Col, Row} from "reactstrap";

const ChatComponent = () => {
        const {id} = useParams()
        const [message, setMessage] = useState("");
        const [messageHistory, setMessageHistory] = useState([]);
        const socketUrl = `ws://${constants.HOST}/ws/chat/${id}/?token=${localStorage.access}`;

        const {
            sendMessage,
            sendJsonMessage,
            lastMessage,
            lastJsonMessage,
            readyState,
            getWebSocket,
        } = useWebSocket(socketUrl, {
            onOpen: () => console.log('Connected'),
            onClose: () => console.log('Disconnected'),
            shouldReconnect: (closeEvent) => true,
            onError: (error) => console.log("WebSocket encountered an error: " + error.text),
            onMessage: (event) => {
                console.log("onmessage data " + event);
                addMessage(event.toString());
            }
        });

        const addMessage = (message) => {
            setMessageHistory((prevMessages) => [...prevMessages, message]);
        };
        const getMessages = async () => {
            try {
                const response = await axios.get(`${constants.API_URL}/messages/`, {
                    params: {
                        ticket: id,
                    }
                });
                setMessageHistory(response.data)
            } catch (error) {
                console.log(error)
            }
        }

        useEffect(() => {
            getMessages();
        }, [])
        const handleSubmit = () => {
            // toDo: check for whitespace
            if (message) {
                sendJsonMessage({
                    // name: "chat_message",
                    message: message,
                });
                setMessage("");
            }
        };

//
// useEffect(() => {
//     if (lastMessage !== null) {
//         setReceivedMessages(prevMessages => [...prevMessages, lastMessage]);
//     }
// }, [lastMessage]);
//
        return (
            <>
                <h1>Chat</h1>
                <p>{getWebSocket}</p>

                {messageHistory &&
                    <div>
                        {messageHistory.map((message, index) => (
                            <div className="message" key={index}>
                                <Row>
                                    <Col>
                                        {message.author}:
                                    </Col>
                                    <Col>
                                        {message.message}
                                    </Col>

                                </Row>
                            </div>

                        ))}
                    </div>
                }
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