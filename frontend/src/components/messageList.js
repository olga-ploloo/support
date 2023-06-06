import {Col, Row, Container} from "reactstrap";
import React from "react";
import moment from "moment/moment";

const MessageList = ({messageHistory, currentUserId}) => {
    const isCurrentUserMessage = (message) => {
        return message.author_id === currentUserId;
  };

    return (
        <>
            <Container className="chat-message-list">
            {messageHistory &&
                <div>
                    {messageHistory.slice().reverse().map((message, index) => (
                        <div className="message" key={message.id}>
                            <div className={isCurrentUserMessage(message) ? "chat-message-row user-message" : "chat-message-row"}>
                                <div>
                                    {!isCurrentUserMessage(message) ? message.author + ":": ""}
                                </div>
                                <div className="chat-message">
                                    {message.message}
                                </div>
                                <div className="chat-message-spacer">

                                </div>
                                <div className="chat-message-status">
                                    {moment(message.created_at).format('DD/MM/YYYY HH:mm:ss')}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            }
            </Container>
        </>
    )
}

export default MessageList