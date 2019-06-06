import React from 'react';
import Leaflet from 'leaflet';
import { Map, TileLayer, Marker, Popup } from 'react-leaflet';

import { defaultLocation, mapMarkers } from '../common/mapConfig';
import { getSiteActivity } from '../../utils/requests';

const greenIcon = new Leaflet.Icon({
  iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png'
});

const redIcon = new Leaflet.Icon({
  iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png'
})

class ReserveMap extends React.Component {
  constructor() {
    super();
    this.state = { siteActivity: [] }
  }

  async componentDidMount() {
    let siteActivity = await getSiteActivity();
    this.setState({ siteActivity });
  }

  render() {
    const position = [defaultLocation.lat, defaultLocation.lng];
    return (
      <Map center={position} zoom={defaultLocation.zoom} zoomControl={false}>
        <TileLayer
          attribution='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
          url='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
        />
        {mapMarkers.map((marker, key) => {
          if (this.state.siteActivity.length === 0) {
            return (
              <Marker position={marker.position} key={key}>
                <Popup>
                  <b>{marker.name}</b>
                </Popup>
              </Marker>
            );
          }
          if (this.state.siteActivity[key].alive === true) {
            return (
              <Marker position={marker.position} key={key} icon={greenIcon}>
                <Popup>
                  <b>{marker.name}</b>
                </Popup>
              </Marker>
            );
          }
          else {
            return (
              <Marker position={marker.position} key={key} icon={redIcon}>
                <Popup>
                  <b>{marker.name}</b>
                </Popup>
              </Marker>
            );
          }
        })}
      </Map>
    );
  }
}

export default ReserveMap;