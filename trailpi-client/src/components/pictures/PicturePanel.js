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
        <div className={this.props.className} onClick={() => this.props.onPictureSelect(this.props.imageInfo.id)}>
          <img src={this.props.imageInfo.url} />
        </div>
        <div className='info-wrapper'>
          <div><b>Date:</b> {this.props.imageInfo.timestamp}</div>
          <div><b>Site No:</b> {this.props.imageInfo.site}</div>
          <div><b>Tags:</b> {() => this.buildTagString(this.props.tags)}</div>
        </div>
      </div>
    );
  }
}

PicturePanel.propTypes = {
  imageInfo: PropTypes.object.isRequired,
  onPictureSelect: PropTypes.func.isRequired,
  className: PropTypes.string.isRequired,
  tags: PropTypes.array
}

export default PicturePanel;