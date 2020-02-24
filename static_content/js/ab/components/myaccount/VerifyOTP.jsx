import React from 'react';
import Avatar from 'material-ui/Avatar';
import List from 'material-ui/List/List';
import ListItem from 'material-ui/List/ListItem';
import FlatButton from 'material-ui/FlatButton';
import {Tabs, Tab} from 'material-ui/Tabs';
// From https://github.com/oliviertassinari/react-swipeable-views
import SwipeableViews from 'react-swipeable-views';
import Subheader from 'material-ui/Subheader';
import Call from 'material-ui/svg-icons/communication/call';
import Email from 'material-ui/svg-icons/communication/email';
import UserIcon from 'material-ui/svg-icons/action/account-circle';
import Divider from 'material-ui/Divider';
import Dialog from 'material-ui/Dialog';
import TextField from 'material-ui/TextField';
import Snackbar from 'material-ui/Snackbar';
import RaisedButton from 'material-ui/RaisedButton';
import Paper from 'material-ui/Paper';



import API from '../../store/API'
import UserDetailStore from '../../store/UserStore.jsx';

class VerifyOTP extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      notifyOTPVerification : false,
      otpValue: '',
      openMobileVerificationDialogue: false,
      mobile: this.props['mobile'],
      isUserLoggedIn: this.props['isUserLoggedIn'],
      // enableMobileVerifyButton: props['customer_details']['is_mobile_verified']
    };
  }

	verifyOTP = (event) => {
	    var self = this;
	    this.setState({
	    	mobile: this.props['mobile'],
	    })
	    API.verifyOTP(this.state.otpValue, this.state.mobile, function(data){
	      if (data.success){
	        self.setState({notifyOTPVerification: true})
	        self.handleClose()
	        if (self.state.isUserLoggedIn){
	        	UserDetailStore.updateUserDetailsAfterMobileVerification(self.state.mobile)
	        }
	        else{
	        	UserDetailStore.fetchUserBasicDetails()	
	        }
	      }
	      else{
	        self.setState({errorTextOTP: 'Incorrent OTP, Please try again'})
	      	}
		})
	}   

	 onChangeOTP = (event) => {
	    var otpNoRegex = new RegExp("\\d{6}$");
	    if (otpNoRegex.test(event.target.value) && event.target.value.length == 6 ){
	      this.setState({ errorTextOTP: '', otpValue: event.target.value })
	    }
	    else if (event.target.value == ''){
	      this.setState({ errorTextOTP: 'This field is required' })
	    }
	    else {
	      this.setState({ errorTextOTP: 'Please enter a valid 6 digit number' }) 
	    }
	    console.log(this.state)
	}

	  handleClose = () => {
	    this.setState({openMobileVerificationDialogue: false});
	  };

	  handleOpen = () => {
	  	self = this;
	    this.setState({
	      openMobileVerificationDialogue: true,
	      errorTextOTP: '',
	    });
	    API.sendOTP(this.props['mobile'], function(data){
	    	if (data.success){
	    		self.setState({
			    	mobile: self.props['mobile'],
			    })
	    	}
	    })
	  };

	render(){

	const actions = [
      <FlatButton
        label="Cancel"
        primary={true}
        keyboardFocused={true}
        onTouchTap={this.handleClose}
      />,
      <RaisedButton
        label="Verify" 
        onTouchTap={this.verifyOTP.bind(this)}
        ref="otpField"
      />
    ];
		return ( 
		<div>
		<RaisedButton label="Verify" disabled={!this.props['enable']} onTouchTap={this.handleOpen} />
			<Dialog
	            title="Enter OTP (one time password) sent on your Mobile"
	            modal={true}
	            actions={actions}
	            open={this.state.openMobileVerificationDialogue}
	          >
	          <TextField
	            hintText="6 Digit One Time Password"
	            errorText= {this.state.errorTextOTP}
	            onChange={this.onChangeOTP.bind(this)}
	          /><br />
	          </Dialog>
	          <Snackbar
	            open={this.state.notifyOTPVerification}
	            message="OTP is verified"
	            autoHideDuration={1000}
	          />
		</div>
		)
	}
 }

export default VerifyOTP;