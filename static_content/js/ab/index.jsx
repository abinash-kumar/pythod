import "babel-polyfill";
import React from 'react';
import ReactDOM from 'react-dom';
import Slider from './components/Slider.jsx';
import DesignerHome from './components/Designers.jsx';
import DesignerSignUp from './components/DesignerSignUp.jsx';
import DesignerSignUpPopUp from './components/DesignerSignUpPopUp.jsx'
import Home from './components/Home.jsx';
import DesignerProfile from './components/DesignerProfile.jsx';
import UserProfile from './components/myaccount/UserProfile.jsx'
import RedeemPromoCode from './components/myaccount/RedeemPromoCode.jsx'
import OrderCheckout from './components/checkout/OrderCheckout.jsx'
import ProductListing from './components/product/ProductListing.jsx'
import AddCartBtn from './components/product/AddCartBtn.jsx'
import ProductTagSearch from './components/auraai/ProductTagSearch.jsx';
import ProductSearch from './components/auraai/ProductSearch.jsx';
import FbMagicSearch from './components/auraai/FbMagicSearch.jsx';
import ProductSearchPage from './components/auraai/ProductSearchPage.jsx';
import ArtistDetails from './components/myaccount/ArtistDetails.jsx';
import EditProfile from './components/myaccount/EditProfile.jsx';
import DeliveryPincode from './components/product/DeliveryPincode.jsx';
import ArtistDesigns from './components/artist/ArtistDesigns.jsx';
import ArtistHome from './components/artist/ArtistHome.jsx';
import ArtistAll from './components/artist/ArtistAll.jsx';
import ArtistProfile from './components/artist/ArtistProfile.jsx';
import SignInAndUp from './components/myaccount/SignInAndUp.jsx';
import ForgetPasswordPopUp from './components/myaccount/ForgetPasswordPopUp.jsx';
import TagBanner from './components/auraai/TagBanner.jsx';
import { render } from 'react-dom';
import ImageStore from './store/Store.jsx';
import injectTapEventPlugin from 'react-tap-event-plugin';
import { BrowserRouter } from 'react-router-dom';
import { Switch, Route } from 'react-router-dom';
import HeaderMenu from './components/HeaderMenu.jsx';


injectTapEventPlugin();

var createReactClass = require('create-react-class');

var AppUser = function () {
	return (
		<UserProfile />
	);
}


var AppOrderCheckout = function () {
	return (
		<OrderCheckout />
	);
}

module.exports = AppUser;
module.exports = AppOrderCheckout;

function topFunction() {
	document.body.scrollTop = 0; // For Safari
	document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}
var ProductListingWrapper = createReactClass({
	render: function () {
		var dataVarients = document.getElementById('product-page').dataset.varient;
		var category = document.getElementById('product-page').dataset.category;
		var mainCategory = document.getElementById('product-page').dataset.maincategory;
		var comboType = document.getElementById('product-page').dataset.combotype;
		document.body.scrollTop = 0;
		document.documentElement.scrollTop = 0;
		return (<ProductListing product={category} banner={false} varients={dataVarients} mainCategory={mainCategory} />);
	}
});

if (document.getElementById('home')) {
	ReactDOM.render(<Home />, document.getElementById('home'));
}

if (document.getElementById('user-profile')) {
	ReactDOM.render(<AppUser />, document.getElementById('user-profile'));
}
if (document.getElementById('final-checkout')) {
	ReactDOM.render(<OrderCheckout />, document.getElementById('final-checkout'));
}

if (document.getElementById('designers')) {
	ReactDOM.render(<DesignerHome />, document.getElementById('designers'));
}

if (document.getElementById('des-signup')) {
	ReactDOM.render(<DesignerSignUp user='designer' />, document.getElementById('des-signup'));
}

if (document.getElementById('art-signup')) {
	ReactDOM.render(<DesignerSignUp user='artist' />, document.getElementById('art-signup'));
}

if (document.getElementById('product-page')) {
	ReactDOM.render(<ProductListingWrapper />, document.getElementById('product-page'));
}

if (document.getElementById('t-shirt-sub')) {
	ReactDOM.render(
		<div>
			<nav>
				<ul className="breadcrumb">
					<li><a href="/" rel="index up up up">home</a></li>
					<li><a href="/tshirt/" rel="up up">products</a></li>
				</ul>
			</nav>
			<ProductListing product="tshirt" banner={false} />
		</div>, document.getElementById('t-shirt-sub'));
}

if (document.getElementById('designers-profile')) {
	ReactDOM.render(<DesignerProfile />, document.getElementById('designers-profile'));
}

if (document.getElementById('artist-profile')) {
	ReactDOM.render(<DesignerProfile isArtistProfile={true} />, document.getElementById('artist-profile'));
}

if (document.getElementById('add-cart')) {
	ReactDOM.render(<AddCartBtn />, document.getElementById('add-cart'));
}

if (document.getElementById('product-tag-search')) {
	ReactDOM.render(<ArtistDetails />, document.getElementById('product-tag-search'));
}
if (document.getElementById('tag-banner')) {
	ReactDOM.render(<TagBanner />, document.getElementById('tag-banner'));
}
if (document.getElementById('artist-design')) {
	ReactDOM.render(<ArtistHome />, document.getElementById('artist-design'));
}
if (document.getElementById('user-register')) {
	ReactDOM.render(<SignInAndUp register={true} />, document.getElementById('user-register'));
}
if (document.getElementById('edit-profile')) {
	ReactDOM.render(<EditProfile />, document.getElementById('edit-profile'));
}
if (document.getElementById('coupon-box')) {
	ReactDOM.render(<RedeemPromoCode type='TRANSACTIONAL' />, document.getElementById('coupon-box'));
}
if (document.getElementById('forget-password')) {
	ReactDOM.render(<ForgetPasswordPopUp />, document.getElementById('forget-password'));
}
if (document.getElementById('artist-profile-new')) {
	ReactDOM.render(<ArtistProfile />, document.getElementById('artist-profile-new'));
}
if (document.getElementById('artist-all')) {
	ReactDOM.render(<ArtistAll />, document.getElementById('artist-all'));
}
if (document.getElementById('product-search')) {
	ReactDOM.render(<ProductSearchPage />, document.getElementById('product-search'));
}
if (document.getElementById('fb-magic-search')) {
	ReactDOM.render(<FbMagicSearch />, document.getElementById('fb-magic-search'));
}

if (document.getElementById('header-menu')) {
	ReactDOM.render(<HeaderMenu />, document.getElementById('header-menu'));
}

if (document.getElementById('varient-wise-listing')) {
	var category = window.location.pathname.split('/')[3];
	var varients = window.location.pathname.split('/')[4];
	ReactDOM.render(<ProductListing product={category} varients={varients} banner={true} />, document.getElementById('varient-wise-listing'));
}
if (document.getElementById('other-user-signup')) {
	ReactDOM.render(<DesignerSignUpPopUp />, document.getElementById('other-user-signup'));
}

if (document.getElementById('cfblog-prodcut-page')) {
	let tags = document.getElementById('cfblog-prodcut-page').getAttribute('tags');
	ReactDOM.render(<ProductListing product="search" tags={tags} banner={false} />, document.getElementById('cfblog-prodcut-page'));
}