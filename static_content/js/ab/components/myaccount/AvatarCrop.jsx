import React from "react";
import ReactDom from "react-dom";
import AvatarCropper from "react-avatar-cropper";
import Avatar from 'material-ui/Avatar';

import API from '../../store/API.js';

var createReactClass = require('create-react-class');

var AvatarCrop = createReactClass({
  getInitialState: function () {
    return {
      cropperOpen: false,
      img: null,
      croppedImg: this.props.img
    };
  },
  handleFileChange: function (dataURI) {
    this.setState({
      img: dataURI,
      croppedImg: this.state.croppedImg,
      cropperOpen: true
    });
  },
  handleCrop: function (dataURI) {
    this.setState({
      cropperOpen: false,
      img: null,
      croppedImg: dataURI
    });
    API.uploadUserProfilePic(this.dataURItoBlob(dataURI), function (data) {
      if (data.success) {
        console.log('AAA')
      }
      else {
        console.log('BBB')
      }
    });
  },
  handleRequestHide: function () {
    this.setState({
      cropperOpen: false
    });
  },

  dataURItoBlob(dataURI) {
    // convert base64/URLEncoded data component to raw binary data held in a string
    var byteString;
    if (dataURI.split(',')[0].indexOf('base64') >= 0)
      byteString = atob(dataURI.split(',')[1]);
    else
      byteString = unescape(dataURI.split(',')[1]);

    // separate out the mime component
    var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];

    // write the bytes of the string to a typed array
    var ia = new Uint8Array(byteString.length);
    for (var i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i);
    }

    return new Blob([ia], { type: mimeString });
  },

  render() {
    return (
      <div>
        <div className="avatar-photo">
          <FileUpload handleFileChange={this.handleFileChange} />
          <div className="avatar-edit">
            <i className="fa fa-camera"></i>
          </div>
          <Avatar
            src={this.state.croppedImg}
            size={250}
          />
        </div>
        {this.state.cropperOpen &&
          <AvatarCropper
            onRequestHide={this.handleRequestHide}
            cropperOpen={this.state.cropperOpen}
            onCrop={this.handleCrop}
            image={this.state.img}
            width={400}
            height={400}
          />
        }
      </div>
    );
  }
});

var FileUpload = createReactClass({

  handleFile: function (e) {
    var reader = new FileReader();
    var file = e.target.files[0];

    if (!file) return;

    reader.onload = function (img) {
      ReactDom.findDOMNode(this.refs.in).value = '';
      this.props.handleFileChange(img.target.result);
    }.bind(this);
    reader.readAsDataURL(file);
  },

  render: function () {
    return (
      <input ref="in" type="file" accept="image/*" onChange={this.handleFile} />
    );
  }
});

export default AvatarCrop;
