import { EventEmitter } from 'events';
import dispatcher from '../dispatcher/Dispatcher.jsx'
import API from './API'
import Const from '../constants/Constants';
import * as SliderActions from "../actions/SliderActions.jsx";
import * as UserActions from "../actions/UserActions.jsx";

class UserStore extends EventEmitter {

	constructor() {
		super()
		this.user_full_name = null;
		this.user_email = null;
		this.user_mobile = null;
		this.email_sent = false;
		this.cartCount = 0;
		this.is_authenticated = false;
		this.share_link = null;
		this.artist_details = null;
		this.artist_public_profile_detail = null;
		this.userWalletData = [];
		this.fb_text = null;
		this.fb_link = null;
	}

	fetchUserBasicDetails() {
		API.getUserDetail((function (data) {
			if (data.is_authenticated == undefined) {
				this.user_full_name = data.user_full_name;
				this.user_email = data.user_email;
				this.user_mobile = data.user_mobile;
				this.user_photo = data.user_photo;
				this.orders = data.orders_list;
				this.customer_details = data.customer_details;
				this.is_authenticated = true;
				this.cartCount = data.cart_count;
				this.fb_text = data.fb_text;
				this.fb_link = data.fb_link;
				UserActions.updateUserDetails(this.user_full_name, this.user_email, this.user_mobile, this.user_photo, this.orders, this.customer_details, this.cartCount, this.fb_link, this.fb_text)
			}
			else {
				this.is_authenticated = data.is_authenticated;
				this.cartCount = data.cart_count;
				this.fb_text = data.fb_text;
				this.fb_link = data.fb_link;
				UserActions.updateUserIfNotAuthenticated(this.is_authenticated, this.cartCount, this.fb_link, this.fb_text);
			}
		}).bind(this));
		return this.images
	}

	updateCustomerAddress(name, address, city, state, pincode, mobile, email) {
		API.updateNewAddress(name, address, city, state, pincode, mobile, email, (function (data) {
			console.log(this.customer_details)
			this.customer_details = data.customer_details;
			console.log(this.customer_details)
			UserActions.updateUserDetails(this.user_full_name, this.user_email, this.user_mobile, this.user_photo, this.orders, this.customer_details, this.cartCount);
		}).bind(this));

	}

	updateUserDetailsAfterMobileVerification(mobile) {
		this.customer_details['is_mobile_verified'] = true;
		this.user_mobile = mobile;
		UserActions.updateUserDetails(this.user_full_name, this.user_email, this.user_mobile, this.user_photo, this.orders, this.customer_details, this.cartCount)
	}

	getUserDetail() {
		return [this.user_full_name, this.user_email, this.user_mobile, this.user_photo, this.orders, this.customer_details]
	}

	isUserAuthenticatedAndMobileVerified() {
		return this.is_authenticated && this.customer_details['is_mobile_verified'];
	}

	is_user_authenticated() {
		return this.is_authenticated && true;
	}

	get_email_sent_status() {
		return this.email_sent;
	}

	getCartCount() {
		return this.cartCount;
	}

	getUserFullName() {
		return this.user_full_name;
	}

	updateUserSignInStatus(value) {
		this.is_authenticated = value;
	}

	fetchArtistDetails() {
		API.fetchArtistDetails();
	}

	fetchArtistPublicProfile(artistId) {
		API.fetchArtistPublicProfile(artistId);
	}

	fetchUserWallet() {
		API.fetchUserWallet();
	}

	getUserWallet() {
		return this.userWalletData;
	}

	getArtistDetails() {
		return this.artist_details;
	}

	getArtistPublicProfileDetails() {
		return this.artist_public_profile_detail;
	}

	getMagicSearchBtnLink() {
		return this.fb_link;
	}
	getMagicSearchBtnText() {
		return this.fb_text;
	}

	is_logged_in_user_is_artist() {
		return this.is_authenticated && this.customer_details ? this.customer_details['is_artist'] : false;
	}

	handleAction(action) {
		switch (action.type) {
			case Const.RECEIVE_USER_DETAILS: {
				this.user_full_name = action.user_full_name;
				this.user_email = action.user_email;
				this.user_mobile = action.user_mobile;
				this.user_photo = action.user_photo;
				this.orders = action.orders;
				this.customer_details = action.customer_details;
				this.is_authenticated = true;
				this.cartCount = action.cart_count;
				this.fb_link = action.fb_link;
				this.fb_text = action.fb_text;
				this.emit("change")
				break;
			}
			case Const.RECIEVE_IS_USER_AUTHENTICATED: {
				this.is_authenticated = action.is_authenticated;
				this.cartCount = action.cart_count;
				this.emit("change")
				break;
			}
			case Const.UPDATE_EMAIL_SENT_STATUS: {
				this.email_sent = action.data.success;
				this.emit("change")
				break;
			}
			case Const.UPDATE_CART: {
				this.cartCount = this.cartCount + 1;
				this.emit("change")
				break;
			}
			case Const.SIGNIN_STATUS: {
				this.is_authenticated = true;
				this.emit("change")
				break;
			}
			case Const.RECEIVE_ARTIST_DETAILS: {
				this.artist_details = action.data;
				this.emit("change")
				break;
			}
			case Const.RECEIVE_ARTIST_PUBLIC_PROFILE: {
				this.artist_public_profile_detail = action.data;
				this.emit("change")
				break;
			}
			case Const.RECEIVE_USER_WALLET: {
				this.userWalletData = action.data;
				this.emit("change")
				break;
			}
			case Const.RECEIVE_REDEEM_VALUE: {
				if (!action.data.error) {
					setCookie('coupon', '', -1)
					this.userWalletData.money_list.push(action.data);
				}
				this.emit("change")
				break;
			}
				break;
		}
	}
}

const userstore = new UserStore;
dispatcher.register(userstore.handleAction.bind(userstore));
export default userstore;