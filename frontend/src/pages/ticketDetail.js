import React, {useState, useEffect} from "react";
import axios from "axios";
import * as constants from "../constatns/ticketConstans";
import {Link, useParams} from "react-router-dom";
import TicketUpdate from "../components/ticketUpdate";
import AssignTicket from "../components/assignTicket";
import {Container, Row, Col} from "reactstrap";


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
        <>
            <Container>
                <Row>
                    <Col><h2>Ticket Detail № {ticket.id}</h2></Col><Col><h3>{ticketStatus}</h3></Col>
                </Row>
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
                    <Row>
                        <Col>
                            <p>{ticket.title}</p>
                        </Col>
                    </Row>
                    <Row>
                        <Col>
                            The {ticket.author} reported:
                        </Col>
                        <Col>
                            {ticket.image && (
                                <p>Click on the image to enlarge</p>
                            )}
                        </Col>
                    </Row>
                    <Row>
                        <Col >
                            <p>{ticket.description}</p>
                        </Col>
                        <Col>
                            {ticket.image && !isOpen ? (
                                <img className="ticket-image" src={ticket.image} alt="ticket picture"
                                     onClick={handleClick}/>
                            ) : (
                                isOpen && (
                                    <div className="fullscreen-overlay" onClick={handleClose}>
                                        <div className="fullscreen-image">
                                            <img src={ticket.image} alt="full screen picture"/>
                                        </div>
                                    </div>
                                )
                            )}</Col>

                    </Row>
                </div>
                <div>
                    <Link className="modal-btn btn-more" to={`/tickets/${ticket.id}/`}>
                        Open chat
                    </Link>
                </div>
            </Container>
        </>
    )
}
export default TicketsDetail;