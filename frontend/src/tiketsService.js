import axios from 'axios';

const API_URL = 'http://0.0.0.0:8000';

export default class TicketsService {

    constructor() {
    }

    getTickets() {
        const url = `${API_URL}/tickets/`;
        return axios.get(url).then(response => response.data);
    }

    getTicketsByURL(link) {
        const url = `${link}`;
        return axios.get(url).then(response => response.data);
    }

    getTicket(pk) {
        const url = `${API_URL}/tickets/${pk}`;
        return axios.get(url).then(response => response.data);
    }

    deleteTicket(pk) {
        const url = `${API_URL}/tickets/${pk}`;
        return axios.delete(url);
    }

    createTicket(customer) {
        const url = `${API_URL}/tickets/`;
        return axios.post(url, customer);
    }

    updateTicket(pk) {
        const url = `${API_URL}/tickets/${pk}`;
        return axios.put(url);
    }
}