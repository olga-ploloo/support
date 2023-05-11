import {Table} from "reactstrap";
import TicketsService from '../../tiketsService';
import {Component} from "react";

const Service = new TicketsService();

const TableHeader = () => {
    return (
        <thead>
        <tr>
            <th>№</th>
            <th>Unique number</th>
            <th>Creation date</th>
            <th>Status</th>
            <th>Author</th>
            <th>Title</th>
            <th>Description</th>
        </tr>
        </thead>
    )
}

const TableBody = (props) => {
    const {tickets} = props
    return (
        <tbody>
        {!tickets || tickets.length <= 0 ? (
            <tr>
                <td colSpan="6" align="center">
                    <b>Пока ничего нет</b>
                </td>
            </tr>
        ) : tickets.map(student => (
                <tr key={tickets.pk}>
                    <td>#</td>
                    <td>{student.id}</td>
                    <td>{student.created_at}</td>
                    <td>{student.status}</td>
                    <td>{student.author}</td>
                    <td>{student.title}</td>
                    <td>{student.description}</td>
                </tr>
            )
        )}
        </tbody>
    )
}

class TicketsList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            tickets: [],
            nextPageURL: ''
        };
        this.nextPage = this.nextPage.bind(this);
    }

    componentDidMount() {
        const self = this;
        Service.getTickets().then(function (result) {
            self.setState({tickets: result.results, nextPageURL: result.next})
            // console.log(self)
        });
    }

    nextPage() {
        var self = this;
        // console.log(this.state.nextPageURL);
        Service.getTicketsByURL(this.state.nextPageURL).then((result) => {
            self.setState({tickets: result.results, nextPageURL: result.next})
        });
    }

    render() {
        // console.log(this.state)
        return (
            <div>
                <Table dark>
                    <TableHeader/>
                    <TableBody tickets={this.state.tickets}/>
                </Table>
                <button className="btn btn-primary" onClick={this.nextPage}>Next</button>
            </div>
        )
    }
}

export default TicketsList