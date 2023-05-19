import React, {useState, useEffect} from "react";
import axios from "axios";
import * as constants from "../constatns/ticketConstans";
import {useParams} from "react-router-dom";
import TicketUpdate from "../components/ticketUpdate";
import AssignTicket from "../components/assignTicket";


const TicketsDetail = () => {
    const [ticket, setTicket] = useState("")
    const [ticketStatus, setTicketStatus] = useState(ticket.status)
    const {id} = useParams()
    const [isOpen, setIsOpen] = useState(false);

    useEffect(() => {
        getTicket();
    }, [])
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

    const updateTicket = async (status) => {
        try {
            const response = await axios.put(`${constants.API_URL}/tickets/${id}/`,
                {status: status});
            setTicketStatus(status)
        } catch (error) {
            console.log(error)
        }
    }

    const updateTicketInfo = () => {
        getTicket();
    }

console.log(ticket.assigned_ticket)
    return (
        <div>
            <h2>Ticket Detail № {ticket.id}</h2> <h3>{ticketStatus}</h3>
            {ticket.assigned_ticket.assigned_support ? (
                <td><TicketUpdate ticketId={ticket.id}
                                  updateTicket={updateTicket}/></td>
            ) : (
                <td><AssignTicket assignTicketId={ticket.assigned_ticket.id}
                                  update={updateTicketInfo}/>
                </td>
            )
            }
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