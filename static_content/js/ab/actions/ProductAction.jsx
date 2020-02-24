var AppDispatcher = require('../dispatcher/Dispatcher.jsx');
var AppConstants = require('../constants/Constants');

export function getProductDetails(data) {
  AppDispatcher.dispatch({
    type: AppConstants.RECEIVE_PRODUCT_DETAILS,
    data,
  });
}

export function getAllProductDetails(data) {
  AppDispatcher.dispatch({
    type: AppConstants.RECEIVE_ALL_PRODUCTS,
    data,
  });
}


export function getAllProductVarient(data) {
  AppDispatcher.dispatch({
    type: AppConstants.RECEIVE_ALL_PRODUCT_VARIENTS,
    data,
  });
}

export function getProductPriceAndVarientID(data) {
  AppDispatcher.dispatch({
    type: AppConstants.RECEIVE_PRODUCT_PRICE_AND_VARIENTS,
    data,
  });
}

export function getPincodeStatus(data) {
  AppDispatcher.dispatch({
    type: AppConstants.RECEIVE_PINCODE_STATUS,
    data,
  });
}