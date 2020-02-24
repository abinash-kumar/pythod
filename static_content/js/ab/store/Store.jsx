import { EventEmitter } from 'events';
import dispatcher from '../dispatcher/Dispatcher.jsx'
import API from './API'
import Const from '../constants/Constants';
import * as SliderActions from "../actions/SliderActions.jsx";

class ImageStore extends EventEmitter{

	constructor(){
		super()
		this.images = []
		this.activeImage = []
	}

	fetchImages(onPage, path){
		API.getImages(onPage, path, (function(data){
				this.images = this.images.concat(data.slider_list);
				this.activeImage = this.activeImage.concat(data.active_slider);
				SliderActions.updateImages(this.images, this.activeImage)
			}).bind(this));
		return this.images
	}

	getImages(){
		return [this.images, this.activeImage]
	}

	handleAction(action){
		switch (action.type){
			case Const.LOAD_IMG_SLIDER: {
				this.getImages()
			}
			case Const.RECEIVE_IMAGES: {
				this.images = action.image;
				this.activeImage = action.activeImage;
				this.emit("change")
        		break;
			}
			break;
		}
	}
}

const sliderStore = new ImageStore;
dispatcher.register(sliderStore.handleAction.bind(sliderStore));
export default sliderStore;