import React from 'react';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'
import * as UserActions from "../../actions/UserActions.jsx";
const lightMuiTheme = getMuiTheme(lightBaseTheme);

import API from '../../store/API'
import UserDetailStore from '../../store/UserStore.jsx';

class RedeemPromoCode extends React.Component {

	constructor(props) {
		super(props);
			this.redeemType = this.props['type'];
			// if (this.code){
			// 	self.handleAddPromoClick()
			// }
			this.state = {
				errorCodeText: null,
				redeemCode: getCookie('coupon'),
		};
	}

	handleAddPromoClick = () => {
    var self = this;
    if (this.state.redeemCode.length >= 6){
	      API.redeemCoupon(this.state.redeemCode, this.redeemType, function(data){
	        if (data.error){
	          self.setState(
	            {errorCodeText : <td dangerouslySetInnerHTML={{__html: data.errorText}} />}
	          )
	          setCookie('coupon', self.state.redeemCode, 1)
					}
				else {
						// UserActions.getNewRedeemValue(data)
						window.location = '/user/profile/?tab=2'
				}
	      });
	    }
	    else{
	      this.setState(
	        {errorCodeText : "Invalid Code, Please try another code" }
	      )
	    }
  	}


	handleCodeChange = (e) => {
		this.setState(
		  {redeemCode: e.target.value}
		)
	}


	render(){
		return ( 
			<MuiThemeProvider muiTheme={lightMuiTheme}>
			<div>
	            <TextField
	              hintText="PROMO CODE"
	              onChange={(e)=>this.handleCodeChange(e)}
	              value={this.state.redeemCode}
	              />
	            <RaisedButton
	              label="REDEEM" 
	              onTouchTap={this.handleAddPromoClick.bind(this)}
	              ref="redeemButton"
	            />
	            <p className='error'>{this.state.errorCodeText}</p>
	            <br />
	        </div>
	    </MuiThemeProvider>
		)
	}
 }

export default RedeemPromoCode;