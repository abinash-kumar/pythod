import React from 'react';
import SliderImg from './SliderImg.jsx';
import { showImages } from '../actions/SliderActions.jsx';
import ImageStore from '../store/Store.jsx';
import SwipeableViews from 'react-swipeable-views';
import { autoPlay } from 'react-swipeable-views-utils';

const AutoPlaySwipeableViews = autoPlay(SwipeableViews);

class Slider extends React.Component {

  constructor(props) {
    super(props);
    this.height = parseInt(this.props['height'])
    this.width = this.props['width']
    this.getImages = this.getImages.bind(this);
    ImageStore.fetchImages(this.props['onpage'], this.props['path'])
    this.state = {
      images: null,
      activeImage: null,
    };
  }

  componentWillMount() {
    ImageStore.on("change", this.getImages);
  }

  componentWillUnmount() {
    ImageStore.removeListener("change", this.getImages);
  }

  getImages() {
    this.setState({
      images: ImageStore.getImages()[0],
      activeImage: ImageStore.getImages()[1],
    });
  }

  render() {
    let images = this.state.images;
    let activeImage = this.state.activeImage;
    // const ActiveImgComponent = !activeImage ? null : activeImage.map((img, path) => ( <SliderImg path={path} {...img} myclass="active" height={this.height} width={this.width}/> ));
    const ImgComponent = !images ? null : activeImage.concat(images).map((img) => ( <img className='fadeOut' src={img.image} height={this.height} width={this.width}/> ));
    return (
     <div>

     <AutoPlaySwipeableViews >
     {ImgComponent}
     </AutoPlaySwipeableViews>


     </div>

    );
  }

}

export default Slider;
