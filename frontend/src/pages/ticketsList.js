import moment from 'moment';
import React, {useEffect, useState} from "react";
import axios from "axios";
import * as constants from "../constatns/ticketConstans";
import ReactPaginate from 'react-paginate';
import {Link} from 'react-router-dom';
import {Table} from "reactstrap";
import AssignTicket from "../components/assignTicket";


const TicketsList = () => {
    const [tickets, setTickets] = useState([]);
    const [pageCount, setPageCount] = useState(0);
    const [currentPage, setCurrentPage] = useState(0);

    useEffect(() => {
        getTickets();
    }, [])

    const getTickets = async (pageNumber = 1) => {
        try {
            const response = await axios.get(`${constants.API_URL}/tickets/?page=${pageNumber}`);
            setTickets(response.data.results);
            setPageCount(Math.ceil(response.data.count / constants.PAGINATION_PAGE_SIZE))
        } catch (error) {
            console.log(error)
        }
    };

    const handlePageChange = (selectedPage) => {
        const pageNumber = selectedPage.selected + 1;
        setCurrentPage(selectedPage.selected);
        getTickets(pageNumber);
    };

    const updateTicketsList = (data) => {
        setTickets(prevState => {
            return prevState.map(ticket => {
                if (ticket.id === data.ticketId) {
                    return {
                        ...ticket, assigned_ticket:
                            {
                                ...ticket.assigned_ticket,
                                assigned_support: data.assigned_support,
                                is_assign: data.is_assign
                            }
                    };
                }
                return ticket;
            });
        });
    }

    const TableHeader = () => {
        return (
            <thead>
            <tr>
                <th className="narrow-column">№</th>
                <th className="narrow-column">Unique number</th>
                <th className="medium-column">Creation date</th>
                <th className="medium-column">Status</th>
                <th className="medium-column">Author</th>
                <th className="medium-column">Assignee</th>
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
                        <td>{ticket.author}</td>
                        {!ticket.assigned_ticket.assigned_support ? (
                            <td><AssignTicket assignTicketId={ticket.assigned_ticket.id}
                                              update={updateTicketsList}
                                              ticketId={ticket.id}/>
                            </td>
                        ) : (
                            <td>{ticket.assigned_ticket.assigned_support}</td>
                        )
                        }
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
        <div>
            <Table hover className="TicketsList">
                <TableHeader/>
                <TableBody tickets={tickets}/>
            </Table>
            <ReactPaginate
                pageCount={pageCount}
                initialPage={currentPage}
                onPageChange={handlePageChange}
                containerClassName="pagination"
                activeClassName="active"/>
        </div>
    );
};
export default TicketsList;





