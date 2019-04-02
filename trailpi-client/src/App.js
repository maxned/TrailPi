import React, { Component } from 'react';
import { Map, TileLayer, Marker, Popup } from 'react-leaflet';

const markers = [
  {
    name: 'Camera 7',
    caption: 'Photos taken: 5',
    position: [38.527945, -122.145610]
  },
  {
    name: 'Camera 13',
    caption: 'Photos taken: 7',
    position: [38.506524, -122.158719]
  },
  {
    name: 'Camera 17',
    caption: 'Photos taken: 13',
    position: [38.506904, -122.147281]
  },
  {
    name: 'Camera 2',
    caption: 'Photos taken: 2',
    position: [38.514314, -122.141300]
  },
  {
    name: 'Camera 4',
    caption: 'Photos taken: 3',
    position: [38.507806, -122.124003]
  },
];

class App extends Component {
  constructor() {
    super();
    this.state = {
      lat: 38.511,
      lng: -122.147,
      zoom: 14.5
    };
  }

  render() {
    const position = [this.state.lat, this.state.lng]
    return (
      <Map center={position} zoom={this.state.zoom}>
        <TileLayer
          attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {markers.map((marker, key) => {
          return (
            <Marker position={marker.position}>
              <Popup>
                <b>{marker.name}</b> <br /> {marker.caption}
              </Popup>
            </Marker>
          );
        })}
      </Map>
    );
  }
}

export default App;
