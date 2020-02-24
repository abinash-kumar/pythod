import React from 'react';
import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';
import ProductStore from '../../store/ProductStore.jsx';
import RaisedButton from 'material-ui/RaisedButton';
import DeliveryPincode from './DeliveryPincode.jsx'
import ProductVarients from './ProductVarientsNew.jsx';


class ProductVarientsContainer extends React.Component {
  constructor(props) {
    super(props);
    this.getVarientChange = this.getVarientChange.bind(this);
    this.getPriceAndVarientId = this.getPriceAndVarientId.bind(this);
    this.allVarientSelected = this.allVarientSelected.bind(this);
    this.checkDeliveryAvailibility = this.checkDeliveryAvailibility.bind(this);
    this.getProductDetail = this.getProductDetail.bind(this);
    this.type = props['submitType']
    this.state = {
      productData: ProductStore.getProductDetail(),
      selectedValuesDict: {},
      productPriceAndVarientId: {},
      btnCartState: false,
      productID: this.props.product_id,
      dropdownState: false,
      isDeliveryAvailable: false,
    };
    //ProductStore.fetchProduct(this.productSlug, this.productID);
    //ProductStore.fetchProductVarient('tshirt', this.state.productID);

  }

  getProductDetail() {
    this.setState({
      productData: ProductStore.getProductDetail(),
    });
  }

  checkDeliveryAvailibility() {
    var isDeliveryAvailable = ProductStore.getPincodeDetails() ? ProductStore.getPincodeDetails().online : false;
    var allVarientSelected = this.allVarientSelected();
    this.setState({ btnCartState: allVarientSelected && isDeliveryAvailable })
  }

  componentWillMount() {
    ProductStore.on("change", this.getProductDetail);
    ProductStore.on("change", this.checkDeliveryAvailibility);
  }


  componentWillUnmount() {
    ProductStore.on("change", this.getProductDetail);
  }


  handleAddToCart() {
    if (this.state.btnCartState) {
      var varientIds = [];
      var temp = this.state.productPriceAndVarientId;
      objectKeys(temp).map(function (productID) {
        varientIds.push(temp[productID])
      })
      ProductStore.addToCart(varientIds)
      if (this.props.submitType === "Buy Now") {
        window.location.href = "/my-cart/"
      }
      this.props.req_close_modal();
    }
    else {
      var $animation_elements = $('.pd-details');
      $animation_elements.addClass('shake');
      $('.mybox')[0].scrollIntoView();
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

  getVarientChange(varient) {
    // for changing image on varient change
    // var product_images_url = this.state.productData.product_images_url;
    // for (var i = 0; i < product_images_url.length; i++) {
    //   for (var j = 0; j < product_images_url[i].varients.length; j++) {
    //     if (product_images_url[i].varients[j][varient.type] === varient.value && product_images_url[i]["id"] === varient.id) {
    //       this.handleClickImage(product_images_url[i].url);
    //       break;
    //     }
    //   }
    // }
    if (this.allVarientSelected()) {
      this.setState({ btnCartState: true });
    }
    else {
      this.setState({ btnCartState: false });
    }
  }


  render() {
    var self = this;
    const varientComponent = this.state.productData == null ? null : !this.state.productData.all_varients ? null : this.state.productData.all_varients.map(function (all_varient, i) {
      return (<div><ProductVarients key={i} getPriceAndVarientId={self.getPriceAndVarientId} varientChange={self.getVarientChange} showTitle={true} varients={all_varient} /><br /></div>)
    });

    return (
      <div className="varientsList">
        {varientComponent}
        <br />
        <DeliveryPincode />
        <RaisedButton label={this.type} style={{ margin: 12 }} onTouchTap={self.handleAddToCart.bind(this)} disabled={!this.state.btnCartState} />

      </div>
    );
  }
}

export default ProductVarientsContainer;