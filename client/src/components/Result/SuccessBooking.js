import React, { Component } from 'react'
import { Link, withRouter } from 'react-router-dom'
import { clearReducers } from '../../actions/submitActions'
import { connect } from 'react-redux'


class SuccessBooking extends Component {

    state = {

    }

    render() {
        return (
            <div className="container">
                <h1>Your Booking is Successful</h1>
                <h4>Thank You For Choosing Us</h4>
                <Link to="/" onClick={(e) => { this.props.clearReducers() }}>Book Another Ticket</Link>
            </div>
        )
    }
}

const mapStateToProps = state => ({
    auth: state.auth,
    errors: state.errors,
    submit: state.submit
})

export default connect(mapStateToProps, { clearReducers })(withRouter(SuccessBooking))