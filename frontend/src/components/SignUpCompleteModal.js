import Modal from 'react-bootstrap/Modal';
import Row from "react-bootstrap/Row";
import React from "react";

const SignUpCompleteModal = ({email, showModal, closeModal}) => {
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
                            You have successfully created a new account.
                        </label>
                    </Row>
                    <Row>
                        <label>
                           Please check your email <b>{email}</b> for the activation link.
                        </label>
                    </Row>

                </Modal.Body>
                <Modal.Footer>
                </Modal.Footer>
            </Modal>
        </>
    )
}
export default SignUpCompleteModal