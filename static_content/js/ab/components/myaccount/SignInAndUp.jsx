import React from 'react';
import SignUp from './SignUp.jsx'
import SignIn from './SignIn.jsx'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'
import RaisedButton from 'material-ui/RaisedButton';

const lightMuiTheme = getMuiTheme(lightBaseTheme);

class SignInAndUp extends React.Component {

	constructor(props) {
		super(props);
		this.isOnlyRegister = props['register']
	}

	render() {

		const signInComponent = this.isOnlyRegister ? null : function () {
			return (
				<div>
					<h3 className="modal-title" id="myModalLabel">Login to Your Account</h3>
					<SignIn type="withoutOtp" />
					<h3 className="modal-title" id="myModalLabel">Dont Have Account ?</h3>
				</div>
			)
		}();
		return (
			<MuiThemeProvider muiTheme={lightMuiTheme}>
				<div className='container'>
					<div className="">
						<div className="col-sm-8 col-xs-12 pad-10">
							<div className="modal-header login_modal_header">
								<h2 style={{ color: 'red' }} className="modal-title" id="myModalLabel">Get Exciting offers and discounts !!</h2>
								{signInComponent}
								<SignUp enabled={false} />
							</div>
						</div>
						<div className="col-sm-4 col-xs-12 pad-10">
							<div className="modal-body login-modal modal-header login_modal_header">
								<div className=''>
									<div className="modal-social-icons" >
										<h3 className="modal-title" id="myModalLabel">Or Connect with </h3>
										<a href="/login/facebook/?next=/aura/fb/request/" className="btn btn-default facebook fw"> <i className="fa fa-facebook modal-icons"></i> Sign In with Facebook </a>
										<a href="/login/google-oauth2/?next=/aura/google/" className="btn btn-default google fw"> <i className="fa fa-google-plus modal-icons"></i> Sign In with Google </a>
										<br />
										<br />
										<br />
										<h3 className="modal-title" id="myModalLabel">Creative Artist, Sign In to your Dashboard </h3>
										<a href="/artist/login"><RaisedButton label="Sign In" /></a>
									</div>
								</div>
							</div>
							<br />
							<br />
							<br />
							<br />
						</div>
					</div>
				</div>
			</MuiThemeProvider>
		)

	}
}

export default SignInAndUp;