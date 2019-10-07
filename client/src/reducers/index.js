import { combineReducers } from 'redux'

import authReducer from './authReducer';
import errorReducer from './errorReducer';
import submitReducer from './submitReducer';

export default combineReducers({
    auth: authReducer,
    errors: errorReducer,
    submit: submitReducer,

});