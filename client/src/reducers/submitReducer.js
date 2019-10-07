import { SHOW_JOURNEY, SAVE_DATA, START_LOCATION, CLEAR_REDUCERS } from '../actions/types'

const initialState = {
    newData: null,
    saveData: null,
    startLat: null,
    startLng: null,
    end: null
}

export default function (state = initialState, action) {
    switch (action.type) {
        case SHOW_JOURNEY:
            return {
                ...state,
                newData: action.payload,
            }
        case SAVE_DATA:
            return {
                ...state,
                saveData: action.payload
            }
        case START_LOCATION:
            console.log("lat,long", action.payload)
            return {
                ...state,
                startLat: parseFloat(action.payload.geometry.lat),
                startLng: parseFloat(action.payload.geometry.lon),
            }
        case CLEAR_REDUCERS:
            return {
                newData: null,
                saveData: null,
                startLat: null,
                startLng: null,
                end: null
            }
        default:
            return state
    }
}