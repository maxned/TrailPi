import React from 'react';
import './Sidebar.scss';

class Sidebar extends React.Component {
  constructor() {
    super();
    this.state = {
      images: []
    };
    this.handleClick.bind(this);
  }

  async handleClick() {
    const url = 'http://flask-server.wqwtbemyjw.us-west-2.elasticbeanstalk.com/TrailPiServer/api/files';
    let response = await fetch(url);
    let data = await response.json();
    
    let images = [];
    for (let file of data.filenames) 
      images.push(file);

    this.setState({ images });
  }

  render() {
    const s3BucketURL = 'https://s3-us-west-2.amazonaws.com/trailpi-images/';
    return (
      <div className='sidebar-wrapper'>
        <div onClick={() => this.handleClick()}>Press me!</div>
        {this.state.images.map((imageName, key) => {
          let imageURL = s3BucketURL + imageName;
          return (
            <div key={key} className='image-wrapper'>
                <img src={imageURL} /> 
            </div>
          );
        })}
      </div>
    );
  }
}

export default Sidebar;