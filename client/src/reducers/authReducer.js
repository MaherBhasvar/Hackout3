//import { SET_CURRENT_USER } from '../actions/types'

const initialState = {
    isAuthenticated: true,
    user: {
        name: 'Maher Bhavsar',
        emailId: 'maher.daiict@gmail.com'
    }
}

export default function (state = initialState, action) {
    switch (action.type) {

        default:
            return state
    }
}