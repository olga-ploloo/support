import {Card, CardBody, CardTitle, ListGroup, ListGroupItem} from "reactstrap";
import {Link, Navigate} from "react-router-dom";
import moment from "moment/moment";
import React, {useContext, useEffect, useState} from "react";
import {useNavigate} from 'react-router-dom';
import axios from "axios";
import * as constants from "../constatns/ticketConstans";
import {LoginContext} from "../App";

const LastTicketsCard = () => {
    const [tickets, setTickets] = useState([]);
    const [loggedIn, setLoggedIn] = useContext(LoginContext);
    const navigate = useNavigate();

    useEffect(() => {
        getTickets();
    }, [])

    const getTickets = async () => {
        try {
            const response = await axios.get(`${constants.API_URL}/tickets/`);
            setTickets(response.data.results);
        } catch (error) {
            console.log(error)
            if (error.response.status === 401) {
                setLoggedIn(false);
                navigate('/login');
            }
        }
    };

    return (
        <>
            <Card className="home-card last-added">
                <CardBody>
                    <CardTitle tag="h5">
                        Last added tickets:
                    </CardTitle>
                </CardBody>
                <ListGroup flush>
                    {!tickets || tickets.length <= 0 ? (
                        <ListGroupItem>
                            You don't have any tickets.
                        </ListGroupItem>
                    ) : (
                        tickets.slice(0, 5).map((ticket, index) => (
                            <Link to={`/tickets/${ticket.id}/`} className="card-btn-link" key={ticket.id}>
                                <ListGroupItem>
                                    № {ticket.id} {moment(ticket.created_at).format('DD/MM/YYYY')}: {ticket.status}
                                </ListGroupItem>
                            </Link>
                        ))
                    )}
                </ListGroup>
                <CardBody>
                    <Link to="/tickets/" className="card-btn-link">
                        See all
                    </Link>
                </CardBody>
            </Card>
        </>
    )
}

export default LastTicketsCard