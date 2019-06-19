import React from 'react';
import './MapPage.scss';

import ReserveMap from '../map/ReserveMap';
import Sidebar from '../sidebar/Sidebar';

class MapPage extends React.Component {
  render() {
    return (
      <div className='mapPage-wrapper'>
        <div className='sidebar-wrapper'>
          <Sidebar />
        </div>
        <div className='map-wrapper'>
          <ReserveMap />
        </div>      
      </div>
    );
  }
};

export default MapPage;