import React from 'react';
import API from '../../store/API'
import ProductStore from '../../store/ProductStore.jsx';
import ReactImageMagnify from 'react-image-magnify';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import RaisedButton from 'material-ui/RaisedButton';
import HeaderUserCard from '../myaccount/HeaderUserCard.jsx';
import BreadCreum from '../abcomponents/BreadCrumb.jsx';
import DeliveryPincode from './DeliveryPincode.jsx';
import { toast } from 'react-toastify';
import BreadCrumb from '../abcomponents/BreadCrumb.jsx';
import ProductVarients from './ProductVarientsNew.jsx';
import ProductName from './smallComponents/ProductName.jsx';
import ArtistName from './smallComponents/ArtistName.jsx';
import VarientText from './smallComponents/VarientText.jsx';
import ProductPrice from './smallComponents/ProductPrice.jsx';
import ProductOffer from './smallComponents/ProductOffer.jsx';
import SocialShare from './smallComponents/SocialShare.jsx';
import Accordian from './productDetailSmallComponents/Accordian.jsx';

const lightMuiTheme = getMuiTheme(lightBaseTheme);



class AddCartBtn extends React.Component {

  constructor(props) {
    super(props);
    this.productSlug = window.location.href.split('/')[4];
    this.productID = window.location.href.split('/')[5];
    this.getProductDetail = this.getProductDetail.bind(this);
    this.getVarientChange = this.getVarientChange.bind(this);
    this.getPriceAndVarientId = this.getPriceAndVarientId.bind(this);
    this.allVarientSelected = this.allVarientSelected.bind(this);
    this.handleClickImage = this.handleClickImage.bind(this);
    this.checkDeliveryAvailibility = this.checkDeliveryAvailibility.bind(this);
    ProductStore.fetchProduct(this.productSlug, this.productID);
    this.state = {
      productData: null,
      value: 1,
      productVarient: null,
      errorTextCart: null,
      productPriceAndVarientId: {},
      btnCartState: false,
      productID: null,
      selectedValuesDict: {},
      openCartNotification: false,
      activeImage: null,
      isDeliveryAvailable: false,
      cartButtonLabel: 'Add to Cart'
    };
  }

  componentWillMount() {
    ProductStore.on("change", this.getProductDetail);
    ProductStore.on("change", this.checkDeliveryAvailibility)
  }


  componentWillUnmount() {
    ProductStore.removeListener("change", this.getProductDetail);
  }

  componentDidUpdate() {
    var step = 50;
    var scrolling = false;
    // Wire up events for the 'scrollUp' link:
    $("#scrollUp").bind("click", function (event) {
      var imageTileLength = document.getElementsByClassName('img-product')[0].height
      console.log(imageTileLength + "anuj")
      $(".ver-scroll").animate({
        scrollTop: "-=" + imageTileLength / 3 + "px"
      }, 10);
    })

    $("#scrollDown").bind("click", function (event) {
      var imageTileLength = document.getElementsByClassName('img-product')[0].height
      console.log(imageTileLength + "anuj")
      $(".ver-scroll").animate({
        scrollTop: "+=" + imageTileLength / 3 + "px"
      }, 10);
    })

  }

  getVarientChange(varient) {
    // for changing image on varient change
    var product_images_url = this.state.productData.product_images_url;
    for (var i = 0; i < product_images_url.length; i++) {
      for (var j = 0; j < product_images_url[i].varients.length; j++) {
        if (product_images_url[i].varients[j][varient.type] === varient.value && product_images_url[i]["id"] === varient.id) {
          this.handleClickImage(product_images_url[i].url);
          break;
        }
      }
    }
    if (this.allVarientSelected()) {
      this.setState({ btnCartState: true });
    }
    else {
      this.setState({ btnCartState: false });
    }
  }
  getPriceAndVarientId(data) {
    let productId = data.product_id;
    let varientId = data.product_varient_id;
    let productPriceAndVarientId = this.state.productPriceAndVarientId;
    productPriceAndVarientId[productId] = varientId
    this.setState({ productPriceAndVarientId }, this.checkDeliveryAvailibility());
  }
  allVarientSelected() {
    let productPriceAndVarientId = this.state.productPriceAndVarientId;
    let allVarients = this.state.productData.all_varients;
    for (let i = 0; i < allVarients.length; i++) {
      let pid = allVarients[i].product_id;
      if (productPriceAndVarientId[pid] === undefined) {
        return false;
      }
    }
    return true;
  }

  checkDeliveryAvailibility() {
    var isDeliveryAvailable = ProductStore.getPincodeDetails() ? ProductStore.getPincodeDetails().online : false;
    var allVarientSelected = this.allVarientSelected();
    this.setState({ btnCartState: allVarientSelected && isDeliveryAvailable })
  }

  getProductDetail() {
    this.setState({
      productData: ProductStore.getProductDetail(),
    });
    if (this.state.activeImage === null)
      this.setState({ activeImage: ProductStore.getProductDetail()['product_images_url'][0]['url'].replace('/th_', '/') });
  }


  handleAddToCart() {
    if (this.state.cartButtonLabel == "Add to Cart" && this.state.btnCartState) {
      var varientIds = [];
      var temp = this.state.productPriceAndVarientId;
      objectKeys(temp).map(function (productID) {
        varientIds.push(temp[productID])
      })
      ProductStore.addToCart(varientIds)
      this.setState({
        openCartNotification: true,
        cartButtonLabel: "Go to My Cart"
      })
    }
    else if (!this.state.btnCartState) {
      var $animation_elements = $('.pd-details');
      $animation_elements.addClass('shake');
      $('.container')[0].scrollIntoView();
    }
    else {
      window.location.href = "/my-cart/"
    }
  }

  handleClickImage(image) {
    this.setState({
      activeImage: image.replace('/th_', '/'),
    });
  }

  render() {
    const userAgent = window.navigator.userAgent;
    const isMobile = /mobile/i.test(userAgent);
    // console.log(isMobile, 'mobbbbsadsadfdsfs')
    const self = this;
    const productTitle = !this.state.productData ? null : this.state.productData['product_name'];
    const artistName = !this.state.productData ? null : this.state.productData['artist_name'];
    const artistProfileLink = !this.state.productData ? null : this.state.productData['artist_link'];
    const productDescription = !this.state.productData ? null : this.state.productData['product_main_description'];
    const productPrice = !this.state.productData ? null : parseInt(this.state.productData['product_price']).toLocaleString('en-IN', {
      maximumFractionDigits: 2,
      style: 'currency',
      currency: 'INR'
    });;
    const price = parseInt(!this.state.productData ? null : parseInt(this.state.productData['product_price']))
    const discount = parseInt(!this.state.productData ? null : parseInt(this.state.productData['discount_value']))
    const discountType = !this.state.productData ? null : this.state.productData['discount_type']
    const productBreadCrumb = !this.state.productData ? [] : this.state.productData['breadcrumb'];
    const productPriceAfterdiscount = function () {
      if (discountType == 'FLAT') {
        return (price - discount);
      }
      else {
        return (price - (price * discount / 100))
      }
    }().toLocaleString('en-IN', {
      maximumFractionDigits: 2,
      style: 'currency',
      currency: 'INR'
    });
    const imagesComponent = !this.state.productData || this.state.productData.length == 0 ? null : this.state.activeImage;

    const image = imagesComponent == null ? null :
      <ReactImageMagnify {...{
        largeImage: {
          alt: '',
          background: 'white',
          src: imagesComponent,
          width: 1500,
          height: 1500,
          enlargedImageStyle: { zIndex: 10 },
          enlargedImageContainerStyle: { zIndex: 10 },
          enlargedImageClassName: "fuck"
        },
        smallImage: {
          isFluidWidth: true,
          alt: 'Buy-' + productTitle + "at Addiction Bazaar",
          src: imagesComponent,
          srcSet: imagesComponent,
          sizes: "(min-width: 480px) 30vw, 80vw"
        }
      }} />
    const otherImages = !this.state.productData || this.state.productData.length == 0 ? null : this.state.productData['product_images_url'].map(function (image, i) {
      return (
        <div key={"image_" + i} style={{ padding: 2, paddingTop: 4 }}>
          <a onClick={self.handleClickImage.bind(this, image.url)}><img src={image.url} className="img-product" alt={"buy " + productTitle + " at Addiction Bazaar"} style={{ width: '100%' }} /></a>
        </div>
      )
    })
    const showTitle = this.state.productData ? this.state.productData.all_varients ? this.state.productData.all_varients.length === 1 ? true : false : false : false;
    const varientComponent = this.state.productData == null ? null : !this.state.productData.all_varients ? null : this.state.productData.all_varients.map(function (all_varient, i) {
      return (<div><ProductVarients key={i} getPriceAndVarientId={self.getPriceAndVarientId} varientChange={self.getVarientChange} showTitle={true} varients={all_varient} /><br /></div>)
    });
    const productOffers = this.state.productData ? this.state.productData['offers'].toString() : ""
    const sizeChartURL = !this.state.productData || this.state.productData.length == 0 ? null : this.state.productData['size_chart_url']
    const fbLink = "https://www.facebook.com/sharer/sharer.php?u=" + escape(window.location.href) + "&t=AddictionBazaar"
    const twitterLink = "https://twitter.com/share?url=" + escape(window.location.href) + "&text=AddictionBazaar"
    const gplusLink = "https://plus.google.com/share?url=" + escape(window.location.href)

    if (this.state.openCartNotification) {
      this.setState({ openCartNotification: false }, () => {
        toast.info("Porduct Added to the Cart");
      });
    }
    return (
      <MuiThemeProvider muiTheme={lightMuiTheme}>
        <div>
          <div id="content">
            <BreadCrumb bList={productBreadCrumb} />
            <div className="container" style={{ width: "auto" }}>
              <div className="col-md-12">
                <div className="col-sm-6 col-md-6">
                  <div className="col-sm-3 col-md-3">
                    <p className='txtc' id="scrollUp"><i className="arrow up"></i></p>
                    <div className="ver-scroll">
                      {otherImages}
                    </div>
                    <p className='txtc' id="scrollDown"><i className="arrow down"></i></p>
                  </div>
                  {!isMobile && <div className="col-sm-9 col-md-9 main-image">
                    {image}
                  </div>}
                </div>

                <div className="col-sm-6 col-md-6 pad-10-lr">
                  {artistName ? <div className="col-sm-12 col-md-12 col-xs-12">
                    <div className="col-sm-5 col-md-5 col-xs-7">
                      <ProductName isMobile={isMobile} name={productTitle} />
                      <VarientText isMobile={isMobile} />
                    </div>
                    <div className="col-sm-5 col-md-5 col-xs-5">
                      <ArtistName isMobile={isMobile} link={artistProfileLink} artistName={artistName} />
                    </div>
                    {!isMobile && <div className="col-sm-2 col-md-2">
                      <img src="/static/img/resource/trust-logo.png" alt="Trust Logo" style={{ maxWidth: "100%" }} />
                    </div>}
                  </div> : <div className="col-sm-12 col-md-12 col-xs-12">
                      <div className="col-sm-10 col-md-10 col-xs-10">
                        <ProductName isMobile={isMobile} name={productTitle} />
                        <VarientText isMobile={isMobile} />
                      </div>
                      {!isMobile && <div className="col-sm-2 col-md-2">
                        <img src="/static/img/resource/trust-logo.png" alt="Trust Logo" style={{ maxWidth: "100%" }} />
                      </div>}
                    </div>}
                  <br />
                  <div className="col-sm-12 col-md-12">
                    <div className="col-sm-5 col-md-5">
                      <ProductPrice productPriceAfterdiscount={productPriceAfterdiscount} productPrice={productPrice} discount={discount} />
                    </div>
                    <div className="col-sm-7 col-md-7">
                      <div className="offer-text" style={{ position: 'inherit', }}>
                        <ProductOffer offer={productOffers} />
                      </div>
                    </div>
                  </div>
                  <div className="col-sm-12 col-md-12">
                    <div className='animated pd-details'>
                      {varientComponent}
                      <p className="fix-width-250">{this.state.errorTextCart}</p>
                      <br />
                      <h3>Delivery/COD availablity</h3>
                      <DeliveryPincode isMobile={isMobile} />
                    </div>
                    <div className="col-sm-12 col-md-12">
                      <div className="col-sm-6 col-md-6">
                        <RaisedButton
                          backgroundColor={this.state.cartButtonLabel === "Go to My Cart" ? "#fff" : "#000"}
                          labelColor={this.state.cartButtonLabel === "Go to My Cart" ? "#000" : "#fff"}
                          label={this.state.cartButtonLabel}
                          className='cart-btn'
                          style={{ height: '56px' }}
                          overlayStyle={{ height: '56px', padding: '20px' }}
                          onTouchTap={self.handleAddToCart.bind(this)} />
                      </div>
                      <div className="col-sm-6 col-md-6">
                        <SocialShare fbLink={fbLink} gplusLink={gplusLink} twitterLink={twitterLink} />
                      </div>
                      <div className="col-sm-12 col-md-12 col-xs-12">
                        <Accordian title={isMobile ? 'Product Speciality' :'Addiction Bazar products are especially manufactured on order just for you'}
                          description={['100% COTTON', 'PRE-WASHED', 'NO SHRINKING', 'BIO-WASHED', 'SILICON WASHED', 'ANTI-PILL']} />
                      </div>
                      <div className="col-sm-12 col-md-12 col-xs-12">
                        <Accordian title='DESCRIPTION' description={productDescription} />
                      </div>
                    </div>
                  </div>
                </div>
                <div style={{background:'rgb(239, 239, 239)'}} className="col-sm-12 col-md-12 col-xs-12">
                  <div style={{borderRight: '1px solid #585858'}} className="col-sm-6 col-md-6 col-xs-12">
                    <Accordian title='Fabric Details'
                      markDown={true}
                      headerStyle={{paddingLeft: 10,}} 
                      // description={'scfdsfdfsdfsd'}
                      description={'100% cotton<br><b>Pre-washed</b> to give is soft touch & texture<br><b>Bio-washed</b> to give to finest quality Silicon wash to give fabric, its shine.<br /><br /><b><u>Washcare instrustions</u></b> Machine wash cold<br />Do not bleach or wash with chlorine based water or detergent Do not do iron directly on the prints Dry on flat surface as hanging may cause measurment variations'}
                       />
                  </div>
                  <div className="col-sm-6 col-md-6 col-xs-12">
                  </div>
                </div>
                <div>
                  <div className="col-xs-12 col-ms-6 pad-10">
                    <ul className="nav nav-tabs" role="tablist">
                      <li role="presentation">
                        <a href="#profile" aria-controls="profile" role="tab" data-toggle="tab">Size Chart</a>
                      </li>
                      <li role="presentation">
                        <a href="#messages" aria-controls="messages" role="tab" data-toggle="tab"></a>
                      </li>
                    </ul>

                    <div className="tab-content">
                      <div role="tabpanel" className="tab-pane" id="profile">
                        <img src={sizeChartURL} alt="Size Chart - Addiction Bazaar" />
                      </div>
                    </div>
                  </div>

                </div>
              </div>
            </div>
          </div>
          <HeaderUserCard />
        </div>
      </MuiThemeProvider>
    )
  }
}

export default AddCartBtn;