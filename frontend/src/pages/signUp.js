import React, {useState} from "react";
import '../LoginForm.css';
import axios from "axios";
import {useNavigate} from 'react-router-dom';
import * as constants from "../constatns/ticketConstans";
import { TextField, CircularProgress } from "@mui/material";
import {Alert} from "reactstrap";
import SignUpCompleteModal from "../components/SignUpCompleteModal";

const SignUp = () => {
    const [input, setInput] = useState({
        username: '',
        email: '',
        password: '',
        password2: ''
    });
    const [error, setError] = useState({
        username: '',
        email: '',
        password: '',
        password2: ''
    })
    const navigate = useNavigate();
    const [isSubmitted, setIsSubmitted] = useState(false);
    const [loading, setLoading] = useState(false);
    const [newUserEmail, setNewUserEmail] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        let formField = new FormData()
        formField.append('username', input.username)
        formField.append('email', input.email)
        formField.append('password', input.password)
        formField.append('password2', input.password2)
        try {
            const response = await axios.post(
                `${constants.API_URL}/auth/users/`, formField);
            setIsSubmitted(true)
            setNewUserEmail(response.data.email)
            console.log(response.data.email)
        } catch (error) {
            const errorFields = (Object.keys(error.response.data))
            errorFields.map((field) => (
            setError(prev => ({
                    ...prev,
                    [field]: error.response.data[field]
                })
            )))
        }
        setLoading(false)
    }

    const onInputChange = e => {

        const {name, value} = e.target;
        setInput(prev => ({
            ...prev,
            [name]: value
        }));
        validateInput(e);
    }

    const validateInput = e => {
        let {name, value} = e.target;
        setError(prev => {
            const stateObj = {...prev, [name]: ""};
            switch (name) {
                case "username":
                    if (!value) {
                        stateObj[name] = "Please enter Username.";
                    }
                    break;

                case "password":
                    if (!value) {
                        stateObj[name] = "Please enter Password.";
                    } else if (input.password2 && value !== input.password2) {
                        stateObj["password2"] = "Password and Confirm Password does not match.";
                    } else {
                        stateObj["password2"] = input.password2 ? "" : error.password2;
                    }
                    break;

                case "password2":
                    if (!value) {
                        stateObj[name] = "Please enter Confirm Password.";
                    } else if (input.password && value !== input.password) {
                        stateObj[name] = "Password and Confirm Password does not match.";
                    }
                    break;

                default:
                    break;
            }

            return stateObj;
        });
    }

    const closeModal = () => {
        setIsSubmitted(false)
        navigate("/login")
    };

    return (
        <div className="login-container">
            <div className="login-right"></div>
            <div className="login-left">
                <div className="login-header">
                    <h2 className="login-animation login-a1">
                        Create Your Account
                    </h2>
                    <h4 className="login-animation login-a1">
                        Fill in the form
                    </h4>
                </div>
                <form className="sign-up-form"  onSubmit={handleSubmit}>
                    <TextField
                        required
                        label="Name"
                        className="login-a2"
                        margin="dense"
                        name="username"
                        type="username"
                        value={input.username}
                        onChange={onInputChange}
                        onBlur={validateInput}/>
                    {error.username && <Alert color="danger">{error.username}</Alert>}
                    <TextField
                        required
                        label="Email"
                        className="login-a3"
                        margin="dense"
                        type="email"
                        name="email"
                        value={input.email}
                        onChange={onInputChange}
                        onBlur={validateInput}/>
                    {error.email && <Alert color="danger">{error.email}</Alert>}

                    <TextField
                        required
                        label="Password"
                        classeame="login-a4"
                        margin="dense"
                        type="password"
                        name="password"
                        value={input.password}
                        onChange={onInputChange}
                        onBlur={validateInput}/>
                    {error.password && <Alert color="danger">{error.password}</Alert>}

                    <TextField
                        required
                        label="Confirm Password"
                        className="login-a5"
                        margin="dense"
                        type="password"
                        name="password2"
                        value={input.password2}
                        onChange={onInputChange}
                        onBlur={validateInput}/>
                    {error.password2 && <Alert color="danger">{error.password2}</Alert>}

                    <button type="submit" className="form-gradient-button login-animation login-a6">
                        {loading ? (
                            <CircularProgress color="primary"
                                              size="30"/>
                        ) : (
                            <span>Sign Up</span>)}
                    </button>
                </form>
                {isSubmitted && (
                    <SignUpCompleteModal email={newUserEmail}
                                         showModal={isSubmitted}
                                         closeModal={closeModal}/>
                )}
            </div>
        </div>
    )
}
export default SignUp;