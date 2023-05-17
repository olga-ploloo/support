import Modal from 'react-bootstrap/Modal';
import Row from "react-bootstrap/Row";
import Form from "react-bootstrap/Form";
import React from "react";

const ActionCompleteModal = ({ticketId, showModal, closeModal}) => {
    return (
        <>
            <Modal
                show={showModal}
                className="modal"
                backdrop="static"
                keyboard={false}
                onHide={closeModal}
                centered>
                <Modal.Header closeButton>
                    <Modal.Title>
                        Creation completed.
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Row>
                        <label>
                            You have successfully created a ticket <b>№ {ticketId}</b>.
                        </label>
                    </Row>
                    <Row>
                        <label>
                            The support team will reply to it shortly.
                        </label>
                    </Row>

                </Modal.Body>
                <Modal.Footer>

                </Modal.Footer>
            </Modal>
        </>
    )
}
export default ActionCompleteModal