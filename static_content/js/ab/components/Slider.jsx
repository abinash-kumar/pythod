import React from 'react';
import SliderImg from './SliderImg.jsx';
import { showImages } from '../actions/SliderActions.jsx';
import ImageStore from '../store/Store.jsx';
import SwipeableViews from 'react-swipeable-views';

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
    const ActiveImgComponent = !activeImage ? null : activeImage.map((img, path) => ( <SliderImg path={path} {...img} myclass="active" height={this.height} width={this.width}/> ));
    const ImgComponent = !images ? null : images.map((img, path) => ( <SliderImg path={path} {...img} height={this.height} width={this.width}/> ));
    return (
      <div id="myCarousel" className="carousel slide" data-ride="carousel">
      <ol className="carousel-indicators">
        <li data-target="#myCarousel" data-slide-to="0" className="active"></li>
        <li data-target="#myCarousel" data-slide-to="1"></li>
        <li data-target="#myCarousel" data-slide-to="2"></li>
      </ol>
      <div className="carousel-inner" role="listbox" style={{height:this.height}}>
        {ActiveImgComponent}
        {ImgComponent}
      </div>
      <a className="left carousel-control" href="#myCarousel" role="button" data-slide="prev">
        <span className=" " aria-hidden="true"></span>
        <span className="sr-only">Previous</span>
      </a>

      <a className="right carousel-control" href="#myCarousel" role="button" data-slide="next" style={{marginTop:this.height/2 -15}}>
        <span className="" aria-hidden="true"></span>
        <span className="sr-only">Next</span>
      </a>

    </div>

    );
  }

}

export default Slider;
