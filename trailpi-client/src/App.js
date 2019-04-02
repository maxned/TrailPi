import React, { Component } from 'react';
import { Map, TileLayer, Marker, Popup } from 'react-leaflet';

import { defaultLocation, mapMarkers } from './components/common/mapConfig';

class App extends Component {
  render() {
    const position = [defaultLocation.lat, defaultLocation.lng]
    return (
      <Map center={position} zoom={defaultLocation.zoom}>
        <TileLayer
          attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {mapMarkers.map((marker, key) => {
          return (
            <Marker position={marker.position}>
              <Popup>
                <b>{marker.name}</b>
              </Popup>
            </Marker>
          );
        })}
      </Map>
    );
  }
}

export default App;
