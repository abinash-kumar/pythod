import { EventEmitter } from 'events';
import dispatcher from '../dispatcher/Dispatcher.jsx'
import API from './API'
import Const from '../constants/Constants';

class DesignerStore extends EventEmitter {

	constructor(){
		super();
		this.data = [];
	}

	fetchDesigners(value){
		API.fetchDesigners(value);
	}

	getPremiumDesignerDetails(){
		return this.data
	}

	handleAction(action){
		switch (action.type){
			case Const.RECEIVE_DESIGNER_DETAILS: {
				this.data = action.data;
				this.emit("change")
        		break;
			}
			break;
		}
	}



}

const designerStore = new DesignerStore;
dispatcher.register(designerStore.handleAction.bind(designerStore));
export default designerStore;