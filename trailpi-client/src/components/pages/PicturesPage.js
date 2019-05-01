import React from 'react';

import { Button } from 'reactstrap';


class PicturesPage extends React.Component {
  constructor() {
    super();
    this.state = {
      images: []
    };
    this.downloadImage = this.downloadImage.bind(this);
  }

  componentDidMount() {
    this.getImages({
      startDate: this.props.location.state.startDate,
      endDate: this.props.location.state.endDate,
      cameras: this.props.location.state.cameras
    });
  }

  async getImages(options) {
    let url = 'http://flask-server.wqwtbemyjw.us-west-2.elasticbeanstalk.com/TrailPiServer/api/filesByDateRange/';
    let requestStartDate = this.buildDateString(options.startDate);
    let requestEndDate = this.buildDateString(options.endDate);

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
      <div className='picturesPage-wrapper'>
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
};

export default PicturesPage;