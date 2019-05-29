import React from 'react';
import { Link } from 'react-router-dom';
import trailPiLogo from './trailpi-logo.png';
import './Sidebar.scss';

import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";

import Select from 'react-select';
import { selectOptions  } from '../common/selectConfig';

import { Button } from 'reactstrap';

class Sidebar extends React.Component {
  constructor() {
    super();
    this.state = {
      startDate: new Date(),
      endDate: new Date(),
      selectedOptions: null
    };
    this.handleChangeStart = this.handleChangeStart.bind(this);
    this.handleChangeEnd = this.handleChangeEnd.bind(this);
    this.handleCameraSelect = this.handleCameraSelect.bind(this);
  }

  handleChangeStart(date) {
    this.setState({ startDate: date });
  }

  handleChangeEnd(date) {
    this.setState({ endDate: date});
  }

  handleCameraSelect(selectedOptions) {
    this.setState({ selectedOptions });
  }

  render() {
    return (
      <div className='sidebar-wrapper'>
        <h2>date select</h2>
        <div className='datepicker-wrapper'>
          <DatePicker 
            selected={this.state.startDate}
            selectsStart 
            startDate={this.state.startDate}
            endDate={this.state.endDate}
            onChange={this.handleChangeStart}
          />
          <DatePicker 
            selected={this.state.endDate}
            selectsEnd 
            startDate={this.state.startDate}
            endDate={this.state.endDate}
            onChange={this.handleChangeEnd}
          />        
        </div>
        <div className='site-select'>
          <Select 
            isMulti 
            name='sites'
            options={selectOptions}
            onChange={this.handleCameraSelect}
            className='basic-multi-select'
            classNamePrefix='select'
          />
        </div>
        <div className='submit-wrapper'>
          <Link to={{ 
            pathname: '/pictures', 
            state: {
              startDate: this.state.startDate,
              endDate: this.state.endDate,
              sites: this.state.selectedOptions 
            } 
          }}>
            <Button
              color='primary'
            >
              Submit
            </Button>                  
          </Link>
        </div>
        <div className='logo-wrapper'>
          <img src={trailPiLogo} alt='TrailPi' />
        </div>
      </div>
    );
  }
}

export default Sidebar;