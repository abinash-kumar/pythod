var AppDispatcher = require('../dispatcher/Dispatcher.jsx');
var AppConstants = require('../constants/Constants');

export function updateImages(image, activeImage) {
  AppDispatcher.dispatch({
    type: "RECEIVE_IMAGES",
    image, activeImage,
  });
}