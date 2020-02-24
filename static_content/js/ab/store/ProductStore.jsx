import { EventEmitter } from 'events';
import dispatcher from '../dispatcher/Dispatcher.jsx'
import API from './API'
import Const from '../constants/Constants';

class ProductStore extends EventEmitter {

	constructor() {
		super();
		this.data = [];
		this.allProductData = {};
		this.allCategoryVarient = [];
		this.allProductVarient = [];
		this.productPriceAndVarientID = {};
		this.pincode = null;
		this.category = null;
	}

	fetchProduct(slug, id) {
		API.fetchProduct(slug, id);
	}

	fetchPincode(pincode) {
		API.deliveryPincodeCheck(pincode);
	}

	getPincodeDetails() {
		return this.pincode
	}

	getProductDetail() {
		return this.data
	}

	getProductVarientDetail() {
		return this.allProductVarient;
	}

	getAllProducts() {
		return this.allProductData
	}

	getAllProductsCount() {
		return this.allProductData['total_number_of_products']
	}

	getProductInEachPage() {
		return this.allProductData['no_of_products']
	}

	getProductsPageno() {
		return this.allProductData['page']
	}

	getAllCategoryVarients() {
		return this.allCategoryVarient;
	}

	getProductPriceAndVarientID() {
		return this.productPriceAndVarientID;
	}

	fetchAllCategoryVarient(product) {
		API.fetchAllCategoryVarient(product);
	}

	fetchAllProducts(product, tag, varients, page, slug) {
		if (tag) {
			API.fetchTagProduct(product, tag, varients, page);
		}
		else {
			API.fetchAllProducts(product, tag, varients, page, slug);
		}
	}

	fetchProductVarient(product, id) {
		API.fetchProductVarient(product, id);
	}

	fetchProductPriceVarientID(id, varients) {
		API.fetchProductPriceVarientID(id, varients);
	}

	addToCart(varientId) {
		API.addToCart(varientId);
	}

	handleAction(action) {
		switch (action.type) {
			case Const.RECEIVE_PRODUCT_DETAILS: {
				this.data = action.data;
				this.emit("change")
				break;
			}
			case Const.RECEIVE_ALL_PRODUCTS: {
				this.allProductData = action.data;
				this.allCategoryVarient = action.data.varients;
				this.emit("change")
				break;
			}
			case Const.RECEIVE_ALL_PRODUCT_VARIENTS: {
				this.allProductVarient = action.data;
				this.emit("change")
				break;
			}
			case Const.RECEIVE_PRODUCT_PRICE_AND_VARIENTS: {
				this.productPriceAndVarientID = action.data;
				this.emit("change")
				//remove it
				break;
			}
			case Const.RECEIVE_PINCODE_STATUS: {
				this.pincode = action.data;
				this.emit("change")
				break;
			}
				break;
		}
	}



}

const productStore = new ProductStore;
dispatcher.register(productStore.handleAction.bind(productStore));
export default productStore;