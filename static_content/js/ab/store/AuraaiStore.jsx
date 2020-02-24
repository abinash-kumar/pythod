import { EventEmitter } from 'events';
import dispatcher from '../dispatcher/Dispatcher.jsx'
import API from './API'
import Const from '../constants/Constants';


class AuraaiStore extends EventEmitter {
    constructor(){
		super();
		this.searchTagProducts = [];
		this.allBanners = [];
		this.autoCompleteKeys =[];
	}
    
    fetchTagProduct(product){
    	if (product=='tshirt'){
    		API.fetchTagProduct();
    	}
    }
	
	fetchAutocompleteKeys(autocomplete_key){
		API.fetchAutocompleteKeys(autocomplete_key);
	}
	fetchAllBanners(){
		API.fetchAllBanners();
    }
		
    getTagSearchProducts(){
		return this.searchTagProducts
	}

	getAllBanners(){
		return this.allBanners
	}
	
	
	getAutocompleteKeys(){
		return this.autoCompleteKeys
	}

    handleAction(action){
		switch (action.type){
            case Const.RECEIVE_TAG_SEARCH_PRODUCTS: {
				this.searchTagProducts = action.data;
				this.emit("change")
				break;
			}
			case Const.RECEIVE_ALL_BANNERS: {
				this.allBanners = action.data;
				this.emit("change")
				break;
			}
			case Const.AUTOCOMPLETE_KEYS: {
				this.autoCompleteKeys = action.data;
				this.emit("change")
				break;
			}
			break;
        }
    }
}


const auraaiStore = new AuraaiStore;
dispatcher.register(auraaiStore.handleAction.bind(auraaiStore));
export default auraaiStore;