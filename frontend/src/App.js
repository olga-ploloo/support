import logo from './logo.svg';
import './App.css';
import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import NavBar from "./components/navBar";
import TicketList from "./components/ticketsList"
import Home from "./components/home";
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import TicketAdd from "./components/ticketAdd";
import TicketDetail from "./components/ticketDetail";
import LoginForm from "./components/loginForm";
import {setAuthToken} from "./services/authService";

function App() {
    const token = localStorage.getItem("access");
    if (token) {
        setAuthToken(token);
    }
    return <div className="App">
        <Router>
            <NavBar/>
            <Routes>
                <Route exact path="/" element={<Home/>}/>
                <Route exact path="/tickets" element={<TicketList/>}/>
                <Route exact path="/addTicket" element={<TicketAdd/>}/>
                <Route exact path="/tickets/:id" element={<TicketDetail/>}/>
                <Route exac path="/login" element={<LoginForm/>}/>
                {/*<Redirect to="/" />*/}
            </Routes>
        </Router>
    </div>;
}

export default App;


