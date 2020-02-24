import React from 'react';
import ReactDOM from 'react-dom';
import { StyleRoot } from 'radium';
import DesignerStore from '../store/DesignerStore.jsx'

import createBrowserHistory from 'history/createBrowserHistory'
import Slider from 'react-slick';
const customHistory = createBrowserHistory()


var fn = function () {
  /* do you want */
}

const styles = {
  designerStyle: {
    '@media (max-width: 800px)': {
      width: '600px',
      height: '300px'
    },
    '@media (min-width: 800px)': {
      width: '960px',
      height: '600px'
    },
  }
}



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
        return { display: 'none' };
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
        return { display: 'none' };
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

class DesignerHome extends React.Component {

  constructor() {
    super();
    DesignerStore.fetchDesigners('all')
    this.getDesigners = this.getDesigners.bind(this);
    this.state = {
      designerData: null,
    };
  }

  componentWillMount() {
    DesignerStore.on("change", this.getDesigners);
  }

  componentWillUnmount() {
    DesignerStore.removeListener("change", this.getDesigners);
  }

  getDesigners() {
    this.setState({
      designerData: DesignerStore.getPremiumDesignerDetails()['premium_desinger']
    });
  }

  render() {
    const staticPath = "https://" + window.location.host;
    var settings = {
      slidesToShow: 3,
      className: 'des-slider',
      autoplay: true,
      autoplaySpeed: 2000,
      nextArrow: <SampleNextArrow />,
      prevArrow: <SamplePrevArrow />,
    }
    let designerData = this.state.designerData
    const ImgComponent = !designerData ? null : designerData.map((designerData) => (
      <div>
        <a href={designerData['profile_link']}>
          <img src={designerData["user_photo"]} alt={designerData['name']} data-action={designerData['profile_link']} className='photo-designer' />
          <div className='des-name'>{designerData['name']}</div>
        </a>
      </div>
    )
    );

    const slider = function () {
      if (ImgComponent) {
        return (
          <div>
            <Slider  {...settings}>
              {ImgComponent}
            </Slider>
          </div>
        )
      }
    }();

    return (
      <div>
        <section className="container des-flow">
          <h2>Adorned Designs by finest deginers</h2>
          <div className="col-md-3">
            <img className="d-img" src={staticPath + "/static/myhome/images/111.png"} />
            <h5>Tell Your Requirement</h5>

          </div>

          <div className="col-md-3">
            <img className="d-img" src={staticPath + "/static/myhome/images/flow-for-designer.png"} />
            <h5>Select Quote of Your Favorite Designer</h5>

          </div>

          <div className="col-md-3">
            <img className="d-img" src={staticPath + "/static/myhome/images/11.png"} />
            <h5>Finalize case and Pay minimum amount</h5>

          </div>

          <div className="col-md-3">
            <img className="d-img" src={staticPath + "/static/myhome/images/41.png"} />
            <h5>Get the Awesome Designer wear at your door steps</h5>

          </div>
        </section>

        <section className="des-p">
          <br />
          <h1>Premium Designers</h1>
          <br />
          <div className="col-md-12">
            <div className='c-slider'>
              <StyleRoot>
                {slider}
              </StyleRoot>
            </div>
          </div>
        </section>
      </div>
    );
  }

}

export default DesignerHome;