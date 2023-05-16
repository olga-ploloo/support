import React, {useState, useEffect} from "react";
import axios from "axios";
import * as constants from "../constatns/ticketConstans";
import {Link, useParams} from "react-router-dom";

const TicketsDetail = () => {
    const [ticket, setTicket] = useState("")
    const {id} = useParams()
    const [isOpen, setIsOpen] = useState(false);
    const handleClick = () => {
        setIsOpen(true);
    };
    const handleClose = () => {
        setIsOpen(false);
    };
    const getTicket = async () => {
        try {
            const response = await axios.get(`${constants.API_URL}/tickets/${id}`);
            setTicket(response.data);

        } catch (error) {
            console.log(error)
        }
    }

    useEffect(() => {
        getTicket();
    }, [])

    return (
        <div>
            <h2>Ticket Detail № {ticket.id}</h2> <h3>{ticket.status}</h3>
            <Link className="btn btn-info" to={`/${ticket.id}/update`}>Update status</Link>
            <div className="single-ticket-info">
                <p>{ticket.title}</p>
                The {ticket.author} reported:
                <p>{ticket.description}</p>
                {!isOpen && (
                    <img className="ticket-image" src={ticket.image} alt="ticket picture" onClick={handleClick}/>
                )}
                {isOpen && (
                    <div className="fullscreen-overlay" onClick={handleClose}>
                        <div className="fullscreen-image">
                            <img src={ticket.image} alt="full screen picture"/>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}
export default TicketsDetail;