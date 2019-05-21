import React from 'react';
import PropTypes from 'prop-types';
import './PicturesPage.scss';

import PicturePanel from '../pictures/PicturePanel';
import { Input, Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';

class PicturesPage extends React.Component {
  constructor() {
    super();
    this.state = {
      images: [],
      isImageSelected: [], // array of booleans 
      modalToggled: false,
      tags: null,
      selectedSite: null
    };
    this.downloadImage = this.downloadImage.bind(this);
    this.toggleModal = this.toggleModal.bind(this);
    this.addTags = this.addTags.bind(this);
    this.updateTags = this.updateTags.bind(this);
    this.saveTags = this.saveTags.bind(this);
  }

  componentDidMount() {
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

    this.setState({ images: data.images });
  }

  async downloadImage(imageName) {
    let url = 'http://flask-server.wqwtbemyjw.us-west-2.elasticbeanstalk.com/TrailPiServer/api/downloadFile/';

    url += imageName;
    window.open(url);
  }

  // return a date string of the format: YYYY-MM-DD
  buildDateString(date) {
    let dateString = '';

    // append year
    dateString += date.getFullYear().toString();
    dateString += '-';

    // append month
    if (date.getMonth() < 10)
      dateString += '0' + (date.getMonth() + 1).toString();
    else
      dateString += (date.getMonth() + 1).toString();
    dateString += '-';

    // append days
    if (date.getDate() < 10)
      dateString += '0' + date.getDate().toString();
    else
      dateString += date.getDate().toString();

    return dateString;
  }

  toggleModal() {
    this.setState(prevState => ({modalToggled: !prevState.modalToggled}))
  }

  addTags(selectedSite) { // pop-up the modal
    this.toggleModal();
    this.setState({ selectedSite });
  }

  updateTags(event) {
    let tags = event.target.value;
    this.setState({ tags });
  }

  saveTags() { // hide the modal and save the user input
    this.toggleModal();
  }

  render() {
    return (
      <div className='picturesPage-wrapper'>
        {this.state.images.map((image, key) => {
          return (
            <PicturePanel
              picture={image.url}
              date={image.timestamp}
              siteNumber={image.site}
              onPictureSelect={this.addTags}
            />
          );
        })}
        <Modal isOpen={this.state.modalToggled} toggle={this.toggleModal} className={this.props.className}>
          <ModalHeader toggle={this.toggle}>Photo Tags</ModalHeader>
          <ModalBody>
            <Input placeholder="tag1, tag2, tag3, etc..." onChange={(value) => this.updateTags(value)}/>
          </ModalBody>
          <ModalFooter>
            <Button color="primary" onClick={this.saveTags}>Submit</Button>{' '}
            <Button color="secondary" onClick={this.toggleModal}>Cancel</Button>
          </ModalFooter>
        </Modal>
      </div>
    );
  }
};

PicturesPage.propTypes = {
  location: PropTypes.object.isRequired
};

export default PicturesPage;