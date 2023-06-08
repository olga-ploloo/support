import {Col, Row, Container, Button} from "reactstrap";
import React from "react";
import moment from "moment/moment";

const MessageList = ({messageHistory, currentUserId, loadMoreMessages, hasMore}) => {
    const isCurrentUserMessage = (message) => {
        return message.author_id === currentUserId;
    };

    return (
        <>
            {messageHistory &&
                <Container className="chat-message-list">
                    {hasMore && (
                        <div className="load-more-button">
                            <Button
                                className="modal-btn confirm-btn"
                                onClick={loadMoreMessages}>
                                Load More
                            </Button>
                        </div>
                    )}
                    {messageHistory.slice().reverse().map((message) => (
                        <div className="message" key={message.id}>
                            <div
                                className={isCurrentUserMessage(message) ? "chat-message-row user-message" : "chat-message-row"}>
                                <div>
                                    {!isCurrentUserMessage(message) ? message.author + ":" : ""}
                                </div>
                                <div
                                    className={isCurrentUserMessage(message) ? "chat-message user-message" : "chat-message"}>
                                    <div className="chat-message-text"> {message.message}</div>
                                    <span
                                        className="chat-message-time">{moment(message.created_at).format('HH:mm')}</span>
                                </div>
                                <div className="chat-message-status">
                                    ok
                                </div>
                                <div className="chat-message-spacer">
                                </div>

                            </div>
                        </div>
                    ))}
                </Container>
            }
        </>
    )
}

export default MessageList