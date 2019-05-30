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
      selectedImages: [], // array of objects -> {id, isSelected}
      tagsModalToggled: false,
      adminModalToggled: false,
      tags: '',
      username: '',
      password: '',
      redirectHome: false
    };
    this.downloadImages = this.downloadImages.bind(this);
    this.toggleTagsModal = this.toggleTagsModal.bind(this);
    this.updateTags = this.updateTags.bind(this);
    this.handleTagSubmit = this.handleTagSubmit.bind(this);
    this.toggleAdminModal = this.toggleAdminModal.bind(this);
    this.updateUsername = this.updateUsername.bind(this);
    this.updatePassword = this.updatePassword.bind(this);
    this.handleAdminSubmit = this.handleAdminSubmit.bind(this);
    this.selectImage = this.selectImage.bind(this);
    this.goHome = this.goHome.bind(this);
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

  async downloadImages() {
    let url = 'http://flask-server.wqwtbemyjw.us-west-2.elasticbeanstalk.com/TrailPiServer/api/download/';
    let imagesToDownload = this.state.selectedImages.filter(image => { // filter out selected images
      return image.isSelected === true; 
    });

    for (let image of imagesToDownload) { // extract the url for each of the selected images
      let currentImageData = this.state.images.filter(imageInfo => {
        return imageInfo.id === image.id;
      });
      let splitStr = currentImageData[0].url.split('/');
      let fileName = splitStr[splitStr.length - 1];
      url += fileName + '+';
    }
    url = url.slice(0, -1);  // remove the trailing "+" from the url
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

  toggleTagsModal() {
    this.setState(prevState => ({ tagsModalToggled: !prevState.tagsModalToggled }));
  }

  updateTags(event) {
    let tags = event.target.value;
    this.setState({ tags });
  }

  handleTagSubmit() { // hide the modal and save the user input
    this.toggleTagsModal();
    console.log(this.state.tags);
  }

  toggleAdminModal() { // pop up a modal which prompts for admin credentials and password
    this.setState(prevState => ({ adminModalToggled: !prevState.adminModalToggled }));
  }

  updateUsername(event) {
    let username = event.target.value;
    this.setState({ username });
  }

  updatePassword(event) {
    let password = event.target.value;
    this.setState({ password });
  }

  async handleAdminSubmit() {
    this.toggleAdminModal();
    console.log(this.state.username);
    console.log(this.state.password);
  }

  goHome() {
    this.setState({ redirectHome: true });
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
            <Button color='success' onClick={this.toggleTagsModal}>Add Tags</Button>
            <Button color='warning' onClick={this.downloadImages}>Download</Button>
            <Button color='danger' onClick={this.toggleAdminModal}>Delete</Button>
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
        <Modal isOpen={this.state.tagsModalToggled} toggle={this.toggleTagsModal} className='tagsModal'>
          <ModalHeader toggle={this.toggle}>Photo Tags</ModalHeader>
          <ModalBody>
            <Input placeholder='tag1, tag2, tag3, etc...' onChange={(event) => this.updateTags(event)}/>
          </ModalBody>
          <ModalFooter>
            <Button color='primary' onClick={this.handleTagSubmit}>Submit</Button>{' '}
            <Button color='secondary' onClick={this.toggleTagsModal}>Cancel</Button>
          </ModalFooter>
        </Modal>
        <Modal isOpen={this.state.adminModalToggled} toggle={this.toggleAdminModal} className='adminModal'>
          <ModalHeader toggle={this.toggle}>Enter Admin Credentials</ModalHeader>
          <ModalBody>
            <Input placeholder='username' onChange={(event) => this.updateUsername(event)} />
            <Input type='password' placeholder='password' onChange={(event) => this.updatePassword(event)} style={{marginTop: '25px'}}/>
          </ModalBody>
          <ModalFooter>
            <Button color='primary' onClick={this.handleAdminSubmit}>Submit</Button>{' '}
            <Button color='secondary' onClick={this.toggleAdminModal}>Cancel</Button>
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