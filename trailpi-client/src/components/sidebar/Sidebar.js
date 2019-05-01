import React from 'react';
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
    this.onDateSubmit = this.onDateSubmit.bind(this);
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

  async onDateSubmit() {
    // Transition to next page
    console.log(this.state.startDate);
    console.log(this.state.endDate);
    console.log(this.state.selectedOptions);
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
        <div className='camera-select'>
          <Select 
            isMulti 
            name='cameras'
            options={selectOptions}
            onChange={this.handleCameraSelect}
            className='basic-multi-select'
            classNamePrefix='select'
          />
        </div>
        <div className='submit-wrapper'>
          <Button
            color='primary'
            onClick={this.onDateSubmit}
          >
            Submit
          </Button>        
        </div>
      </div>
    );
  }
}

export default Sidebar;