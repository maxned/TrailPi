import React from 'react';
import './Sidebar.scss';

import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";

import { Button } from 'reactstrap';

class Sidebar extends React.Component {
  constructor() {
    super();
    this.state = {
      startDate: new Date(),
      endDate: new Date,
      images: []
    };
    this.handleChangeStart = this.handleChangeStart.bind(this);
    this.handleChangeEnd = this.handleChangeEnd.bind(this);
    this.onDateSubmit = this.onDateSubmit.bind(this);
    this.downloadImage = this.downloadImage.bind(this);
  }

  async handleChangeStart(date) {
    this.setState({ startDate: date });
  }

  async handleChangeEnd(date) {
    this.setState({ endDate: date});
  }

  async onDateSubmit() {
    let url = 'http://flask-server.wqwtbemyjw.us-west-2.elasticbeanstalk.com/TrailPiServer/api/filesByDateRange/';
    let requestStartDate = this.buildDateString(this.state.startDate);
    let requestEndDate = this.buildDateString(this.state.endDate);

    url += requestStartDate + '/' + requestEndDate;
    let response = await fetch(url);
    let data = await response.json();
    
    let images = [];
    for (let file of data.filenames) 
      images.push(file);

    this.setState({ images });
  }

  async downloadImage(imageName) {
    let url = 'http://flask-server.wqwtbemyjw.us-west-2.elasticbeanstalk.com/TrailPiServer/api/downloadFile/';
    
    url += imageName;
    window.open(url);
  }

  // return a date string of the format: MMDDYY
  buildDateString(date) {
    let dateString = '';

    // append month
    if (date.getMonth() < 10)
      dateString += '0' + (date.getMonth() + 1).toString();
    else 
      dateString += (date.getMonth() + 1).toString();

    // append days
    if (date.getDate() < 10) 
      dateString += '0' + date.getDate().toString();
    else 
      dateString += date.getDate().toString();

    // append year
    dateString += date.getFullYear().toString().substr(-2);

    return dateString;
  }

  render() {
    const s3BucketURL = 'https://s3-us-west-2.amazonaws.com/trailpi-images/';
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
          <Button 
            color='primary'
            onClick={this.onDateSubmit}
          >
            Submit
          </Button>
        </div>
        <div className='image-panel'>
          {this.state.images.map((imageName, key) => {
            let imageURL = s3BucketURL + imageName;
            return (
              <div key={key} className='image-wrapper'>
                  <img src={imageURL} /> 
                  <Button
                    color='primary'
                    onClick={() => this.downloadImage(imageName)}
                  >
                    download
                  </Button>
              </div>
            );
          })}
        </div>
      </div>
    );
  }
}

export default Sidebar;