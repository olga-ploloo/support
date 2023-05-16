import logo from './logo.svg';
import './App.css';
import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import NavBar from "./components/navBar";
import TicketList from "./components/ticketsList"
import Home from "./components/home";
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import AddTicket from "./components/addTicket";
import TicketDetail from "./components/ticketDetail";


function App() {
    return <div className="App">
        <Router>
            <NavBar/>
            <Routes>
                <Route exact path="/" element={<TicketList/>}/>
                <Route exact path="/addTicket" element={<AddTicket/>}/>
                <Route exact path="/:id" element={<TicketDetail/>}/>

            </Routes>
        </Router>
        {/*  <NavBar/>*/}
        {/*<TicketList/>*/}
    </div>;
}

// function App() {
//     return (
//         <Fragment>
//             <NavBar/>
//             <Home/>
//         </Fragment>
//     );
// }

export default App;

