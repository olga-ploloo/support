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
import TicketUpdate from "./components/ticketUpdate";


function App() {
    return <div className="App">
        <Router>
            <NavBar/>
            <Routes>
                <Route exact path="/" element={<TicketList/>}/>
                <Route exact path="/addTicket" element={<TicketAdd/>}/>
                <Route exact path="/:id" element={<TicketDetail/>}/>
                <Route exact path="/:id/update" element={<TicketUpdate/>}/>

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

