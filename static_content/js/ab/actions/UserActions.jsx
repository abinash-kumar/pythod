var AppDispatcher = require('../dispatcher/Dispatcher.jsx');
var AppConstants = require('../constants/Constants');

export function updateUserDetails(user_full_name, user_email, user_mobile, user_photo, orders, customer_details, cart_count, fb_link, fb_text) {
  AppDispatcher.dispatch({
    type: "RECEIVE_USER_DETAILS",
    user_full_name, user_email, user_mobile, user_photo, orders, customer_details, cart_count, fb_link, fb_text,
  });
}

export function updateUserIfNotAuthenticated(is_authenticated, cart_count, fb_link, fb_text) {
	AppDispatcher.dispatch({
		type: "RECIEVE_IS_USER_AUTHENTICATED",
		is_authenticated, cart_count, fb_link, fb_text,
	})
}

export function getOrderDetailOfUser(order_details) {
  AppDispatcher.dispatch({
    type: "RECEIVE_ORDER_USER_DETAILS",
    order_details,
  });
}

export function getEmailSentStatus(data) {
  AppDispatcher.dispatch({
    type: "UPDATE_EMAIL_SENT_STATUS",
    data,
  });
}

export function updateCart() {

  AppDispatcher.dispatch({
    type: "UPDATE_CART",
  });
}

export function updateSignInStatus() {

  AppDispatcher.dispatch({
    type: "SIGNIN_STATUS",
  });
}

export function getArtistDetails(data) {
  AppDispatcher.dispatch({
    type: AppConstants.RECEIVE_ARTIST_DETAILS,
    data,
  });
}

export function getArtistDesigns(data) {
  AppDispatcher.dispatch({
    type: AppConstants.RECEIVE_ARTIST_DESIGNS,
    data,
  });
}

export function getArtistPublicProfile(data) {
  AppDispatcher.dispatch({
    type: AppConstants.RECEIVE_ARTIST_PUBLIC_PROFILE,
    data,
  });
}

export function getUserWallet(data) {
  AppDispatcher.dispatch({
    type: AppConstants.RECEIVE_USER_WALLET,
    data,
  });
}

export function getNewRedeemValue(data) {
  AppDispatcher.dispatch({
    type: AppConstants.RECEIVE_REDEEM_VALUE,
    data,
  });
}