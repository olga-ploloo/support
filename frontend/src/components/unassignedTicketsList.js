import React, {useEffect, useState} from "react";
import axios from "axios";
import * as constants from "../constatns/ticketConstans";
import { Card, CardBody, CardTitle, ListGroup, ListGroupItem } from "reactstrap";
import moment from "moment/moment";
import {Link} from "react-router-dom";


const UnassignedTicketsList = () => {
    const [tickets, setTickets] = useState([]);

    const getUnassignedTickets = async () => {
        try {
            const response = await axios.get(`${constants.API_URL}/tickets/unassigned_tickets`);
            setTickets(response.data.results);
        } catch (error) {
            console.log(error)
        }
    };

    useEffect(() => {
        getUnassignedTickets();
    }, [])

    return (
        <>
            <Card className="home-card"
                  color="danger"
                  outline>
                <CardBody>
                    <CardTitle tag="h5">
                        Unassigned tickets:
                    </CardTitle>
                </CardBody>
                <ListGroup flush>
                    {!tickets || tickets.length <= 0 ? (
                        <ListGroupItem>
                            No unassigned tickets.
                        </ListGroupItem>
                    ) : (
                        tickets.slice(0, 5).map((ticket, index) => (
                            <Link to={`/tickets/${ticket.id}/`} className="card-btn-link">
                                <ListGroupItem>
                                    № {ticket.id} {moment(ticket.created_at).format('DD/MM/YYYY')}: {ticket.status}
                                </ListGroupItem>
                            </Link>
                        ))
                    )}
                </ListGroup>
            </Card>

        </>
    )

}

export default UnassignedTicketsList;
