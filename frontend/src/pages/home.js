import React from "react";
import { Row, Col } from "reactstrap";
import UnassignedTicketsList from "../components/unassignedTicketsList";
import OwnTicketsCard from "../components/ownTicketsCard";
import LastTicketsCard from "../components/lastTicketsCard";

const Home = () => {

    return (
        <>
            <h3>Welcome</h3>
            <div className="home-container">
                <Row>
                    <Col>
                        <OwnTicketsCard/>
                    </Col>
                </Row>
                <Row>
                    <Col>
                        <LastTicketsCard/>
                    </Col>
                    <Col>
                        <UnassignedTicketsList/>
                    </Col>

                </Row>
            </div>
        </>
    )
}

export default Home;