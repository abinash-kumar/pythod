import React from 'react';
import ReactDOM from 'react-dom';
import HeaderUserCard from './myaccount/HeaderUserCard.jsx'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'
import { FadeInUpBig } from "animate-components";
import SlickSlider from './SlickSlider.jsx';

import { Link } from 'react-router-dom';

import ArtistAllMin from './artist/ArtistAllMin.jsx';
import TagBanner from './auraai/TagBanner.jsx';
import Slider from 'react-slick';


const lightMuiTheme = getMuiTheme(lightBaseTheme);

class Home extends React.Component {

  constructor() {
    super();
    // HomeStore.fetchHomePageCustomUrls('all')
    this.state = {

    };
  }

  componentWillMount() {

  }

  componentWillUnmount() {

  }

  render() {
    const staticPath = "https://" + window.location.host;
    const params = {
      pagination: '.swiper-pagination',
      direction: 'vertical',
      slidesPerView: 1,
      paginationClickable: true,
      spaceBetween: 30,
      mousewheelControl: true,
      keyboardControl: true,
    };
    const isMobile = window.innerWidth <= 500 || getValueOfParam('mobile');
    // const footer_template = "{% include "+ "footer.html"+  "%}"
    const setting ={ 
                  dots: true,
                  infinite: true,
                  speed:400,
                  slidesToShow: 3,
                  slidesToScroll: 1,
                  autoplay: true,
                }
    const setting2 ={
                  dots: true,
                  infinite: true,
                  speed:300,
                  slidesToShow: 1,
                  slidesToScroll: 1,
                  autoplay: true,
                }

    return (
      <MuiThemeProvider muiTheme={lightMuiTheme}>
        <div className="name transition-item">
          <SlickSlider onpage="home" path={this.designer} width='100%'></SlickSlider>
          <div className="">
            <div>
              <section className="home-head">
                <div className="main-items">
                  <div className='col-xs-12 col-sm-12'>
                    <div className='col-xs-12 col-sm-6'>
                      <a href='/couple-tshirts/' target='_blank'>
                        <img className='home-page-banners' style={isMobile ? {} : { width: '92.5%' }} src="https://www.addictionbazaar.com/uploads/homepage/2018-02-07141044755115.jpg" />
                      </a>
                    </div>
                    <div className='col-xs-12 col-sm-6'>
                      <div className='col-xs-6 col-sm-6'>
                        <a href='/mens-clothing/' target='_blank'>
                          <img className='home-page-banners' style={isMobile ? {} : { left: -12, position: 'absolute' }} src="https://www.addictionbazaar.com/uploads/homepage/2018-02-07140934729137.jpg" />
                        </a>
                      </div>
                      <div className='col-xs-6 col-sm-6'>
                        <a href='/womens-clothing/' target='_blank'>
                          <img className='home-page-banners' src="https://www.addictionbazaar.com/uploads/homepage/2018-02-07141002621257.jpg" />
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              </section>
            </div>

            <section className="container home-head">
              <center><h2 className='h2-title'><strong>Buy in Bulk</strong></h2></center>
                <hr className="brace" />
                 <div className='col-xs-12 col-sm-12'>
                  <div >
                    <a href="/buy-in-bulk/" target='_blank' >
                      <img className="" src="https://www.addictionbazaar.com/uploads/homepage/2018-07-30111448002611.png" width="70%"  />
                    </a>
                  </div>
                 </div>

            </section>
                                    
            <section className="container home-head">
              <center><h2 className='h2-title'><strong>Happy Clients & Customers</strong></h2></center>
              <hr className="brace" />

              <div className='container'>
                <div style={{margin: '20px'}}> 
                      <Slider {...setting} style={{overflow: 'hidden', textAlign: 'center', width: '80%'}}>
                          <div>
                            <a>
                              <img src="https://www.addictionbazaar.com/uploads/homepage/2018-07-31104204419951.png" style={{width: '100%'}} />
                            </a>
                          </div>
                          <div>
                              <a>
                                <img src="https://www.addictionbazaar.com/uploads/homepage/2018-07-31104241848365.png" style={{width: '100%'}} />
                              </a>
                          </div>
                          <div>
                              <a>
                                <img src="https://www.addictionbazaar.com/uploads/homepage/2018-07-31104256324841.png" style={{width: '100%'}} />
                              </a> 
                          </div>
                          <div>
                              <a>
                                <img src="https://www.addictionbazaar.com/uploads/homepage/2018-07-31104220736607.png" style={{width: '100%'}} />
                              </a> 
                          </div>
                          <div>
                              <a>
                                <img src="https://www.addictionbazaar.com/uploads/homepage/2018-07-31104143164769.png" style={{width: '100%'}}/>
                              </a> 
                          </div>
                      </Slider>
                    </div>
                </div>
            </section>
              
            <section className="container home-head">
              <h2 className='h2-title'><strong>Trending</strong></h2>
              <hr className="brace" />
              <TagBanner />
            </section>
            
            <section className="container home-head">
              <h2 className='h2-title'><strong>Meet our art legends</strong></h2>
              <hr className="brace" />
              <ArtistAllMin />
            </section>

            
            <section className="container home-head" style={{backgroundColor: "#e8eff9", overflow: 'hidden'}}>
              <center><h2 className='h2-title'><strong>Testimonial</strong></h2></center>
              <center><strong>Reviews from our lovely Customers</strong></center>
              <hr className="brace" />

              <div className='container'>
                <div style={{margin: '20px'}}>
                  <Slider {...setting2}>
                
                  <div className="row">
                    <div className="col-xs-5 col-4 col-sm-4">
                      <center><img className="imgtest" src="https://addictionbazaar.com/uploads/homepage/2018-07-21085038928465.jpg" width="120px" height="120px" /></center>
                    </div>
                    <div className="col-xs-7 col-8 col-sm-8">
                       <p>Extremely satisfied with the service and quality of the t-shirts that I ordered for my friend's bachelorette. They were very prompt in delivering the product within such short notice. Will surely buy from them again!</p>
                       <span className="fa fa-star checked"></span>
                       <span className="fa fa-star checked"></span>
                       <span className="fa fa-star checked"></span>
                       <span className="fa fa-star checked"></span>
                       <span className="fa fa-star checked"></span>
                       <h3><strong>---Sirisha Veera</strong></h3>

                    </div>
                  </div>
                  
               
               
                <div className="row">
                  <div className="col-xs-5 col-4 col-sm-4">
                    <center><img className="imgtest" src="https://addictionbazaar.com/uploads/homepage/2018-07-21085118346215.jpg" width="120px" height="120px" /></center>
                  </div>
                  <div className="col-xs-7 col-8 col-sm-8">
                     <p>I had ordered my sunsign customised t shirt to wear it on my bday eve ..and I am very happy with the quality of product . It was worth spending the amount and looks cool to show off ur sun sign . Thanks a lot Addiction bazaar</p>
                       <span className="fa fa-star checked"></span>
                       <span className="fa fa-star checked"></span>
                       <span className="fa fa-star checked"></span>
                       <span className="fa fa-star checked"></span>
                       <span className="fa fa-star checked"></span>
                     <h3><strong>---Akanksha Dhamija</strong></h3>
                  </div>
                </div> 
               
               
                <div className="row">
                  <div className="col-xs-5 col-4 col-sm-4">
                    <center><img className="imgtest" src="https://addictionbazaar.com/uploads/homepage/2018-07-21085143580971.jpg" width="120px" height="120px" /></center>
                  </div>
                  <div className="col-xs-7 col-8 col-sm-8">
                     <p>Really helpful in getting all the design inputs and incorporating most of them. Also they get in touch with you to get the things done with more clarity and priority. Awesome artists out there to get your imagination real. And also very fast courier service. Thanks!</p>
                       <span className="fa fa-star checked"></span>
                       <span className="fa fa-star checked"></span>
                       <span className="fa fa-star checked"></span>
                       <span className="fa fa-star checked"></span>
                       <span className="fa fa-star checked"></span>
                     <h3><strong>---Shivam Maurya</strong></h3>
                  </div>
                 </div> 
                
                
                  <div className="row">
                    <div className="col-xs-5 col-4 col-sm-4">
                      <center><img className="imgtest" src="https://addictionbazaar.com/uploads/homepage/2018-07-21085242853320.jpg" width="120px" height="120px" /></center>
                    </div>
                   <div className="col-xs-7 col-8 col-sm-8">
                     <p>Its just an awesome place to shop the quality the delivery n the way they understand the customer needs is just amazing. Highly recommend site</p>
                       <span className="fa fa-star checked"></span>
                       <span className="fa fa-star checked"></span>
                       <span className="fa fa-star checked"></span>
                       <span className="fa fa-star checked"></span>
                       <span className="fa fa-star checked"></span>
                     <h3><strong>---Saloni Borde</strong></h3>
                   </div>
                  </div> 
                 
                 
                   <div className="row">
                    <div className="col-xs-5 col-4 col-sm-4">
                      <center><img className="imgtest" src="https://addictionbazaar.com/uploads/homepage/2018-07-21085305979803.jpg" width="120px" height="120px" /></center>
                    </div>
                   <div className="col-xs-7 col-8 col-sm-8">
                     <p>Great people. The way of talking is just awesome. Understands customers and works according to their request most of the time.</p>
                       <span className="fa fa-star checked"></span>
                       <span className="fa fa-star checked"></span>
                       <span className="fa fa-star checked"></span>
                       <span className="fa fa-star checked"></span>
                       <span className="fa fa-star checked"></span>
                     <h3><strong>---Shreyas Jadhav</strong></h3>
                   </div>
                  </div> 
                 
                 
                   <div className="row">
                    <div className="col-xs-5 col-4 col-sm-4">
                      <center><img className="imgtest" src="https://addictionbazaar.com/uploads/homepage/2018-07-21085326409338.jpg" width="120px" height="120px" /></center>
                    </div>
                  <div className="col-xs-7 col-8 col-sm-8">
                     <p>Excellent product. good quality tshirt with good printing. their customer service is extremely satisfactory. don't think twice just go for it..</p>
                       <span className="fa fa-star checked"></span>
                       <span className="fa fa-star checked"></span>
                       <span className="fa fa-star checked"></span>
                       <span className="fa fa-star checked"></span>
                       <span className="fa fa-star checked"></span>
                     <h3><strong>---Micky Abraham</strong></h3>
                  </div>
                </div> 
               
              </Slider>
                </div>
              </div>
            </section>
            
            
            
            <div>
            </div>
          </div>
          <HeaderUserCard />
        </div>
      </MuiThemeProvider>
    );
  }

}
export default Home;

