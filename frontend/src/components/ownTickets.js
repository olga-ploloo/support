import React, {useEffect, useState} from "react";
import axios from "axios";
import * as constants from "../constatns/ticketConstans";
import {Table} from "reactstrap";
import moment from "moment/moment";
import {Link} from "react-router-dom";


const OwnTickets = () => {
    const [tickets, setTickets] = useState([]);
    const getOwnTickets = async () => {
        try {
            const response = await axios.get(`${constants.API_URL}/tickets/support_own_tickets`);
            setTickets(response.data.results);
        } catch (error) {
            console.log(error)
        }
    };

    useEffect(() => {
        getOwnTickets();
    }, [])

    const TableHeader = () => {
        return (
            <thead>
            <tr>
                <th className="narrow-column">№</th>
                <th className="narrow-column">Unique number</th>
                <th className="medium-column">Creation date</th>
                <th className="medium-column">Status</th>
                <th className="medium-column"></th>
            </tr>
            </thead>
        );
    };

    const TableBody = ({tickets}) => {
        return (
            <tbody>
            {!tickets || tickets.length <= 0 ? (
                <tr>
                    <td colSpan="6" align="center">
                        <b>There is nothing yet.</b>
                    </td>
                </tr>
            ) : (
                tickets.map((ticket, index) => (
                    <tr key={ticket.id}>
                        <td>{index + 1}</td>
                        <td>{ticket.id}</td>
                        <td>{moment(ticket.created_at).format('DD/MM/YYYY HH:mm:ss')}</td>
                        <td>{ticket.status}</td>
                        <td className="details-col">
                            <Link className="modal-btn btn-more" to={`/tickets/${ticket.id}/`}>
                                More details
                            </Link>
                        </td>
                    </tr>
                ))
            )}
            </tbody>
        );
    };
    return (
        <>
            <h3>There are you tickets.</h3>
            <Table hover className="TicketsList">
                <TableHeader/>
                <TableBody tickets={tickets}/>
            </Table>
        </>
    )

}

export default OwnTickets;
