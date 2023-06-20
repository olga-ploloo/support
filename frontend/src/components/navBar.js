import React, {useEffect, useContext} from "react";
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import {useLocation} from "react-router-dom";
import {LoginContext} from '../App';
import Notification from "./notification";

const NavBar = () => {
    const location = useLocation();
    const isLoginPage = location.pathname === '/login';
    const isSignUpPage = location.pathname === '/signup'
    const [loggedIn, setLoggedIn] = useContext(LoginContext);

    useEffect(() => {
    }, [location.pathname, loggedIn]);

    if (!isLoginPage && !isSignUpPage) {
        return (
            <div>
                <Navbar bg="light" expand="lg">
                    <Container>
                        <Navbar.Brand href="/">Home</Navbar.Brand>
                        <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                        <Navbar.Collapse id="basic-navbar-nav">
                            <Nav className="me-auto">
                                <Nav.Link href="/tickets">Tickets list</Nav.Link>
                                <Nav.Link href="/addTicket">Add ticket</Nav.Link>
                                {loggedIn ? (
                                    <Nav.Link
                                        href={'/login'}
                                        onClick={() => {
                                            setLoggedIn(false);
                                        }}>
                                        Logout
                                    </Nav.Link>
                                ) : (
                                    <Nav.Link
                                        href={'/login'}>
                                        Login
                                    </Nav.Link>
                                )}
                                <Nav><Notification/></Nav>
                            </Nav>
                        </Navbar.Collapse>
                    </Container>
                </Navbar>
            </div>
        )
    }
}

export default NavBar;