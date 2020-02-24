import { EventEmitter } from 'events';
import dispatcher from '../dispatcher/Dispatcher.jsx'
import API from './API'
import Const from '../constants/Constants';


class ArtistStore extends EventEmitter {
    constructor(){
		super();
		this.artistDesign = null;
		this.artistSocialLinks = null;
		this.artistOtherDetails = {'success':false};
		this.artistBankDetails = {'success':false};
		this.allArtist = null;
	}
	
	fetchArtistDesigns(){
		API.fetchArtistDesigns();
    }
		
	fetchArtistSocialLinks(){
		API.fetchArtistSocialLinks();
	}

	fetchArtistOtherDetails(){
		API.fetchArtistOtherDetails();
 	}

   	fetchArtistBankDetails(){
		API.fetchArtistBankDetails();
	}
	
	getAllArtist(){
		return this.allArtist;
	}

	getArtistSocialLinks(){
		return this.artistSocialLinks
	}

  	getArtistDesign(){
		return this.artistDesign
	}

	getArtistOtherDetails(){
		return this.artistOtherDetails
	}
	getArtistBankDetails(){
		return this.artistBankDetails
	}

	updateDesign(design){
		this.artistDesign = design;
	}

    handleAction(action){
		switch (action.type){
            case Const.RECEIVE_ARTIST_DESIGNS: {
								this.artistDesign = action.data;
								this.emit("change")
								break;
			}
			case Const.RECEIVE_ARTIST_SOCIAL_LINKS: {
					this.artistSocialLinks = action.data;
					this.emit("change")
					break;
			}
			case Const.RECEIVE_ARTIST_OTHER_DETAILS: {
				this.artistOtherDetails = action.data;
				this.emit("change")
				break;
			}
			case Const.RECEIVE_ARTIST_BANK_DETAILS: {
				this.artistBankDetails = action.data;
				this.emit("change")
				break;
			}
			case Const.RECEIVE_ALL_ARTIST: {
				this.allArtist = action.data;
				this.emit("change")
				break;
			}
			break;
        }
    }
}


const artistStore = new ArtistStore;
dispatcher.register(artistStore.handleAction.bind(artistStore));
export default artistStore;