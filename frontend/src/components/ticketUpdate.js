import React, {useState, useEffect} from "react";
import {useNavigate, useParams} from 'react-router-dom';
import axios from "axios";
import * as constants from "../constatns/ticketConstans";

const TicketUpdate = () => {
    const [status, setStatus] = useState("")
    const [statusList, setStatusList] = useState([]);

    const navigate = useNavigate()
    const {id} = useParams()

    const getStatusList = async () => {
        try {
            const response = await axios.get(`${constants.API_URL}/ticket_statuses/`);
            setStatusList(response.data);
            console.log(response.data)
        } catch (error) {
            console.error(error);
        }
    };

    const getTicket = async () => {
        try {
            const response = await axios.get(`${constants.API_URL}/tickets/${id}`);
            setStatus(response.data.status);
        } catch (error) {
            console.log(error)
        }
    }
    const handleChangeStatus = (e) => {
    setStatus(e.target.value);
    console.log(status)
  };

     const updateTicketStatus = async () => {
        try {
            const response = await axios.put(`${constants.API_URL}/tickets/${id}`, { status: status });
            console.log(response.data)
            // setTicket(response.data);
        } catch (error) {
            console.log(error)
        }
    }

    useEffect(() => {
        getTicket();
        getStatusList();
    }, [])

// navigate('/home');
    return (
        <div className="form-group">
            <label>
                Status:
                <select value={status} onChange={handleChangeStatus}>
                    {statusList.map((status) => (
                        <option key={status[0]}>{status[1]}</option>
                    ))}
                </select>
            </label>
            <button onClick={updateTicketStatus}>Update</button>
        </div>

    )
}
export default TicketUpdate;