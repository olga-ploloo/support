import useWebSocket from "react-use-websocket";
import React, {useEffect, useState} from "react";
import * as constants from "../constatns/ticketConstans";
import {useParams} from "react-router-dom";
import axios from "axios";
import MessageList from "../components/messageList";
import jwt_decode from 'jwt-decode';
import {Button, Container, Input, InputGroup} from "reactstrap";
import {IconButton, TextareaAutosize, TextField} from "@mui/material";
import SendIcon from "@mui/icons-material/Send"


const Chat = () => {
    const {id} = useParams()
    const [message, setMessage] = useState("");
    const [messageHistory, setMessageHistory] = useState([]);
    const [currentUserId, setCurrentUserId] = useState(null);

    const token = localStorage.access;
    const socketUrl = `ws://${constants.HOST}/ws/chat/${id}/?token=${localStorage.access}`;

    const socket = useWebSocket(socketUrl, {
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

    // Decode the JWT token to get the user information
    const getCurrentUserInfo = () => {
        if (token) {
            const decodedToken = jwt_decode(token);
            setCurrentUserId(decodedToken.user_id)
        }
    }

    const addMessage = (newMessage) => {
        setMessageHistory(actualMessage => [newMessage, ...(actualMessage ?? [])]);
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

    const handleSubmit = () => {
        // toDo: check for whitespace
        if (message) {
            socket.sendJsonMessage({
                message: message,
            });
            setMessage("");
        }
    };

    useEffect(() => {
        getMessages();
        getCurrentUserInfo();
    }, [token])

    return (
        <div className="chat-page">
            <h1>Chat</h1>
            <Container className="chat-container">
                <MessageList messageHistory={messageHistory}
                             currentUserId={currentUserId}/>
                <div className="chat-send-message">
                    <TextareaAutosize
                        value={message}
                        className="chat-user-input"
                        onChange={(e) => setMessage(e.target.value)}
                        placeholder="write your message"/>
                    <IconButton
                        onClick={handleSubmit}>
                        <SendIcon className="chat-submit-button"/>
                    </IconButton>
                </div>
            </Container>
        </div>
    );
};

export default Chat;