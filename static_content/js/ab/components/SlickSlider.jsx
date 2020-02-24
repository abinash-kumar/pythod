import React from 'react';
import SliderImg from './SliderImg.jsx';
import { showImages } from '../actions/SliderActions.jsx';
import ImageStore from '../store/Store.jsx';
import { autoPlay } from 'react-swipeable-views-utils';
import Slider from 'react-slick';


class SampleNextArrow extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    const className = this.props.className
    const style = this.props.style
    const onClick = this.props.onClick
    const mystyle = function () {
      console.log(className)
      if (className.indexOf("slick-disabled") >= 0) {
        return { opacity: '0.4' };
      }
    }();
    return (
      <div
        className={'right-arrow'}
        style={mystyle}
        onClick={onClick}
      ></div>
    )
  }
}


class SamplePrevArrow extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    const className = this.props.className
    const style = this.props.style
    const onClick = this.props.onClick
    const mystyle = function () {
      console.log(className)
      if (className.indexOf("slick-disabled") >= 0) {
        return { opacity: '0.4' };
      }
    }();
    return (
      <div
        className={'left-arrow'}
        style={mystyle}
        onClick={onClick}
      ></div>
    )
  }
}


class SlickSlider extends React.Component {

  constructor(props) {
    super(props);
    this.height = this.props['height']
    this.width = this.props['width']
    this.userType = this.props['onpage']
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
    var artist_settings = {
      dots: true,
      infinite: true,
      arrows: true,
      slidesToShow: 5,
      slidesToScroll: 5,
      nextArrow: <SampleNextArrow />,
      prevArrow: <SamplePrevArrow />,
    }

    var designer_settings = {
      dots: true,
      infinite: true,
      arrows: true,
      slidesToShow: 1,
      slidesToScroll: 1,
      nextArrow: <SampleNextArrow />,
      prevArrow: <SamplePrevArrow />,
    }

    let images = this.state.images;
    let activeImage = this.state.activeImage;
    const isMobile = window.innerWidth <= 500 || getValueOfParam('mobile');
    var ImgComponent = null;
    if (isMobile) {
      ImgComponent = !images ? null : activeImage.concat(images).map((img, i) => (
        <div className='sli' key={i}>
          <a href={img.url}>
            <img src={img.image_mobile} style={{ height: this.height }} alt="Banner- Addiction Bazaar" />
          </a>
        </div>));
    }
    else {
      ImgComponent = !images ? null : activeImage.concat(images).map((img, i) => (
        <div className='sli' key={i}>
          <a href={img.url}>
            <img src={img.image} style={{ height: this.height }} alt="Banner- Addiction Bazaar" />
          </a>
        </div>));
    }
    const settingOfUser = this.userType == 'artist' ? artist_settings : designer_settings;
    return (
      <div>
        <Slider autoplay="true"  {...settingOfUser}>
          {ImgComponent}
        </Slider>

      </div>

    );
  }

}

export default SlickSlider;
