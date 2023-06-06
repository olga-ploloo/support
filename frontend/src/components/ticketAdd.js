import React, {useState} from "react";
import {Form, FormGroup, Label, Col, Input, Button} from "reactstrap";
import axios from "axios";
import {useNavigate} from 'react-router-dom';
import * as constants from "../constatns/ticketConstans";
import ActionCompleteModal from "./modal";


const TicketAdd = () => {
    const [title, setTitle] = useState("")
    const [description, setDescription] = useState("")
    const [image, setImage] = useState(null)
    const [isSubmitted, setIsSubmitted] = useState(false);
    const [newTicketId, setNewTicketId] = useState("");
    const closeModal = () => {
        setIsSubmitted(false)
        navigate("/")
    };
    const navigate = useNavigate();

    const addTicket = async (e) => {
        e.preventDefault();
        let formField = new FormData()
        formField.append('title', title)
        formField.append('description', description)
        if (image !== null) {
            formField.append('image', image)
        }
        try {
            await axios.post(
                `${constants.API_URL}/tickets/`, formField).then(response => {
                setNewTicketId(response.data.id)
                setIsSubmitted(true)
            });
        } catch (error) {
            console.log(error)
        }
    }

    return (
        <div className="container">
            <h1>Add Ticket</h1>
            <Form onSubmit={addTicket}>
                <FormGroup row>
                    <Label for="title" sm={2}>
                        Titile
                    </Label>
                    <Col sm={10}>
                        <Input
                            id="title"
                            name="title"
                            value={title}
                            placeholder="Add a concise description of the problem"
                            type="text"
                            onChange={(e) => setTitle(e.target.value)}/>
                    </Col>
                </FormGroup>
                <FormGroup row>
                    <Label for="description" sm={2}>
                        Description
                    </Label>
                    <Col sm={10}>
                        <Input
                            id="description"
                            name="description"
                            value={description}
                            placeholder="Add a full description with the details of your problem"
                            type="textarea"
                            required
                            onChange={(e) => setDescription(e.target.value)}/>
                    </Col>
                </FormGroup>
                <FormGroup row>
                    <Label for="file" sm={2}>
                        Attach photo/screenshot
                    </Label>
                    <Col sm={10}>
                        <Input
                            id="file"
                            name="file"
                            type="file"
                            src={image}
                            onChange={(e) => setImage(e.target.files[0])}/>
                        <img src={image}/>
                    </Col>
                </FormGroup>
                <FormGroup check row>
                    <Col sm={{
                        offset: 1,
                        size: 10
                    }}>
                        <Button type="submit" className="modal-btn confirm-btn">
                            Submit
                        </Button>
                    </Col>
                </FormGroup>
            </Form>
            {isSubmitted && (
                <ActionCompleteModal ticketId={newTicketId}
                                     showModal={isSubmitted}
                                     closeModal={closeModal}/>)}
        </div>

    )
}
export default TicketAdd;