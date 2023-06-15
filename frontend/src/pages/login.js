import React, {useContext, useState} from "react";
import '../LoginForm.css';
import {LoginContext} from '../App';
import axios from "axios";
import {useNavigate, useLocation, Link} from 'react-router-dom';
import * as constants from "../constatns/ticketConstans";
import {setAuthToken} from "../services/authService";
import {Alert, Label} from "reactstrap";

const Login = () => {
    const [loggedIn, setLoggedIn] = useContext(LoginContext)
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState(false);
    const navigate = useNavigate();
    const location = useLocation();

    const handleSubmit = async (e) => {
        e.preventDefault();
        let formField = new FormData()
        formField.append('email', email)
        formField.append('password', password)
        try {
            const response = await axios.post(
                `${constants.API_URL}/token/`, formField).then(response => {
                localStorage.setItem('access', response.data.access);
                localStorage.setItem('refresh', response.data.refresh);
                setAuthToken(response.data.access);
                setLoggedIn(true)
               navigate(
                    location?.state?.previousUrl
                        ? location.state.previousUrl
                        : '/'
                );
            });
        } catch (error) {
            setError(error.response.data.detail)
        }
    }

    return (
        <div className="login-container">
            <div className="login-left">
                <div className="login-header">
                    <h2 className="login-animation login-a1">
                        Welcome Back
                    </h2>
                    <h4 className="login-animation login-a2">
                        Log in to your account using email and password
                    </h4>
                </div>
                <form className="login-form" onSubmit={handleSubmit}>
                    <input
                        type="email"
                        name="email"
                        value={email}
                        className="login-form-field login-animation login-a3"
                        placeholder="Email Address"
                        required
                        onChange={(e) => setEmail(e.target.value)}/>
                    <input
                        type="password"
                        name="password"
                        value={password}
                        className="login-form-field login-animation login-a4"
                        placeholder="Password"
                        required
                        onChange={(e) => setPassword(e.target.value)}/>
                    {error &&
                        <Alert color="danger">{error}</Alert>}
                    <button type="submit" className="form-gradient-button login-animation login-a5">
                        LOGIN
                    </button>
                     <p className="login-animation login-a6">
                        <Link to={`/signup`}>Don't have an account?</Link>
                    </p>
                </form>
            </div>
            <div className="login-right"></div>
        </div>
    )
}
export default Login;