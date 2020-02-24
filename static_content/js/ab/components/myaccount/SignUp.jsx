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
import UserStore from '../../store/UserStore.jsx';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'
const lightMuiTheme = getMuiTheme(lightBaseTheme);



import API from '../../store/API'
import UserDetailStore from '../../store/UserStore.jsx';
import VerifyOTP from '../myaccount/VerifyOTP.jsx'

class SignUp extends React.Component {

  constructor(props) {
    super(props);
    this.getUserSignInStatusAndCartData = this.getUserSignInStatusAndCartData.bind(this);
    this.state = {
      notifyOTPVerification : false,
      otpValue: '',
      openSignUpDialogue: props['enabled'],
      mobile: this.props['mobile'],
      isSubmitEnable: true,
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
			  this.state.errorTextEmail == "" && this.state.errorTextName == "" ){
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
	handleSubmit = () => {
		API.signUpCustomer(
			this.state.fullName,
			this.state.email,
			this.state.mobile,
			this.state.password,
			function(data){
	    	if (data.success){
	    		UserStore.updateUserSignInStatus(true)
	    	}
	    })
	}

	getUserSignInStatusAndCartData(){
			var newself = this;
  		this.setState({
	    	openSignUpDialogue: UserStore.is_user_authenticated()? false : newself.state.openSignUpDialogue,
		})
  	}

	componentWillMount() {
  		UserStore.on("change", this.getUserSignInStatusAndCartData);
  		
  	}

  	componentWillUnmount() {
    	UserStore.on("change", this.getUserSignInStatusAndCartData);
  	}

	render(){
	console.log('rendering.... signup');
	console.log(this.state.openSignUpDialogue)
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
		return ( 
		<MuiThemeProvider muiTheme={lightMuiTheme}>
		<div>
		<RaisedButton label="Sign Up" onTouchTap={this.handleOpen} />
			<Dialog
	            title="Sign Up to Addiction Bazaar"
	            modal={true}
	            actions={actions}
	            open={this.state.openSignUpDialogue}
	          >
	          <TextField
	            hintText="Name"
							errorText= {this.state.errorTextName}
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
							maxLength="10"
	            onChange={this.onChangeMobile.bind(this)}
	          /><br />
	          <TextField
	            hintText="Password"
	            errorText= {this.state.errorTextPassword}
	            onChange={this.onChangePassword.bind(this)}
	            type="password"
	          /><br />
	          </Dialog>
		</div>
		</MuiThemeProvider>
		)
	}
 }

export default SignUp;
