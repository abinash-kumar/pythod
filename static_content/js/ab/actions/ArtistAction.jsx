var AppDispatcher = require('../dispatcher/Dispatcher.jsx');
var AppConstants = require('../constants/Constants');


export function getArtistDesign(data) {
  AppDispatcher.dispatch({
    type: AppConstants.RECEIVE_ARTIST_DESIGNS,
    data,
  });
}

export function getArtistSocialLinks(data) {
  AppDispatcher.dispatch({
    type: AppConstants.RECEIVE_ARTIST_SOCIAL_LINKS,
    data,
  });
}

export function getArtistOtherDetails(data) {
  AppDispatcher.dispatch({
    type: AppConstants.RECEIVE_ARTIST_OTHER_DETAILS,
    data,
  });
}

export function getArtistBankDetails(data) {
  AppDispatcher.dispatch({
    type: AppConstants.RECEIVE_ARTIST_BANK_DETAILS,
    data,
  });
}

export function getAllArtist(data) {
  AppDispatcher.dispatch({
    type: AppConstants.RECEIVE_ALL_ARTIST,
    data,
  });
}