import logo from './logo.svg';
import './App.css';
import {Fragment} from "react";
import Header from "../header/header";
import TicketList from "../ticketsList/ticketsList"
import Home from "../home/home";

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

