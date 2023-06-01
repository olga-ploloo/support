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
                let data = JSON.parse(event.data);
                console.log('on message ' + data.message)
                addMessage(data.message);
            }
        });

        const addMessage = (newMessage) => {
            // setMessageHistory((prevMessages) => [...prevMessages, message]);
            setMessageHistory(actualMessage => [...actualMessage, newMessage]);

            console.log('add mesage to histiry')
            console.log(messageHistory)
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
            console.log('messageHistory:', messageHistory);
            console.log('change');

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


        return (
            <>
                <h1>Chat</h1>
                <p>{getWebSocket}</p>

                {messageHistory &&
                    <div>
                        {messageHistory.slice().reverse().map((message, index) => (
                            <div className="message" key={message.id}>
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