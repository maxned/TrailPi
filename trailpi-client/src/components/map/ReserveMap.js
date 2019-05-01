import React from 'react';
import { Map, TileLayer, Marker, Popup } from 'react-leaflet';

import { defaultLocation, mapMarkers } from '../common/mapConfig';

class ReserveMap extends React.Component {
  render() {
    const position = [defaultLocation.lat, defaultLocation.lng];
    return (
      <Map center={position} zoom={defaultLocation.zoom} zoomControl={false}>
        <TileLayer
          attribution='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
          url='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
        />
        {mapMarkers.map((marker, key) => {
          return (
            <Marker position={marker.position} key={key}>
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

export default ReserveMap;