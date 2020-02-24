var AppDispatcher = require('../dispatcher/Dispatcher.jsx');
var AppConstants = require('../constants/Constants');


export function getTagSearchProducts(data) {
  AppDispatcher.dispatch({
    type: AppConstants.RECEIVE_TAG_SEARCH_PRODUCTS,
    data,
  });
}

export function getAllBanners(data) {
  AppDispatcher.dispatch({
    type: AppConstants.RECEIVE_ALL_BANNERS,
    data,
  });
}

export function getAutocompleteKeys(data) {
  AppDispatcher.dispatch({
    type: AppConstants.AUTOCOMPLETE_KEYS,
    data,
  });
}
