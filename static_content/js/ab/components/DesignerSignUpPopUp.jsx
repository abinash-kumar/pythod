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
import Checkbox from 'material-ui/Checkbox';

import API from '../store/API'
import UserDetailStore from '../store/UserStore.jsx';
import VerifyOTP from './myaccount/VerifyOTP.jsx'

class SignUp extends React.Component {

  constructor(props) {
    super(props);
    this.user_type = props['user_type'];
    this.state = {
      notifyOTPVerification : false,
      otpValue: '',
      openSignUpDialogue: props['enabled'],
      mobile: this.props['mobile'],
      isSubmitEnable: true,
			fullName: this.props['fullname'],
			termsConditions:false,
      // enableMobileVerifyButton: props['customer_details']['is_mobile_verified']
    };
  }

  verifyOTP = (event) => {
    var self = this;
    this.setState({
    	mobile: this.props['mobile'],
    })
    console.log(this.state.otpValue, this.state.mobile)
    API.verifyOTP(this.state.otpValue, this.state.mobile, function(data){
      if (data.success){
        self.setState({notifyOTPVerification: true})
        self.handleClose()
        UserDetailStore.updateUserDetailsAfterMobileVerification(self.state.mobile)
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
	this.setState({openSignUpDialogue: false});
	};

	handleOpen = () => {
	this.setState({
	  openSignUpDialogue: true,
	});
	};

	handleTermsConditionCB = (event) => {
		this.setState({termsConditions:event.target.checked,},() => {this.handleSubmitEnableStatus();})
		};

	onChangeName = (event) => {
		if (event.target.value != ''){
			this.setState({
				fullName : event.target.value,
				errorTextName: '',
			},() => {this.handleSubmitEnableStatus();});
		}
		else{
			this.setState({
				errorTextName: 'Please Enter Name to Sign Up',
				fullName : event.target.value,
			},() => {this.handleSubmitEnableStatus();})	
		}
	}

	onChangeBrand = (event) => {
		if (event.target.value != ''){
			this.setState({
				brand : event.target.value,
				errorTextBrand: '',
			},() => {this.handleSubmitEnableStatus();});
		}
		else{
			this.setState({
				errorTextBrand: 'Please enter your preferred shop name',
				brand : event.target.value,
			},() => {this.handleSubmitEnableStatus();})	
		}
	}

	onChangePincode = (event) => {
		if (event.target.value != ''){
			this.setState({
				pincode : event.target.value,
				errorTextPincode: '',
			},() => {this.handleSubmitEnableStatus();});
		}
		else{
			this.setState({
				errorTextPincode: 'Please enter your pincode',
				pincode : event.target.value,
			},() => {this.handleSubmitEnableStatus();})
		}
	}

	onChangeEmail = (event) => {
		var emailRegex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
		if (emailRegex.test(event.target.value)){
			this.setState({
				email : event.target.value,
				errorTextEmail: '',
			},() => {this.handleSubmitEnableStatus();});
		}
		else if (event.target.value == ''){
			this.setState({
				errorTextEmail: 'Please Enter Eamil to Sign Up',
				mobile : event.target.value,
			},() => {this.handleSubmitEnableStatus();})	
		}
		else{
			this.setState({
				errorTextEmail: 'Please Enter valid Email',
				email : event.target.value,
			},() => {this.handleSubmitEnableStatus();})	
		}
	}

	onChangeMobile = (event) => {
		var mobileNoRegex = new RegExp("\\d{10}$");
		if (mobileNoRegex.test(event.target.value) && event.target.value.length == 10 ){
			this.setState({
				mobile : event.target.value,
				errorTextMobile: '',
			},() => {this.handleSubmitEnableStatus();});
		}
		else if (event.target.value == ''){
			this.setState({
				errorTextMobile: 'Please Enter Mobile to Sign Up',
				mobile : event.target.value,
			},() => {this.handleSubmitEnableStatus();})	
		}
		else{
			this.setState({
				errorTextMobile: 'Please Enter Valid Mobile Number',
				mobile : event.target.value,
			},() => {this.handleSubmitEnableStatus();})	
		}
	}

	onChangePassword = (event) => {
		if (event.target.value != ''){
			this.setState({
				password : event.target.value,
				errorTextPassword: '',
			},() => {this.handleSubmitEnableStatus();});
		}
		else{
			this.setState({
				errorTextPassword: 'Please Enter Password',
				password : event.target.value,
			},() => {this.handleSubmitEnableStatus();})	
		}
	}

	handleSubmitEnableStatus = () => {
		if (this.state.fullName && this.state.email  && this.state.mobile && this.state.password && 
				this.state.errorTextPassword == "" && this.state.errorTextMobile == "" &&
				this.state.errorTextEmail == "" && this.state.errorTextName == "")
		{
			if(this.user_type == 'artist' && this.state.termsConditions){
				this.setState({
					isSubmitEnable: false,
				})
			}
			else{
				this.setState({
					isSubmitEnable: true,
				})
			}
		}
		else{
			this.setState({
				isSubmitEnable: true,
			})
		}
	}
	handleSubmit = () => {
		var self = this;
		if (this.user_type == 'designer'){
			API.signUpDesigner(
				this.state.fullName,
				this.state.email,
				this.state.mobile,
				this.state.password,
				this.state.brand,
				this.state.pincode,
				function(data){
					
		    	if (data.success){
		    		self.setState({
		    			openSignUpDialogue: false,
		    		})
		    		console.log('all fine...')
		    		window.location = data.redirect_url;
		    	}
		    })
	    }
	    else if (this.user_type == 'artist'){
	    	API.signUpArtist(
				this.state.fullName,
				this.state.email,
				this.state.mobile,
				this.state.password,
				artist_type,
				function(data){
					
		    	if (data.success){
		    		self.setState({
		    			openSignUpDialogue: false,
		    		})
		    		console.log('all fine...')
		    		window.location = data.redirect_url;
		    	}
		    })

	    }
		
	}

	render(){

	console.log('rendering.... signup');
	const actions = [
      <FlatButton
        label="Cancel"
        primary={true}
        keyboardFocused={true}
        onTouchTap={this.handleClose}
      />,
      <FlatButton
        label="Submit"
        primary={true}
        keyboardFocused={true}
        onTouchTap={this.handleSubmit}
        disabled = {this.state.isSubmitEnable}
      />
    ];

	    if (this.user_type == 'designer'){
			return ( 
				<div>
				<RaisedButton label="Join our Team" onTouchTap={this.handleOpen} />
					<Dialog
						title="Sign Up"
			            modal={false}
			            actions={actions}
			            open={this.state.openSignUpDialogue}
						repositionOnUpdate={true}
						autoDetectWindowHeight={true}
						autoScrollBodyContent={true}
						className="dialog-root"
						contentClassName="dialog-content"
			          >
			          <TextField
			            hintText="Name"
			            errorText= {this.state.errorTextName}
									value={this.state.fullName}
									onChange={this.onChangeName.bind(this)}
			          /><br />
			          <TextField
			            hintText="Email"
			            errorText= {this.state.errorTextEmail}
			            onChange={this.onChangeEmail.bind(this)}
			          /><br />
			          <TextField
			            hintText="Mobile"
									errorText= {this.state.errorTextMobile}
									maxLength= "10"
			            onChange={this.onChangeMobile.bind(this)}
			          /><br />
			          <TextField
			            hintText="Your Preferred Collection Name"
			            onChange={this.onChangeBrand.bind(this)}
			            errorText= {this.state.errorTextBrand}
			          /><br />
			          <TextField
			            hintText="Pincode"
			            onChange={this.onChangePincode.bind(this)}
			            errorText= {this.state.errorTextPincode}
			          /><br />
			          <TextField
			            hintText="Password"
			            errorText= {this.state.errorTextPassword}
			            onChange={this.onChangePassword.bind(this)}
			            type="password"
			          /><br />
			          </Dialog>
				</div>
				)		
		}
		else if(this.user_type == 'artist') {
			return ( 
		<div>
		<RaisedButton label="Join our Team" onTouchTap={this.handleOpen} />
			<Dialog
				title="Sign Up"
	            modal={false}
	            actions={actions}
	            open={this.state.openSignUpDialogue}
				repositionOnUpdate={true}
				autoDetectWindowHeight={true}
				autoScrollBodyContent={true}
				className="dialog-root"
				contentClassName="dialog-content"
	          >
	          <TextField
	            hintText="Name"
	            onChange={this.onChangeName.bind(this)}
	            errorText= {this.state.errorTextName}
	            value={this.state.fullName}
	          /><br />
	          <TextField
	            hintText="Email"
	            errorText= {this.state.errorTextEmail}
	            onChange={this.onChangeEmail.bind(this)}
	          /><br />
	          <TextField
	            hintText="Mobile"
	            errorText= {this.state.errorTextMobile}
	            onChange={this.onChangeMobile.bind(this)}
	          /><br />
	          <TextField
	            hintText="Password"
	            errorText= {this.state.errorTextPassword}
	            onChange={this.onChangePassword.bind(this)}
	            type="password"
	          /><br />
						<div style={{float:'left'}}>
						<Checkbox
						onClick={this.handleTermsConditionCB.bind(this)}
						label={
							<div>
								 <span>I accept the </span>
								 <a href="https://addictionbazaar.com/blog/doc/artist-terms-and-condition" target='_blank'>Our Terms and Conditions</a>
							</div>
							}
						style = {{maxWidth: 250}}
						labelStyle = {{fontSize:15,width:'100%',zIndex:500}}
						/>
						</div>
	          </Dialog>
		</div>
		)

		}
		
	}
 }

export default SignUp;