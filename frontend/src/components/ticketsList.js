import {Table} from "reactstrap";
import React, {useState, useEffect} from "react";
import axios from "axios";
import {API_URL} from "../constatns/ticketConstans";

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
    const [nextPageURL, setNextPageURL] = useState("");


    useEffect(() => {
        const getTickets = async () =>{
            try {
                const response = await axios.get(`${API_URL}/tickets/`);
                console.log(response.data)
                setTickets(response.data.results);
                setNextPageURL(response.data.next);
            }
            catch (error){
                console.log(error)
            }
        };
        getTickets();
    }, [])

    const nextPage = async () => {
        const response = await axios.get(nextPageURL);
        setTickets(response.data.results);
        setNextPageURL(response.data.next);
    };

    return (
        <div>
            <table className="table TicketsList">
                <TableHeader/>
                <TableBody tickets={tickets}/>
            </table>
            <button className="btn btn-primary" onClick={nextPage}>
                Next
            </button>
        </div>
    );
};

export default TicketsList;





