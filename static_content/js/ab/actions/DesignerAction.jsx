var AppDispatcher = require('../dispatcher/Dispatcher.jsx');
var AppConstants = require('../constants/Constants');

export function getAllDesignerDetails(data) {
  AppDispatcher.dispatch({
    type: AppConstants.RECEIVE_DESIGNER_DETAILS,
    data,
  });
}