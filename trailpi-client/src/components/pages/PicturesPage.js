import React from 'react';
import PropTypes from 'prop-types';
import './PicturesPage.scss';
import { Redirect } from 'react-router';

import PicturePanel from '../pictures/PicturePanel';
import { Input, Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';

class PicturesPage extends React.Component {
  constructor() {
    super();
    this.state = {
      images: [],
<<<<<<< HEAD
      selectedImages: [], // array of objects -> {id, isSelected}
=======
      isImageSelected: [], // array of booleans 
>>>>>>> web-dev
      modalToggled: false,
      tags: null,
      redirectHome: false
    };
    this.downloadImages = this.downloadImages.bind(this);
    this.toggleModal = this.toggleModal.bind(this);
    this.addTags = this.addTags.bind(this);
    this.updateTags = this.updateTags.bind(this);
    this.saveTags = this.saveTags.bind(this);
    this.selectImage = this.selectImage.bind(this);
    this.goHome = this.goHome.bind(this);
    this.deleteImage = this.deleteImage.bind(this);
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

    let selectedImages = []; // initialize selectedImages array 
    data.images.map(image => {
      selectedImages.push({
        id: image.id,
        isSelected: false
      });
    });
    this.setState({ images: data.images, selectedImages });
  }

  async downloadImages(imageName) { // TODO
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

  selectImage(imageId) {
    let oldImageState = this.state.selectedImages.filter((image) => { // get the previous selection state
      return image.id === imageId;
    });
    let tempImages = this.state.selectedImages.filter((image) => { // remove the old element
      return image.id !== imageId;
    });
    tempImages.push({ id: oldImageState[0].id, isSelected: !oldImageState[0].isSelected });
    this.setState({ selectedImages: tempImages });
  }

  addTags() { // pop-up the modal
    this.toggleModal();
  }

  updateTags(event) {
    let tags = event.target.value;
    this.setState({ tags });
  }

  saveTags() { // hide the modal and save the user input
    this.toggleModal();
  }

  goHome() {
    this.setState({ redirectHome: true });
  }

  deleteImage() {

  }

  getClass(imageId) {
    let image = this.state.selectedImages.filter((image) => {
      return image.id === imageId;
    });
    if (image[0].isSelected === true) 
      return 'picture-wrapper-selected';
    else
      return 'picture-wrapper';
  }

  render() {
    if (this.state.redirectHome) return <Redirect push to='/' />; // navigate to home
    return (
      <div className='picturesPage-wrapper'>
        <div className='control-panel'>
          <div className='flex-left'>
            <Button color='primary' onClick={this.goHome}>Home</Button>          
          </div>
          <div className='flex-right'>
            <Button color='success' onClick={this.addTags}>Add Tags</Button>
            <Button color='warning' onClick={this.downloadImage}>Download</Button>
            <Button color='danger' onClick={this.deleteImage}>Delete</Button>
          </div>
        </div>
        <div className='pictures-wrapper'>
          {this.state.images.map((image, key) => {
            let className = this.getClass(image.id);
            return (
              <PicturePanel
                key={key}
                imageInfo={image}
                className={className}
                onPictureSelect={this.selectImage}
              />
            );
          })}        
        </div>
        <Modal isOpen={this.state.modalToggled} toggle={this.toggleModal} className={this.props.className}>
          <ModalHeader toggle={this.toggle}>Photo Tags</ModalHeader>
          <ModalBody>
            <Input placeholder='tag1, tag2, tag3, etc...' onChange={(value) => this.updateTags(value)}/>
          </ModalBody>
          <ModalFooter>
            <Button color='primary' onClick={this.saveTags}>Submit</Button>{' '}
            <Button color='secondary' onClick={this.toggleModal}>Cancel</Button>
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