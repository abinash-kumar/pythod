import React from 'react';
import Checkbox from 'material-ui/Checkbox';
import Chip from 'material-ui/Chip';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import ProductModal from './ProductModal.jsx'
import HeaderUserCard from '../myaccount/HeaderUserCard.jsx'
import TagBanner from '../auraai/TagBanner.jsx';
import RaisedButton from 'material-ui/RaisedButton';
import Masonry from 'react-masonry-component';
import ProductStore from '../../store/ProductStore.jsx';
import { Tabs, Tab } from 'material-ui/Tabs';
import BreadCrumb from '../abcomponents/BreadCrumb.jsx';

import ProductFilter from './ProductFilter.jsx';


const lightMuiTheme = getMuiTheme(lightBaseTheme);
const styles = {
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
  },
  gridList: {
    display: 'flex',
    flexWrap: 'nowrap',
    overflowX: 'auto',
  },
  titleStyle: {
    color: 'rgb(0, 188, 212)',
  },
};
const tilesData = [
  {
    img: 'http://test.com:8000/static/myhome/images/req.jpg',
    title: 'Breakfast',
    author: 'jill111',
  },
  {
    img: 'http://test.com:8000/static/myhome/images/3.png',
    title: 'Tasty burger',
    author: 'pashminu',
  },
  {
    img: 'http://test.com:8000/static/myhome/images/4.jpg',
    title: 'Camera',
    author: 'Danson67',
  },
];


class ProductListing extends React.Component {

  constructor(props) {
    super(props);
    this.product = props['product'];
    this.getAllProducts = this.getAllProducts.bind(this);
    this.handleLoadMore = this.handleLoadMore.bind(this);
    this.getSelectedVarients = this.getSelectedVarients.bind(this);
    this.mainCategory = props['mainCategory'];
    this.banner = this.props['banner'];
    this.tag = function () {
      if (this.props['tags']) return this.props['tags'];

      if (window.location.pathname.split('/')[2] == 'tag') {
        return window.location.pathname.split('/')[3]
      }
    }.bind(this)();
    this.propVarient = function () {
      if (props['varients']) {
        return JSON.parse(props['varients']);
      }
      else {
        return {};
      }
    }();
    this.page = 0;
    this.isProductRendered = false;
    this.count = 0;
    this.items = [];
    this.loadingState = true;
    this.state = {
      getAllProducts: null,
      allCategoryVarient: null,
      jsonDataVarient: this.propVarient,
    };
    ProductStore.fetchAllProducts(this.product, this.tag, this.state.jsonDataVarient, this.page, null);
    // AuraaiStore.fetchTagProduct(this.product);
  }

  getAllProducts() {
    this.setState({
      allProductData: ProductStore.getAllProducts(),
      jsonDataVarient: ProductStore.getAllProducts().selected_varients,
      allCategoryVarient: ProductStore.getAllCategoryVarients(),
      // jsonDataVarient: ProductStore.getAllCategoryVarients() ? ProductStore.getAllCategoryVarients() : null,
    });
    this.product = ProductStore.getAllProducts()['categories'];
    let slug = ProductStore.getAllProducts().slug
    if (slug !== '' && slug) {
      history.pushState(null, null, "/products/" + slug);
    }
    isScrolledIntoView($('#main-footer'));
  }

  handleLoadMore() {
    this.loadingState = true;
    this.page = this.page + 1;
    ProductStore.fetchAllProducts(this.product, this.tag, this.state.jsonDataVarient, this.page);
    console.log("API CALLED");
  }

  componentWillMount() {
    ProductStore.on("change", this.getAllProducts);
  }

  componentWillUnmount() {
    ProductStore.removeListener("change", this.getAllProducts);
  }


  componentDidUpdate() {
    if (fixFilterCount <= 0) {
      $(function () {
        function slideMenu() {
          var activeState = $("#menu-container .menu-list").hasClass("active");
        }
        $("#menu-wrapper").unbind().click(function (event) {
          var activeState = $("#menu-container .menu-list").hasClass("active");
          if (activeState == false) {
            $("#hamburger-menu").addClass("open");
            $("#menu-container .menu-list").addClass("active");
            $("#menu-container .menu-list").animate(
              {
                left: "0%"
              },
              400
            );
            $("body").addClass("overflow-hidden");
          }
          else {
            $("#hamburger-menu").removeClass("open");
            $("#menu-container .menu-list").removeClass("active");
            $("#menu-container .menu-list").animate(
              {
                left: "-100%"
              },
              400
            );
            $("body").removeClass("overflow-hidden");
          }
        });
        $(".menu-list").find(".accordion-toggle").click(function () {
          $(this).next().toggleClass("open").slideToggle("fast");
          $(this).toggleClass("active-tab").find(".menu-link").toggleClass("active");

          $(".menu-list .accordion-content")
            .not($(this).next())
            .slideUp("fast")
            .removeClass("open");
          $(".menu-list .accordion-toggle")
            .not(jQuery(this))
            .removeClass("active-tab")
            .find(".menu-link")
            .removeClass("active");
        });
      }); // jQuery load
    }
    fixFilterCount = fixFilterCount + 1;
  }

  handleClickCategory(categorySlug) {
    this.items = [];
    this.isProductRendered = false;
    this.page = 0;
    this.setState({
      // jsonDataVarient: null,
      allProductData: null,
    })
    ProductStore.fetchAllProducts(null, null, null, null, categorySlug);
  }

  getSelectedVarients(varients) {
    // get Varients from Produc filter component
    this.items = [];
    this.isProductRendered = false;
    this.page = 0;
    this.setState({ jsonDataVarient: varients, allProductData: null, });
    ProductStore.fetchAllProducts(this.product, this.tag, varients, this.page);
  }

  render() {
    const self = this;
    const isMobile = window.innerWidth <= 500 || getValueOfParam('mobile');
    const allProductData = this.state.allProductData;
    document.title = !allProductData ? "Addiction Bazaar" : allProductData.page_title == undefined ? "Addiction Bazaar" : allProductData.page_title;
    const allCategoryVarient = this.state.allCategoryVarient;
    const productBreadCrumb = !this.state.allProductData ? [] : this.state.allProductData['breadcrumb'];
    const heading = !this.state.allProductData ? null : this.state.allProductData['heading'] ? <center><h1>{this.state.allProductData['heading']}</h1></center> : null;
    let ProductComponent = !allProductData ? null : allProductData.product_detail_list === undefined ? null : allProductData.product_detail_list.map((product) =>
      (
        <div key={product['id']} className='col-sm-4 col-md-4 col-xs-6 deisgner-product'>
          <ProductModal productSlug={product['slug']} productID={product['id']} product={product} />
        </div>
      )
    );
    if (ProductComponent && !this.isProductRendered) {
      this.items.push(ProductComponent);
      this.count = ProductStore.getProductInEachPage()
      this.isProductRendered = true;
      this.loadingState = false;
      $("#loaderClass").removeClass("loader");
    }

    if (this.page != 0 && ProductStore.getProductsPageno() == this.page) {
      this.items.push(ProductComponent);
      this.count = this.count + ProductStore.getProductInEachPage()
    }

    if (this.items && this.count < ProductStore.getAllProductsCount()) {
      this.loadingState = false;
    }
    else {
      this.loadingState = true;
    }
    if (this.items && this.count <= ProductStore.getAllProductsCount()) {
      this.loader = false;
    }
    else {
      this.loader = true;
    }
    const classLoader = "content-side";

    const banner = function () {
      if (self.banner) {
        return (
          <TagBanner />
        )
      }
    }();

    let categoryLinks = null;
    let mainCategory = this.mainCategory;
    categoryLinks = !mainCategory ? null : Object.keys(JSON.parse(mainCategory)).map(function (key, index) {
      return (
        <li key={key} onClick={self.handleClickCategory.bind(self, key)}>{JSON.parse(mainCategory)[key]}</li>
      )
    });

    $(document).ready(function () {
      var win = $(window);
      // Each time the user scrolls
      win.scroll(function () {
        // End of the document reached?
        if ($(document).height() - win.height() <= win.scrollTop() + (win.height()) * 2) {
          console.log(self.loadingState)
          if (!self.loadingState) {
            self.handleLoadMore();
          }
        }
      });
    });

    return (
      <MuiThemeProvider muiTheme={lightMuiTheme}>
        <div>
          <BreadCrumb bList={productBreadCrumb} />
          <div style={styles.root}>
            <div id="loaderClass" className={classLoader}>
              {this.state.allCategoryVarient ? isMobile ? <div className="container-90">
                <div className="container">
                  {heading}
                  <div className='flex-list'>
                    <ul>{categoryLinks}</ul>
                  </div>
                </div>
                {banner}
                <ProductFilter selectedVarients={this.state.jsonDataVarient} isMobile={isMobile} getVarients={this.getSelectedVarients} allVarients={this.state.allCategoryVarient} />
                <Masonry>{this.items}</Masonry>
              </div> :
                <div className="col-sm-12 col-md-12 col-xs-12">
                  <div className="col-sm-2 col-md-2 col-xs-2">
                    <br />
                    <div className="filter-scroll-bar sticky-filter" id="filter-product-listing">
                      <ProductFilter selectedVarients={this.state.jsonDataVarient} isMobile={isMobile} getVarients={this.getSelectedVarients} allVarients={this.state.allCategoryVarient} />
                    </div>
                  </div>
                  <div className="col-sm-10 col-md-10 col-xs-10 pad-10 ">
                    <div className="container">
                      {heading}
                      <div className='flex-list'>
                        <ul>{categoryLinks}</ul>
                      </div>
                    </div>
                    {banner}
                    <Masonry>{this.items}</Masonry>
                  </div>
                </div> : <div className="container-90">
                  <div className="container">
                    {heading}
                    <div className='flex-list'>
                      <ul>{categoryLinks}</ul>
                    </div>
                  </div>
                  {banner}
                  <Masonry>{this.items}</Masonry>
                </div>
              }
            </div>
            <HeaderUserCard />
            <div className='row pad-10'>
              <br />
              <div style={{ position: 'relative', top: 35, visibility: self.loader ? "visible" : "hidden" }}>
                <div className="leftEye"></div>
                <div className="rightEye"></div>
                <div className="mouth"></div>
              </div>
            </div>
          </div>
        </div>
      </MuiThemeProvider>
    )
  }
}

export default ProductListing;