import React from 'react';
import Avatar from 'material-ui/Avatar';
import List from 'material-ui/List/List';
import ListItem from 'material-ui/List/ListItem';
import FlatButton from 'material-ui/FlatButton';
import { Tabs, Tab } from 'material-ui/Tabs';
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
import ForgetPasswordPopUp from './ForgetPasswordPopUp.jsx';

import API from '../../store/API'
import UserDetailStore from '../../store/UserStore.jsx';
import VerifyOTP from '../myaccount/VerifyOTP.jsx'

class SignIn extends React.Component {

	constructor(props) {
		super(props);
		this.signInType = props['type']
		this.state = {
			openSignInDialogue: false,
			errorTextLogin: '',
			openOTPSignInDialogue: false,
			isVerifyMobileEnable: false,
		};
	}




	handleOpenSignInOTP = () => {
		this.setState({
			openOTPSignInDialogue: true,
		});
	}

	handleOpenSignInOTPClose = () => {
		this.setState({
			openOTPSignInDialogue: false,
		});
	}

	handleCloseOTPSignIn = () => {
		this.setState({
			openOTPSignInDialogue: false,
		});
	}

	handleOpenOTPSignIn = () => {
		this.setState({
			openOTPSignInDialogue: true,
		});
	}

	onChangeUserName = (event) => {
		if (event.target.value != '') {
			this.setState({
				userName: event.target.value,
				errorTextUserName: '',
				errorTextLogin: '',
			});
		}
		else {
			this.setState({
				errorTextUserName: 'Please Enter Mobile/Email to Sign In',
				errorTextLogin: '',
			})
		}
	}

	onChangePassword = (event) => {
		if (event.target.value != '') {
			this.setState({
				password: event.target.value,
				errorTextPassword: '',
				errorTextLogin: '',
			});
		}
		else {
			this.setState({
				errorTextPassword: 'Please enter password',
				errorTextLogin: '',
			})
		}
	}

	onChangeMobile = (event) => {
		var mobileNoRegex = new RegExp("\\d{10}$");
		if (mobileNoRegex.test(event.target.value) && event.target.value.length == 10) {
			var self = this;
			var mobile = event.target.value;
			API.checkMobileExistForUser(
				event.target.value,
				function (data) {
					if (data.success) {
						self.setState({
							isVerifyMobileEnable: true,
							mobileNumber: mobile,
							errorTextMobile: '',
							errorTextLogin: '',
						})
						console.log('all fine...')
					}
					else {
						self.setState({
							errorTextLogin: data.error_text,
							mobileNumber: '',
							errorTextMobile: '',
						})
					}
				})
		}
		else {
			this.setState({
				isVerifyMobileEnable: false,
				errorTextMobile: 'Please enter valid mobile number',
				errorTextLogin: '',
			})
		}
	}

	handleSubmit = () => {
		var self = this;
		if (this.state.userName && this.state.password && this.state.errorTextUserName === '' && this.state.errorTextPassword === '') {
			API.signInCustomer(
				this.state.userName,
				this.state.password,
				function (data) {
					if (data.success) {
						self.setState({
							openSignInDialogue: false,
						})
						console.log('all fine...')
					}
					else {
						self.setState({
							errorTextLogin: data.error_text,
							password: '',
						})
					}
				})
		} else {
			self.setState({
				errorTextLogin: "Fill All the Fields",
			})

		}
	}

	handleSubmitOTPSignIn = () => {

	}

	render() {

		const actions = [
			<FlatButton
				label="Cancel"
				primary={true}
				keyboardFocused={true}
				onTouchTap={this.handleClose}
			/>,

		];

		const actionsOTPSignIn = [
			<FlatButton
				label="Cancel"
				primary={true}
				keyboardFocused={true}
				onTouchTap={this.handleCloseOTPSignIn}
			/>
		];

		const otpButton = this.signInType == "withoutOtp" ? null : <RaisedButton label="Sign In Via OTP" onTouchTap={this.handleOpenOTPSignIn} />

		return (
			<div>
				<br />
				<TextField
					hintText="Email / Mobile"
					onChange={this.onChangeUserName.bind(this)}
					errorText={this.state.errorTextUserName}
				/><br />
				<TextField
					hintText="Password"
					errorText={this.state.errorTextPassword}
					onChange={this.onChangePassword.bind(this)}
					type="password"
				/><br /><br />
				<p className='err'>{this.state.errorTextLogin}</p>
				<br />
				<RaisedButton
					label="Submit"
					onTouchTap={this.handleSubmit}
					disabled={false}
				/>
				<br />
				<div style={{ color: "black" }}>
					<ForgetPasswordPopUp />
				</div>
				<br />
				{otpButton}

				<Dialog
					title="Sign In to Addiction Bazaar"
					modal={true}
					actions={actionsOTPSignIn}
					open={this.state.openOTPSignInDialogue}
				>
					<TextField
						hintText="Mobile"
						onChange={this.onChangeMobile.bind(this)}
						errorText={this.state.errorTextMobile}
					/><br />
					<br />
					<VerifyOTP mobile={this.state.mobileNumber} enable={this.state.isVerifyMobileEnable} isUserLoggedIn={false} />
					<p>{this.state.errorTextLogin}</p>
				</Dialog>
			</div>
		)
	}
}

export default SignIn;