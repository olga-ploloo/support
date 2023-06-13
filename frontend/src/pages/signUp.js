import React, {useContext, useState} from "react";
import '../LoginForm.css';
import {LoginContext} from '../App';
import axios from "axios";
import {useNavigate, useLocation} from 'react-router-dom';
import * as constants from "../constatns/ticketConstans";
import {setAuthToken} from "../services/authService";
import {TextField, Alert} from "@mui/material";
import {type} from "@testing-library/user-event/dist/type";

const SignUp = () => {
    const [input, setInput] = useState({
        username: '',
        email: '',
        password: '',
        password2: ''
    });
    const [error, setError] = useState({
        username: '',
        password: '',
        password2: ''
    })
    const navigate = useNavigate();
    const location = useLocation();

    const handleSubmit = async (e) => {
        console.log('handle submit')
        e.preventDefault();
        let formField = new FormData()
        formField.append('username', input.username)
        formField.append('email', input.email)
        formField.append('password', input.password)
        formField.append('password2', input.password2)
        try {
            const response = await axios.post(
                `${constants.API_URL}/auth/users/`, formField).then(response => {
                setAuthToken(response.data.access);
                // navigate(
                //      location?.state?.previousUrl
                //          ? location.state.previousUrl
                //          : '/'
                //  );
            });
        } catch (error) {
             // const {name, value} =
            console.log(typeof error.response.data)
            setError(error.response.data.detail)
        }
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

      let { name, value } = e.target;
      setError(prev => {
      const stateObj = { ...prev, [name]: "" };

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
  });}


    return (
        <div className="login-container">
            <div className="login-right"></div>
            <div className="login-left">
                <div className="login-header">
                    <h2 className="login-animation login-a1">
                        Create Your Account
                    </h2>
                    <h4 className="login-animation login-a2">

                    </h4>
                </div>
                <form className="sign-up-form" onSubmit={handleSubmit}>

                        <TextField
                            required
                            label="Name"
                            className="sign-up-input"
                            name="username"
                            type="username"
                            value={input.username}
                            onChange={onInputChange}
                            onBlur={validateInput}/>
                        {error.username && <span className='err'>{error.username}</span>}

                        <TextField
                            required
                            label="Email"
                            className="sign-up-input"
                            type="email"
                            name="email"
                            value={input.email}
                            onChange={onInputChange}
                            onBlur={validateInput}/>
                        {error.email && <span className='err'>{error.email}</span>}

                        <TextField
                            required
                            label="Password"
                            className="sign-up-input"
                            type="password"
                            name="password"
                            value={input.password}
                            onChange={onInputChange}
                            onBlur={validateInput}/>
                        {error.password && <span className='err'>{error.password}</span>}

                        <TextField
                            required
                            label="Confirm Password"
                            className="sign-up-input"
                            type="password"
                            name="password2"
                            value={input.password2}
                            onChange={onInputChange}
                            onBlur={validateInput}/>
                        {error.password2 && <span className='err'>{error.password2}</span>}

                        <button type="submit" className="login-animation login-a6">
                            Sign Up
                        </button>
                </form>
            </div>

        </div>
    )
}
export default SignUp;