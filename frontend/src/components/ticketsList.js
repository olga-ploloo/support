import moment from 'moment';
import React, {useState, useEffect} from "react";
import axios from "axios";
import * as constants from "../constatns/ticketConstans";
import ReactPaginate from 'react-paginate';
import { Link } from 'react-router-dom';

import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

const TableHeader = () => {
    return (
        <thead>
        <tr>
            <th>№</th>
            <th>Unique number</th>
            <th>Creation date</th>
            <th>Status</th>
            <th>Author</th>
            <th>Assignee</th>
            <th></th>
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
                    <b>Пока ничего нет</b>
                </td>
            </tr>
        ) : (
            tickets.map((ticket, index) => (
                <tr key={ticket.id}>
                    <td >{index+1}</td>
                    <td>{ticket.id}</td>
                    <td>{moment(ticket.created_at).format('DD/MM/YYYY HH:mm:ss')}</td>
                    <td>{ticket.status}</td>
                    <td>{ticket.author}</td>
                    <td>{ticket.assigned_ticket.assigned_support}</td>
                    <td><Link className="btn-more" to={`/${ticket.id}/`}>More</Link></td>
                </tr>
            ))
        )}
        </tbody>
    );
};

const TicketsList = () => {
    const [tickets, setTickets] = useState([]);
    const [pageCount, setPageCount] = useState(0);
    const [currentPage, setCurrentPage] = useState(0);

    const getTickets = async (pageNumber = 1) => {
        try {
            const response = await axios.get(`${constants.API_URL}/tickets/?page=${pageNumber}`);
            setTickets(response.data.results);
            setPageCount(Math.ceil(response.data.count / constants.PAGINATION_PAGE_SIZE))
        } catch (error) {
            console.log(error)
        }
    };

    useEffect(() => {
        getTickets();
    }, [])

    const handlePageChange = (selectedPage) => {
        const pageNumber = selectedPage.selected + 1;
        setCurrentPage(selectedPage.selected);
        getTickets(pageNumber);
    };

    return (
        <div>
            <table className="table TicketsList">
                <TableHeader/>
                <TableBody tickets={tickets}/>
            </table>
            <ReactPaginate
                pageCount={pageCount}
                initialPage={currentPage}
                onPageChange={handlePageChange}
                containerClassName="pagination"
                activeClassName="active"
            />
        </div>
    );
};
export default TicketsList;





