import {Container, Row, Col, Card, CardBody, CardTitle, CardText, ListGroup, ListGroupItem, CardLink} from "reactstrap";
// import ListStudents from "../appListStudents/ListStudents";
import axios from "axios";
import React, {useEffect, useState} from "react";
import * as constants from "../constatns/ticketConstans";
import TicketUpdate from "./ticketUpdate";
import OwnTickets from "./ownTickets";
import {Link} from "react-router-dom";
import moment from "moment";
// import ModalStudent from "../appModalStudent/ModalStudent";
// import {API_URL} from "../../index";

const Home = () => {
    const [ownTickets, setOwnTickets] = useState([]);

    useEffect(() => {
        getOwnTickets();
    }, [])

    const getOwnTickets = async () => {
        try {
            const response = await axios.get(`${constants.API_URL}/tickets/support_own_tickets`);
            setOwnTickets(response.data.results);
        } catch (error) {
            console.log(error)
        }
    };


    return (<>
            <h3>Welcome</h3>
            <div className="home-container">
                <Card
                    style={{width: '18rem'}}>
                    <CardBody>
                        <CardTitle tag="h5">
                            You last tickets:
                        </CardTitle>
                    </CardBody>
                    <ListGroup flush>
                        {!ownTickets || ownTickets.length <= 0 ? (
                            <ListGroupItem>
                                You don't have any tickets.
                            </ListGroupItem>
                        ) : (
                            ownTickets.slice(0, 3).map((ticket, index) => (
                                <Link to={`/tickets/${ticket.id}/`} className="card-btn-link">
                                    <ListGroupItem>
                                        № {ticket.id} {moment(ticket.created_at).format('DD/MM/YYYY')}: {ticket.status}
                                    </ListGroupItem>
                                </Link>

                            ))
                        )}
                    </ListGroup>
                    <CardBody>
                        <Link to="/tickets/own_tickets/" className="card-btn-link">
                            See all
                        </Link>

                    </CardBody>
                </Card>
                <Card style={{width: '18rem'}}>
                    <CardBody>
                        <CardTitle tag="h5">
                            You last tickets:
                        </CardTitle>
                    </CardBody>
                    <ListGroup flush>
                        {!ownTickets || ownTickets.length <= 0 ? (
                            <ListGroupItem>
                                You don't have any tickets.
                            </ListGroupItem>
                        ) : (
                            ownTickets.slice(0, 3).map((ticket, index) => (
                                <Link to={`/tickets/${ticket.id}/`} className="card-btn-link">
                                    <ListGroupItem>
                                        № {ticket.id} {moment(ticket.created_at).format('DD/MM/YYYY')}: {ticket.status}
                                    </ListGroupItem>
                                </Link>

                            ))
                        )}
                    </ListGroup>
                    <CardBody>
                        <Link to="/tickets/own_tickets/" className="card-btn-link">
                            See all
                        </Link>

                    </CardBody>
                </Card>
            </div>
        </>
    )

}

export default Home;