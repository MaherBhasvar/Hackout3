import Axios from 'axios';
import {
    SHOW_JOURNEY,
    GET_ERRORS,
    SAVE_DATA,
    START_LOCATION,
    CLEAR_REDUCERS
} from './types';

//axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

const axios = Axios.create({
    baseURL: 'http://localhost:54545/',
    timeout: 2000000,
    headers: {
        // 'X-Custom-Header': 'foobar',
        'Content-Type': 'application/x-www-form-urlencoded',
        ['Content-Type']: 'application/json;charset=utf-8',
        ['Access-Control-Allow-Origin']: '*',
    }
});


export const clearReducers = () => dispatch => {
    dispatch({
        type: CLEAR_REDUCERS,
    })
}

export const sendLocations = data => dispatch => {

    axios.post('/locate', data)
        .then(res => {
            console.log("send locations", res.data)
        })
        .catch(err => {
            console.log(err)
        })
}

export const getLocation = data => dispatch => {
    axios.post('/locate1', data)
        .then(res => {
            console.log("lat,long", res.data)
            dispatch({
                type: START_LOCATION,
                payload: res.data
            })
        })
        .catch(err => {
            console.log(err)
        })
}


export const saveData = (data) => dispatch => {
    dispatch({
        type: SAVE_DATA,
        payload: data
    })
}

export const submitData = (data, history) => dispatch => {

    // axios.get('/')
    //     .then(res => {
    //         console.log(res.data)
    //         dispatch({
    //             type: SHOW_JOURNEY,
    //             payload: res.data,
    //         })
    //     })
    //     .catch(err => {
    //         console.log(err)
    //         dispatch({
    //             type: GET_ERRORS,
    //             payload: err.response.data
    //         })
    //     })
    if (data.primaryMode == "Bus") {
        axios.post('/bus', data)
            .then(res => {
                console.log("actions", res.data)
                dispatch({
                    type: SHOW_JOURNEY,
                    payload: res.data,
                })

                history.push('/result')
            })
            .catch(err => {
                dispatch({
                    type: GET_ERRORS,
                    //payload: err.response.data
                })
            })
    } else if (data.primaryMode == "Flight") {
        axios.post('/flight', data)
            .then(res => {
                console.log("actions", res.data)
                dispatch({
                    type: SHOW_JOURNEY,
                    payload: res.data,
                })

                history.push('/result')
            })
            .catch(err => {
                dispatch({
                    type: GET_ERRORS,
                    //payload: err.response.data
                })
            })
    } else {
        axios.post('/flight', data)
            .then(res => {
                console.log("actions", res.data)
                dispatch({
                    type: SHOW_JOURNEY,
                    payload: res.data,
                })

                history.push('/result')
            })
            .catch(err => {
                dispatch({
                    type: GET_ERRORS,
                    //payload: err.response.data
                })
            })
    }


}


// export const animalRegistration = (data, history) => dispatch => {
//     axios.post('/api/animalRegistration', data)
//         .then(res => {
//             //Lock AR
//             dispatch({
//                 type: LOCK_AR,
//             });
//             dispatch({
//                 type: AR,
//                 payload: res.data,
//             });
//             //
//             history.push('/animalInsemination');
//         })
//         .catch(err =>
//             dispatch({
//                 type: GET_ERRORS,
//                 payload: err.response.data
//             })
//         );
// }