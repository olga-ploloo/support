import axios from "axios";

export default axios({
  baseURL: "http://0.0.0.0:8000",
  headers: {
    "Content-type": "application/json"
  }
});