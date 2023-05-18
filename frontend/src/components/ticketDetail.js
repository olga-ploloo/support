import React, {useState, useEffect} from "react";
import axios from "axios";
import * as constants from "../constatns/ticketConstans";
import {Link, useParams} from "react-router-dom";
import TicketUpdate from "./ticketUpdate";


const TicketsDetail = () => {
    const [ticket, setTicket] = useState("")
    const [ticketStatus, setTicketStatus] = useState(ticket.status)
    const {id} = useParams()
    const [isOpen, setIsOpen] = useState(false);
    const [isImage, setIsImage] = useState(false);
    console.log(ticket.image)
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
            setTicketStatus(response.data.status);
        } catch (error) {
            console.log(error)
        }
    }

    async function updateTicket(status) {
        try {
            const response = await axios.put(`${constants.API_URL}/tickets/${id}/`,
                {status: status});
            setTicketStatus(status)
        } catch (error) {
            console.log(error)
        }
    }

    useEffect(() => {
        getTicket();
    }, [])

    return (
        <div>
            <h2>Ticket Detail № {ticket.id}</h2> <h3>{ticketStatus}</h3>
            <TicketUpdate ticketId={ticket.id}
                          updateTicket={updateTicket}/>
            <div className="single-ticket-info">
                <p>{ticket.title}</p>
                The {ticket.author} reported:
                <p>{ticket.description}</p>
                {ticket.image && !isOpen ? (
                    <img className="ticket-image" src={ticket.image} alt="ticket picture" onClick={handleClick}/>
                ) : (
                    isOpen && (
                        <div className="fullscreen-overlay" onClick={handleClose}>
                            <div className="fullscreen-image">
                                <img src={ticket.image} alt="full screen picture"/>
                            </div>
                        </div>
                    )
                )}
            </div>
        </div>
    )
}
export default TicketsDetail;