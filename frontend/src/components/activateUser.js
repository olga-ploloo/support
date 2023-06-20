import {useEffect} from 'react';
import {useNavigate, useLocation} from 'react-router-dom';
import axios from 'axios';
import * as constants from "../constatns/ticketConstans";

function ActivateUser() {
    const navigate = useNavigate();
    const location = useLocation();
    const searchParams = new URLSearchParams(location.search);
    const uid = searchParams.get('uid');
    const token = searchParams.get('token');

    useEffect(() => {
        activateUser()
    }, [location.search]);

    const activateUser = async () => {
        try {
            const response = await axios.post(`${constants.API_URL}/auth/users/activation/`, {uid, token});
            navigate('/login');
        } catch (error) {
            console.log(error)
        }
    };

    return (
        <>
            <p>Activating your account...</p>
        </>
    );
}

export default ActivateUser;