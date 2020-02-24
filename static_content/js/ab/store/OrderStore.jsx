import { EventEmitter } from 'events';
import dispatcher from '../dispatcher/Dispatcher.jsx'
import API from './API'
import Const from '../constants/Constants';
import * as UserActions from "../actions/UserActions.jsx";

class OrderStore extends EventEmitter {

	constructor() {
		super()
		this.order_details = null;
		this.order_price = null;
	}

	fetchOrderDetailOfUser(
		transaction_id,
		name,
		address,
		city,
		state,
		pincode,
		mobile,
		email,
	) {
		API.getOrderDetailOfUser(
			transaction_id,
			name,
			address,
			city,
			state,
			pincode,
			mobile,
			email,
			(function (data) {
				console.log(data)
				UserActions.getOrderDetailOfUser(data)
			}).bind(this));
	}

	getOrderDetailOfUser() {
		return this.order_details;
	}

	getordersPrice() {
		return this.order_price;
	}


	handleAction(action) {
		switch (action.type) {
			case Const.RECEIVE_ORDER_USER_DETAILS: {
				this.order_details = action.order_details['order_list'];
				this.order_price = action.order_details;
				this.emit("change")
				break;
			}
				break;
		}
	}
}

const orderstore = new OrderStore;
dispatcher.register(orderstore.handleAction.bind(orderstore));
export default orderstore;