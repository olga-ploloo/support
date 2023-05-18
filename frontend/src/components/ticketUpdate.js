import React, {useState, useEffect} from "react";
import axios from "axios";
import * as constants from "../constatns/ticketConstans";
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';

const TicketUpdate = ({ticketId, updateTicket}) => {
    // console.log(props.ticketId)
    const [status, setStatus] = useState("")
    const [statusList, setStatusList] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const openModal = () => {
        setShowModal(true);
    };

    const closeModal = () => {
        setShowModal(false);
    };

    const getStatusList = async () => {
        try {
            const response = await axios.get(`${constants.API_URL}/ticket_statuses/`);
            setStatusList(response.data);
        } catch (error) {
            console.error(error);
        }
    };

    const getTicket = async () => {
        try {
            const response = await axios.get(`${constants.API_URL}/tickets/${ticketId}`);
            setStatus(response.data.status);
        } catch (error) {
            console.log(error)
        }
    }

    useEffect(() => {
        getTicket();
        getStatusList();
    }, [ticketId])


    return (
        <div>
            <button className="modal-btn confirm-btn" onClick={openModal}>Update status</button>
            <Modal
                className="modal"
                show={showModal}
                onHide={closeModal}
                backdrop="static"
                keyboard={false}
                centered>
                <Modal.Header closeButton>
                    <Modal.Title>
                        Update status
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                   <Row>
                    <label>
                        Select status for ticket №{ticketId}:
                        <Form.Select value={status} onChange={(e) => setStatus(e.target.value)}>
                            {statusList.map((status) => (
                                <option key={status[0]} value={status[0]}>{status[1]}</option>
                            ))}
                        </Form.Select>
                    </label>
                   </Row>
                </Modal.Body>
                <Modal.Footer>
                    <button className="modal-btn confirm-btn" onClick={(e) => {
                        e.preventDefault();
                        updateTicket(status);
                        closeModal();
                    }}>Update
                    </button>
                    <button className="modal-btn cancel-btn" onClick={closeModal}>
                        Close
                    </button>
                </Modal.Footer>
            </Modal>
        </div>
    )
}
export default TicketUpdate;