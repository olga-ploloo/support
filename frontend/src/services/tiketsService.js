import http from "./http-common";
import axios from "axios";

// const getAll = () => {
//     return http.get("/tickets/");
// };

function getTickets() {
        const url = `${API_URL}/tickets/`;
        return axios.get(url).then(response => response.data);
    }


const get = id => {
    return http.get(`/tickets/${id}`);
};
const getTicketsByURL = url => {
    return http.get(`${url}`);
};

const create = data => {
    return http.post("/tickets", data);
};

const update = (id, data) => {
    return http.put(`/tickets/${id}`, data);
};

const remove = id => {
    return http.delete(`/tickets/${id}`);
};

export default {
    // getAll,
    get,
    create,
    update,
    remove,
    getTicketsByURL
};
