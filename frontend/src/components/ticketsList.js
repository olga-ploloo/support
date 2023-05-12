import {Table} from "reactstrap";
import React, {useState, useEffect} from "react";
import axios from "axios";
import * as constants from "../constatns/ticketConstans";
import ReactPaginate from 'react-paginate';

const TableHeader = () => {
    return (
        <thead>
        <tr>
            <th>№</th>
            <th>Unique number</th>
            <th>Creation date</th>
            <th>Status</th>
            <th>Author</th>
            <th>Title</th>
            <th>Description</th>
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
                <tr>
                    <td>index</td>
                    <td>{ticket.id}</td>
                    <td>{ticket.created_at}</td>
                    <td>{ticket.status}</td>
                    <td>{ticket.author}</td>
                    <td>{ticket.title}</td>
                    <td>{ticket.description}</td>
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
            console.log(response.data)
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





