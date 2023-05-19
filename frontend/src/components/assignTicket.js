import React, {useEffect, useState} from "react";
import axios from "axios";
import * as constants from "../constatns/ticketConstans";
import {Card, CardBody, CardTitle, ListGroup, ListGroupItem} from "reactstrap";
import {Link} from "react-router-dom";
import moment from "moment";

const AssignTicket = ({assignTicketId, update}) => {
    const assignTicket = async (assignTicketId) => {
        try {
            const response = await axios.put(`${constants.API_URL}/assign_ticket/${assignTicketId}/`);
            update();
        } catch (error) {
            console.error(error);
        }
    }

    return (
        <>
            <button className="modal-btn confirm-btn" onClick={(e) => {
                e.preventDefault();
                assignTicket(assignTicketId);
            }}>
                Assign me
            </button>
        </>
    )
}

export default AssignTicket;