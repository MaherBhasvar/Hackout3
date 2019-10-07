import React, { Component } from 'react'
import { connect } from 'react-redux'
import { getLocation } from '../../actions/locationActions'

class GetLocation extends Component {
    state = {

    }

    componentDidMount() {
        const data = null
        this.props.getLocation(data)
    }

    render() {
        return (
            <div>

            </div>
        )
    }
}

const mapStateToProps = state => ({
    auth: state.auth,
    error: state.error,
    submit: state.submit
})
export default connect(mapStateToProps, { getLocation })(GetLocation)