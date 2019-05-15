import React from 'react';
import PropTypes from 'prop-types';
import './PicturePanel.scss';

class PicturePanel extends React.Component {
  // given an array of tags, return them as a string
  buildTagString(tags) {
    return tags.join(', ');
  }

  render() {
    return (
      <div className='panel-wrapper'>
        <div className='picture-wrapper' onClick={this.props.onPictureSelect}>
          <img src={this.props.picture} />
        </div>
        <div className='info-wrapper'>
          <div><b>Date:</b> {this.props.date}</div>
          <div><b>Site No:</b> {this.props.siteNumber}</div>
          <div><b>Tags:</b> {() => this.buildTagString(this.props.tags)}</div>
        </div>
      </div>
    );
  }
}

PicturePanel.propTypes = {
  picture: PropTypes.string.isRequired, // picture src url
  date: PropTypes.string.isRequired,
  siteName: PropTypes.string.isRequired,
  siteNumber: PropTypes.number.isRequired,
  onPictureSelect: PropTypes.func.isRequired,
  tags: PropTypes.array
}

export default PicturePanel;