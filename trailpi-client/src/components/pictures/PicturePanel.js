import React from 'react';
import PropTypes from 'prop-types';

// given an array of strings, build a single string
const buildTagString = tags => {
  return tags.join(', ');
}

const PicturePanel = props => {
  return (
    <div className='panel-wrapper'>
      <div className='picture-wrapper'>
        <img src={props.picture} />
      </div>
      <div className='info-wrapper'>
        <div>Date: {props.date}</div>
        <div>Site Name: {props.siteName}</div>
        <div>Site Number: {props.siteNumber}</div>
        <div>Tags: { () => buildTagString(props.tags) }</div>
      </div>
    </div>
  );
}

PicturePanel.propTypes = {
  picture: PropTypes.string.isRequired, // picture src url
  date: PropTypes.string.isRequired,
  siteName: PropTypes.string.isRequired,
  siteNumber: PropTypes.number.isRequired,
  tags: PropTypes.array
}

export default PicturePanel;