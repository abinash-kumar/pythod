import React from 'react';
import ReactDOM from 'react-dom';
import DesignerStore from '../store/DesignerStore.jsx'
import UserStore from '../store/UserStore.jsx'
import SlickSlider from './SlickSlider.jsx';
import ProductModal from './product/ProductModal.jsx'
import Gallery from 'react-photo-gallery';
import {Lightbox} from 'react-lightbox-component';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
const lightMuiTheme = getMuiTheme(lightBaseTheme);


class DesignerProfile extends React.Component {

  constructor(props) {
      super(props);
      this.designer = window.location.pathname.split('/')[4];
      this.isArtistProfile = props['isArtistProfile'];
      this.getDesigners = this.getDesigners.bind(this);
      this.getArtistPublicProfileDetails = this.getArtistPublicProfileDetails.bind(this);
      if (this.isArtistProfile){
        UserStore.fetchArtistPublicProfile(this.designer)
      }
      else {
        DesignerStore.fetchDesigners(this.designer)
      }
      this.state = {
        designerData: null,
      };
  }


  componentWillMount() {
    UserStore.on("change", this.getArtistPublicProfileDetails);
    DesignerStore.on("change", this.getDesigners);
  }

  componentWillUnmount() {
    UserStore.removeListener("change", this.getArtistPublicProfileDetails);
    DesignerStore.removeListener("change", this.getDesigners);
  }

  getArtistPublicProfileDetails(){
    this.setState({
      designerData: UserStore.getArtistPublicProfileDetails()
    });
  }

  getDesigners() {
    this.setState({
      designerData: DesignerStore.getPremiumDesignerDetails()
    });
  }

  render(){
    const designerData = this.state.designerData;
    let requiredData = null;
    if (this.isArtistProfile){
       requiredData = !designerData ? null : [designerData];
    }
    else{
      requiredData = !designerData ? null : designerData['premium_desinger'].length == 0 ? designerData['other_designer'] : designerData['premium_desinger']
    }
    const products = !designerData? null: designerData['product_detail_list'];
    
    const ProductComponent = !products ? null : products.map((product) => 
          (
          <div className='col-sm-4 col-md-4 col-xs-6 deisgner-product'>
            <ProductModal productSlug={product['slug']} productID={product['id']} product={product}/>
          </div>
          )
    );

    const images = !designerData? null: !designerData['collage_list']? null: designerData['collage_list'].map(function(collageImage){
      return {src:collageImage['image']};
    });

    const collageComponent = () => {
      if (images){
     return (
       <Lightbox images={images}
        thumbnailWidth='250px'
        thumbnailHeight='250px'
        /> 
      )
     }
    }

    
    const renderCollage = collageComponent();
   
    const ProfileImgComponent = !requiredData ? null : requiredData[0].user_photo ;
    const AboutComponent = !requiredData ? null : requiredData[0].about ;
    const EductionComponent = !requiredData ? null : requiredData[0].education ;
    const ExpComponent = !requiredData ? null : requiredData[0].experience ;
    const GenderComponent = !requiredData ? null : requiredData[0].name[0] ;
    const NameComponent = !requiredData ? null : requiredData[0].name;
    const SpclComponent = !requiredData ? null : requiredData[0].specialization ;
    const user_type = this.isArtistProfile ? 'artist' : 'designer';
    const ProfileDetails = this.isArtistProfile ? null : function(){
      return (
            <div className='designer-header'>
              <h2><i className="fa fa-certificate"></i> {ExpComponent} years of Experience</h2>
              <h2><span className="fa fa-graduation-cap"></span>{EductionComponent} </h2>
              <div className="profile-bio">
                <p>Design Specialized In-</p>
                <p>{SpclComponent}</p>
              </div>
            </div>
        )
    }();
    return (
    <MuiThemeProvider muiTheme={lightMuiTheme}>
    <div>
      <SlickSlider onpage={user_type} path={this.designer} width='100%'></SlickSlider>
      <div className='container'>   
        <div className='col-xs-12 col-sm-12'>
          <div className='col-xs-12 col-sm-6 pad10'>
            <aside className="profile-card" style={{background:'rgb(145, 191, 187)'}}>
              <div className='designer-header'>
                <a href="#">
                  <img className='profile-image' src={ProfileImgComponent} />
                </a>
                <h1>{NameComponent}</h1>
              </div>
              {ProfileDetails}

            </aside>
          </div>

          <h1>{NameComponent}</h1>
          <p>{AboutComponent}</p>
        </div>
       </div>   
       <div className="container-full shade container">
       {ProductComponent}
       </div> 
    </div>
    </MuiThemeProvider>
    )
  }
}

export default DesignerProfile;