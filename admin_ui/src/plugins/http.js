import axios from "axios";
import Vue from 'vue'

function createInstance(){
    const API_URL = process.env.VUE_APP_EVENTS_API;
    const API_KEY = process.env.VUE_APP_EVENTS_API_KEY;    

    return axios.create({
        baseURL: API_URL,
        headers: {
            'x-api-key': API_KEY
        }
    });
}

export default {
    install () {
        Vue.prototype.$http = createInstance()
    }
};