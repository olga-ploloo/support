import logo from './logo.svg';
import './App.css';
import React, {createContext, useEffect, useState} from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import NavBar from "./components/navBar";
import TicketList from "./pages/ticketsList"
import Home from "./pages/home";
import {BrowserRouter as Router, Navigate, Route, Routes} from 'react-router-dom';
import TicketAdd from "./components/ticketAdd";
import TicketDetail from "./pages/ticketDetail";
import Login from "./pages/login";
import {clearAuthToken, setAuthToken} from "./services/authService";
import axios from "axios";
import * as constants from "./constatns/ticketConstans";
import OwnTickets from "./pages/ownTickets";
import Chat from "./pages/сhat";

export const LoginContext = createContext();

function App() {
    const token = localStorage.access;
    if (token) {
        setAuthToken(token);
    }
    const [loggedIn, setLoggedIn] = useState(localStorage.access ? true : false);

    async function refreshTokens() {
        if (localStorage.refresh && loggedIn) {
            await axios.post(`${constants.API_URL}/token/refresh/`, {refresh: localStorage.refresh})
                .then((response) => {
                    localStorage.access = response.data.access;
                    localStorage.refresh = response.data.refresh;
                    setLoggedIn(true);
                    return response;
                })
        }
    }

    function changeLoggedIn(value) {
        setLoggedIn(value);
        if (value === false) {
            clearAuthToken();
        }
    }

    useEffect(() => {
        const minute = 1000 * 60;
        refreshTokens()
        setInterval(refreshTokens, minute * 5)
    }, [])

    return <div className="App">
        <LoginContext.Provider value={[loggedIn, changeLoggedIn]}>
            <Router>
                <NavBar/>
                <Routes>
                    <Route exact path="/" element={loggedIn
                        ? <Home/>
                        : <Navigate to="/login" replace/>
                    }/>
                    <Route exact path="/tickets" element={<TicketList/>}/>
                    <Route exact path="/addTicket" element={<TicketAdd/>}/>
                    <Route exact path="/tickets/:id" element={<TicketDetail/>}/>
                    <Route exact path="/tickets/own_tickets" element={<OwnTickets/>}/>
                    <Route exac path="/login" element={<Login/>}/>
                    <Route exac path="/chat/:id" element={<Chat/>}/>
                </Routes>
            </Router>
        </LoginContext.Provider>
    </div>;
}

export default App;


