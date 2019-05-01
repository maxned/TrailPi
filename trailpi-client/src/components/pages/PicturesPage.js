import React from 'react';
import './PicturesPage.scss';

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
    console.log(this.props.location.state.sites);
    this.getImages({
      startDate: this.props.location.state.startDate,
      endDate: this.props.location.state.endDate,
      sites: this.props.location.state.sites
    });
  }

  async getImages(options) {
    let url = 'http://flask-server.wqwtbemyjw.us-west-2.elasticbeanstalk.com/TrailPiServer/api/images/';
    let requestStartDate = this.buildDateString(options.startDate);
    let requestEndDate = this.buildDateString(options.endDate);

    url += `${requestStartDate}/${requestEndDate}`;
    if (options.sites.length > 0)
      url += '/';

    for (let site of options.sites) 
      url += `${site.value}+`;

    url = url.slice(0, -1);  

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
                <div className='control-panel'>
                  <h6>{imageName.slice(0, 5)}</h6>
                  <Button
                    color='primary'
                    onClick={() => this.downloadImage(imageName)}
                    size='sm'
                  >
                    download
                  </Button>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  }
};

export default PicturesPage;