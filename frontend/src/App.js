import logo from './logo.svg';
import './App.css';
import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import Header from "./components/header";
import TicketList from "./components/ticketsList"
import Home from "./components/home";

function App() {
  return <div className="App">
  <Header/>
<TicketList/>
    </div>;
}

// function App() {
//     return (
//         <Fragment>
//             <Header/>
//             <Home/>
//         </Fragment>
//     );
// }

export default App;

