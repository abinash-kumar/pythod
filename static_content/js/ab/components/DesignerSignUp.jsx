import React from 'react';
import ReactDOM from 'react-dom';
import DesignerSignUpPopUp from './DesignerSignUpPopUp.jsx'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'

class DesignerSignUp extends React.Component {

	constructor(props) {
		super(props);
		this.user_type = props['user'];
	}

	render(){
		const lightMuiTheme = getMuiTheme(lightBaseTheme);
		const staticPath = "http://"+ window.location.host;
		const fullName = fullName;
		return (
			<MuiThemeProvider muiTheme={lightMuiTheme}>
			<div>
			<div className="col-md-12 des-signup-top">
					<div className="container">
						<div className="col-md-10">
							<h1>Sign Up</h1>
							<h2><i>Welcome to </i>ADDICTION BAZAAR</h2>
							<h5><i>A runway to flaunt your talent</i></h5>
						</div>
						<div className="col-md-2 vcen">
							<DesignerSignUpPopUp user_type={this.user_type} fullname={fullName}/>
						</div>
					</div>
			</div>
			<div className="container">
				<div className="row">
					<div className="col-sm-12 txtc">
						<h1>Team with Addiction Bazaar</h1>
							<DesignerSignUpPopUp user_type={this.user_type}/>
					</div>
				</div>
				<div className="row">
					<div className="col-xs-6 vc">
						<h3 className='animated'>Reach across the globe</h3>
						<div className="line"></div>
						<p>Your work would be appreciated by shoppers not only in India but also other countries all over the world.</p>
					</div>
					<div className="col-xs-6 txtc">
						<img className='fx250' src={staticPath + "/static/img/reach-across-the-globe.png"}  alt=""></img>
					</div>
				</div>
				<div className="row">
					<div className="col-xs-6 txtc">
						<img className='fx250' src={staticPath + "/static/img/complete-transperancy.png"}  alt=""></img>
					</div>
					<div className="col-xs-6">
						<h3 className='animated'>Complete transparency</h3>
						<div className="line"></div>
						<p>Track your sales, profits, inventory, customer base, target audience and much more with interactive dashboards and daily reports in your inbox. Stay on top of the game with enhanced analytics.</p>
					</div>
				</div>
				<div className="row">
					<div className="col-xs-6">
						<h3 className='animated'>Managing other essentials</h3>
						<div className="line"></div>
						<p>Meanwhile, let us handle all the marketing and customer acquisition for you. We will take care of all the hassles of delivery, inventory management, order management, cash flow, etc.</p>
					</div>
					<div className="col-xs-6 txtc">
						<img className='fx250' src={staticPath + "/static/img/managing-other-essentials.png"}  alt=""></img>
					</div>
				</div>
				<div className="row">
					<div className="col-xs-6 txtc">
						<img className='fx250' src={staticPath + "/static/img/feedback.png"}  alt=""></img>
					</div>
					<div className="col-xs-6">
						<h3 className='animated'>Feedback</h3>
						<div className="line"></div>
						<p>We will channel the customer feedbacks to you to create better customer experience and customer retention for your successful future endeavour.</p>
					</div>
				</div>
				<div className="row">
					<div className="col-xs-6">
						<h3 className='animated'>Authentic platform</h3>
						<div className="line"></div>
						<p>Be a part of a recognised and trusted brand. Leverage the brand of Addiction Bazaar to pump up your sales. Be the heart and soul authority of your designs.</p>
					</div>
					<div className="col-xs-6 txtc">
						<img className='fx250' src={staticPath + "/static/img/AUTHENTIC.png"}  alt=""></img>
					</div>
				</div>
				<div className="row">
					<div className="col-xs-6 txtc">
						<img className='fx250' src={staticPath + "/static/img/direct-customer-selling.png"}  alt=""></img>
					</div>
					<div className="col-xs-6">
						<h3 className='animated'>Direct consumer selling</h3>
						<div className="line"></div>
						<p>You can reach out to your consumers directly and know their personal interests and this also reduces the profit margin of middlemen.</p>
					</div>
				</div>					
					<div className="row">
						<div className="col-xs-12">
							<h2>Better yet, meet us in person!</h2>
						</div>
						<h5>You can even drop us an email at contact@addictionbazaar.com to schedule a meeting.</h5>
						<h5>Let us make the world get addicted to fashion together!</h5>
						<DesignerSignUpPopUp user_type={this.user_type}/>
					</div>
					<div className="row">
						<div className="col-sm-12">
						<div className="line"></div>
						<h2>About Us</h2>
							<p>Addiction bazaar is an easy and a smart platform where anyone can shop non-stop online. To make this shopping more fun, we need cooperation of yours so that our shoppers look their best in all occasions.</p>
						</div>
					</div>
				</div>
			</div>
			</MuiThemeProvider>
		)
	}
}

export default DesignerSignUp;