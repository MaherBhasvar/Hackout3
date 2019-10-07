import Axios from 'axios';
import {
    CURRENT_LOCATION,
    GET_ERRORS,
} from './types';

const axios = Axios.create({
    baseURL: 'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyB1U9ZSkPklUAWt7WTQQT9E_T1qLfWGHSQ',
    timeout: 1000,
    headers: {
        // 'X-Custom-Header': 'foobar',
        'Content-Type': 'application/x-www-form-urlencoded',
        // ['Content-Type']: 'application/json;charset=utf-8',
        // ['Access-Control-Allow-Origin']: '*',
    }
});

export const getLocation = (data) => dispatch => {
    axios.post('/', data)
        .then(res => {
            console.log(res.data)
        })
        .catch(err => {
            console.log(err)
        })

}


