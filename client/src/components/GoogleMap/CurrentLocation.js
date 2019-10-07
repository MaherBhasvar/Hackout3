import React, { Component } from 'react'
import { Map, GoogleApiWrapper, InfoWindow, Geocoder, Marker } from 'google-maps-react';

var map, infoWindow
class CurrentLocation extends Component {

    // state = {
    //     // map: '',
    //     // infoWindow: '',
    //     lat: this.props.startlat,
    //     lng: '72.6369',
    // }
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
    //         navigator.geolocation.getCurrentPosition(this.showPosition);
    //     } else {
    //         alert("Geolocation is not supported by this browser.");
    //     }
    // }

    state = {
        lat: this.props.startLat,
        lng: this.props.startLng
    }


    render() {
        const mapStyles = {
            width: '100%',
            height: '100%',
        };
        console.log(this.props.startLat)
        return (
            <div className="GoogleMaps">
                <Map
                    google={this.props.google}
                    zoom={4}
                    style={mapStyles}
                    initialCenter={{ lng: 76.813073, lat: 28.6466773 }}
                //center={{ lat: this.props.startLat, lng: this.props.startLng }}
                >
                    {/* <Marker position={{ lat: (this.props.startLat), lng: (this.props.startLng) }} /> */}
                </Map>
            </div>
        );
    }
}

export default GoogleApiWrapper({
    apiKey: 'AIzaSyCfVJ5BempzSWsifnLXpNHwTAqh3lXL-oA'
})(CurrentLocation);

//export default CurrentLocation;