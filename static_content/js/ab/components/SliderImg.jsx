import React from 'react';

class SliderImg extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    let path = this.props['image'];
    let myclass = !this.props['myclass'] ? 'item' : this.props['myclass'] + ' item';

    const style = {
      sliderImage: {height:this.props['height'], width:this.props['width']}
    }

    return (
        <div className={myclass}>
          <img className="second-slide" src="data:image/gif;base64,R0lGODlhAQABAIAAAHd3dwAAACH5BAAAAAAALAAAAAABAAEAAAICRAEAOw==" alt="Second slide"></img>
          <div >
          <img src={path} alt="" style={style.sliderImage}></img>
          <div className="carousel-caption">
            
          </div>
          </div>
        </div>
    );
  }

}

export default SliderImg;
