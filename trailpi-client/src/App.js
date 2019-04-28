import React from 'react';
import './App.scss';

import ReserveMap from './components/map/ReserveMap';
import Sidebar from './components/sidebar/Sidebar';

class App extends React.Component {
  render() {
    return (
      <div className='wrapper'>
        <div className='sidebar-wrapper'>
          <Sidebar />
        </div>
        <div className='map-wrapper'>
          <ReserveMap />
        </div>      
      </div>
    );
  }
}

export default App;
