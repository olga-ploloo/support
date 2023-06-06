import React from "react";
import axios from "axios";
import * as constants from "../constatns/ticketConstans";


const AssignTicket = ({assignTicketId, update, ticketId}) => {
    const assignTicket = async (assignTicketId) => {
        try {
            const response = await axios.put(`${constants.API_URL}/assign_ticket/${assignTicketId}/`);
            response.data.ticketId = ticketId
            update(response.data);
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