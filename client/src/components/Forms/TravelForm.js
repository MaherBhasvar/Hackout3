import React, { Component } from 'react'
import Input from '../common/Input'
import Radio from '../common/Radio'
//import PrimaryMode from './PrimaryMode'
import { Modal, Button } from 'react-bootstrap'
import { submitData, saveData, sendLocations } from '../../actions/submitActions'
import { connect, } from 'react-redux'
import { withRouter } from 'react-router-dom'
import CurrentLocation from '../GoogleMap/CurrentLocation'


class TravelForm extends Component {
    state = {
        name: '',
        start: '',
        end: '',
        date: '',
        emailId: '',
        passengers: '',
        primaryMode: '',
        showPrimaryMode: false,
        startLat: 28.6466773,
        startLng: 76.813073,
    }


    onBlur = (e) => {
        console.log(e.target.name)
        const data = {
            city: this.state[e.target.name],
        }
        //this.props.getLocation(data)
    }

    handleClose = (e) => {
        //e.preventDefautl()
        this.setState({
            showPrimaryMode: false
        })
    }

    handleSave = (e) => {
        // console.log(this.state);
        var data = {}
        if (this.state.primaryMode == "Bus") {
            data = { "entry": this.state.start, "dest": this.state.end, "date": "07-10-2019", "seats": this.state.passengers, "primaryMode": this.state.primaryMode }
        } else {
            data = { "entry": this.state.start, "dest": this.state.end, "date": "20191007", "seats": this.state.passengers, "primaryMode": this.state.primaryMode }
        }

        console.log(data)
        this.props.submitData(data, this.props.history)
        this.props.saveData(data)

        this.props.history.push('/result')
        this.setState({
            showPrimaryMode: false
        })
    }

    onChangeValue = (e) => {
        e.preventDefault()

        //console.log(nam, val)
        this.setState({
            [e.target.name]: e.target.value
        })

        if (e.target.name === "passengers") {
            const data = {
                city: this.state.start,
            }
            //this.props.getLocation(data)

            const data2 = {
                city: this.state.end
            }

            //setTimeout(() => { this.props.getLocation(data2) }, 10000)
        }

        // if ((this.state.startLat == '' || this.state.startLat == null) && this.state.start != '') {

        // }
    }

    onSubmit = (e) => {
        e.preventDefault();

        const data = {
            city: this.state.start,

        }

        const data2 = {
            entry: this.state.start,
            dest: this.state.end
        }

        this.setState({
            showPrimaryMode: true
        })

        // this.props.getLocation(data)

        this.props.sendLocations(data2)

        console.log(data);
    }

    fillDefault = (e) => {
        e.preventDefault()
        this.setState({
            name: 'Maher Bhavsar',
            start: 'Gandhinagar',
            end: 'Bangalore',
            date: '2019-10-06',
            emailId: 'maher.daiict@gmail.com',
            passengers: '1'
        })
    }

    // showPosition = (position) => {
    //     var lat = position.coords.latitude;
    //     var lng = position.coords.longitude;
    //     console.log(lat, lng)
    //     //map.setCenter(new google.maps.LatLng(lat, lng));
    //     this.setState({
    //         lat: lat,
    //         lng: lng
    //     })
    // }
    // getLocation = () => {
    //     if (navigator.geolocation) {
    //         navigator.geolocation.getCurrentPosition((position) => this.showPosition(position));
    //     } else {
    //         alert("Geolocation is not supported by this browser.");
    //     }
    // }





    render() {
        return (

            <div className="TravelForm container">

                <Modal show={this.state.showPrimaryMode} onHide={e => this.handleClose(e)}>
                    <Modal.Header closeButton>
                        <Modal.Title>Select Preferable Mode</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <div className="container" >
                            <div className=" col-12" >
                                <Radio
                                    label="Primary Mode"
                                    type="radio"
                                    name="primaryMode"
                                    value="Bus"
                                    radioMessage="Bus"
                                    onChange={e => this.onChangeValue(e)}
                                /></div>
                            <div className=" col-12" >
                                <Radio
                                    label=""
                                    type="radio"
                                    name="primaryMode"
                                    value="Flight"
                                    radioMessage="Flight"
                                    onChange={e => this.onChangeValue(e)}
                                />
                            </div>
                        </div>
                        {/* <Radio
                            label=""
                            type="radio"
                            name="primaryMode"
                            value="Both"
                            radioMessage="Both"
                            onChange={e => this.onChangeValue(e)}
                        /> */}
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="danger" onClick={e => this.handleClose(e)} >
                            Close
                        </Button>
                        <Button variant="primary" onClick={e => this.handleSave(e)} disabled={this.state.primaryMode == ''}>
                            Save
                        </Button>
                    </Modal.Footer>
                </Modal>
                <button className="btn btn-primary" onClick={e => this.fillDefault(e)}>
                    Fill Default
                </button>
                <div class="row">
                    <div class="col-4">

                        <form >
                            {/* <Input
                        label="Name"
                        type="text"
                        name="name"
                        value={this.state.name}
                        onChange={e => this.onChangeValue(e)} /> */}
                            <Input
                                label="Start Point"
                                type="text"
                                name="start"
                                value={this.state.start}
                                onChange={e => this.onChangeValue(e)}
                                onBlur={e => this.onBlur(e)}
                            />
                            <Input
                                label="End Point"
                                type="text"
                                name="end"
                                value={this.state.end}
                                onChange={e => this.onChangeValue(e)}
                                onBlur={e => this.onBlur(e)}
                            />

                            <Input
                                label="Date of Journey"
                                type="date"
                                name="date"
                                value={this.state.date}
                                onChange={e => this.onChangeValue(e)} />
                            {/* <Input
                                label="Email Id"
                                type="tex"
                                name="eamilId"
                                value={this.state.emailId}
                                onChange={e => this.onChangeValue(e)} /> */}
                            <Input
                                label="Number of Passengers"
                                type="number"
                                name="passengers"
                                value={this.state.passengers}
                                onChange={e => this.onChangeValue(e)} />
                            <button
                                disabled={this.state.start == '' || this.state.end == '' || this.state.date == '' || this.state.passengers == ''}
                                className="btn btn-primary"
                                onClick={e => this.onSubmit(e)}> Submit </button>
                        </form>
                    </div>
                    <div class="col-6">

                        {console.log(this.props.submit.startLng)}
                        <CurrentLocation startLng={this.props.submit.startLng} startLat={this.props.submit.startLat} />
                    </div>

                </div>



            </div>
        )
    }

}

const mapStateToProps = state => ({
    auth: state.auth,
    errors: state.errors,
    submit: state.submit
});

export default connect(mapStateToProps, { submitData, saveData, sendLocations })(withRouter(TravelForm));