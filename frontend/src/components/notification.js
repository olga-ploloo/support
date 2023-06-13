import React, {useState, useEffect} from 'react';
import * as constants from "../constatns/ticketConstans";
import NotificationsNoneIcon from '@mui/icons-material/NotificationsNone';
import NotificationsActiveIcon from '@mui/icons-material/NotificationsActive';
import useWebSocket from "react-use-websocket";

const Notification = () => {
    const [message, setMessage] = useState('');
    const socketUrl = `ws://${constants.HOST}/ws/notifications/`;
    const {lastMessage, readyState} = useWebSocket(socketUrl)


    // const notificationSocket = useWebSocket(socketUrl, {
    //     onOpen: () => console.log('Connected'),
    //     onClose: () => console.log('Disconnected'),
    //     shouldReconnect: (closeEvent) => true,
    //     onError: (error) => console.log("WebSocket encountered an error: " + error.text),
    //     onMessage: (event) => {
    //         console.log('get notification')
    //         const data = JSON.parse(event.data);
    //         console.log(data)
    //         setMessage(data.message);
    //     }
    // });


    return (
        <div>
            {message ? (<NotificationsActiveIcon/>) : (<NotificationsNoneIcon/>)}
            {readyState === 1 && lastMessage && <span>{lastMessage.data}</span>}
            {/*{message && <span>{message}</span>}*/}
        </div>
    );
};

export default Notification;