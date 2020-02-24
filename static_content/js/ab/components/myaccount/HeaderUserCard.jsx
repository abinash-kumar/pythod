import React from 'react';
import ReactDOM from 'react-dom';
import Modal from 'react-responsive-modal';
import UserStore from '../../store/UserStore.jsx';
import Slider from 'react-slick';
import { BottomNavigation, BottomNavigationItem } from 'material-ui/BottomNavigation';
import Paper from 'material-ui/Paper';
import FontIcon from 'material-ui/FontIcon';
import IconLocationOn from 'material-ui/svg-icons/communication/location-on';
import IconShoppingCart from 'material-ui/svg-icons/action/shopping-cart';
import IconAccount from 'material-ui/svg-icons/action/account-box';
import Iconwallet from 'material-ui/svg-icons/action/account-balance-wallet';
import IconSearch from 'material-ui/svg-icons/action/search';
import IconClose from 'material-ui/svg-icons/navigation/close';
import FlatButton from 'material-ui/FlatButton';
import FullscreenDialog from 'material-ui-fullscreen-dialog'
import SignInAndUp from './SignInAndUp.jsx'
import Snackbar from 'material-ui/Snackbar';
import Badge from 'material-ui/Badge';
import IconButton from 'material-ui/IconButton';
import { List, ListItem } from 'material-ui/List';
import Divider from 'material-ui/Divider';
import Drawer from 'material-ui/Drawer';
import AppBar from 'material-ui/AppBar';
import NavigationClose from 'material-ui/svg-icons/navigation/close';
import FullScreenSearch from '../auraai/FullScreenSearch.jsx'
import Notify from '../Notification.jsx';



class HeaderUserCard extends React.Component {

	constructor(props) {
		super(props);
		this.openAccountOrSignInPop = this.openAccountOrSignInPop.bind(this);
		this.getUserSignInStatusAndCartData = this.getUserSignInStatusAndCartData.bind(this);
		this.openFav = this.openFav.bind(this);
		this.isProfilePage = false;
		if (window.location.pathname == '/user/profile/') {
			this.isProfilePage = true;
		}
		this.isSignIn = getCookie("isSignIn") == 'true' ? true : false;
		this.state = {
			cartCount: 0,
			openPopup: false,
			openPopupforSignIn: false,
			isSignedIn: this.isSignIn,
			userFullName: '',
			openDrawer: false,
			showSearchBar: false,
		};
		UserStore.fetchUserBasicDetails()
	}

	componentWillMount() {
		UserStore.on("change", this.getUserSignInStatusAndCartData);
		if (!this.state.isSignedIn && !getCookie('popupSeen') && !getValueOfParam('prerender')) {
			setTimeout(function () {
				this.setState({ openPopup: true });
			}.bind(this), 5000);
		}
	}

	componentWillUnmount() {
		UserStore.on("change", this.getUserSignInStatusAndCartData);
	}

	getUserSignInStatusAndCartData() {
		this.setState({
			isSignedIn: UserStore.is_user_authenticated(),
			cartCount: UserStore.getCartCount(),
			openPopup: false,
			userFullName: UserStore.getUserFullName(),
		})
	}

	openAccountOrSignInPop() {
		if (this.state.isSignedIn) {
			this.setState({
				openDrawer: true,
			});
			// window.location.href = "/user/profile/";
		}
		else {
			this.setState({
				openPopup: true,
				openPopupforSignIn: true,
			});
		}
	}

	handleTouchTapMyAccount = () => {
		this.setState({
			openDrawer: false
		})
	}
	showSeaech = () => {
		this.setState({ showSearchBar: true });
	};
	hideSearch = () => {
		this.setState({ showSearchBar: false });
	};
	openCart() {
		window.location.href = "/my-cart"
	}

	openFav() {
		if (this.state.isSignedIn) {
			window.location.href = "/user/profile/?tab=2"
		}
		else {
			this.setState({
				openPopup: true,
			});
		}
	}

	render() {
		const isSignIn = this.state.isSignedIn;
		const self = this;
		const userFullName = this.state.userFullName;
		const accountIcon = <IconAccount />
		const shoppingIcon = <IconShoppingCart />
		const isMobile = window.innerWidth <= 500 || getValueOfParam('mobile');
		const walletIcon = <Iconwallet />;
		const className = isMobile ? "mobile-header-card" : "desktop-header-card sticky"
		const title = "Sign In"
		const lableSignIn = isSignIn ? "Profile" : "Sign In";
		const uploadArtComponent = function () {
			if (UserStore.is_logged_in_user_is_artist()) {
				return (
					<div>
						<a href="/artist/home/">
							<ListItem innerDivStyle={{ padding: '16px 16px 16px 16px' }} insetChildren={true} primaryText="Upload Your Art" />
						</a>
						<Divider />
					</div>
				)
			}
			else {
				return null;
			}
		}();
		const dropdownComponent = function () {
			return (
				<Drawer containerClassName='drawer' width={200} openSecondary={true} open={self.state.openDrawer} >
					<AppBar
						iconElementLeft={<a onClick={self.handleTouchTapMyAccount}><IconButton><NavigationClose /></IconButton></a>}
						titleStyle={{ fontSize: '15px' }}
						className='drawer-bar'
						style={{ backgroundColor: 'rgb(11, 168, 154)' }}
						title="My Account" />
					<List>
						{uploadArtComponent}
						<a href="/user/profile/">
							<ListItem innerDivStyle={{ padding: '16px 16px 16px 16px' }} insetChildren={true} primaryText="Your Profile" />
						</a>
						<Divider />
						<a href="/aura/fb/request/">
							<ListItem innerDivStyle={{ padding: '16px 16px 16px 16px' }} insetChildren={true} primaryText="Connect to Facebook" />
						</a>
						<Divider />
						<a href="/my-cart/">
							<ListItem innerDivStyle={{ padding: '16px 16px 16px 16px' }} insetChildren={true} primaryText="Cart" />
						</a>
						<Divider />
						<a href="/user/profile/?tab=1">
							<ListItem innerDivStyle={{ padding: '16px 16px 16px 16px' }} insetChildren={true} primaryText="Order History" />
						</a>
						<Divider />
						<a href="/user/profile/?tab=2">
							<ListItem innerDivStyle={{ padding: '16px 16px 16px 16px' }} insetChildren={true} primaryText="Wallet" />
						</a>
						<Divider />
						<a href='/logout/'>
							<ListItem innerDivStyle={{ padding: '16px 16px 16px 16px' }} insetChildren={true} primaryText="Logout" />
						</a>
						<Divider />
					</List>
				</Drawer>
			)
		}();

		const card = function () {
			if (isMobile) {
				return (
					<Paper zDepth={1}>
						<FullScreenSearch show={this.state.showSearchBar} isMobile={true} />
						<BottomNavigation selectedIndex={this.state.selectedIndex} overlayStyle={{ width: '200px' }}>
							<BottomNavigationItem
								label="Search"
								icon={<IconSearch />}
								onClick={this.showSeaech}
								style={{ zIndex: 0 }}
							/>
							<BottomNavigationItem
								label={lableSignIn}
								icon={accountIcon}
								onClick={this.openAccountOrSignInPop}
								style={{ zIndex: 0 }}
							/>
							<Badge
								badgeContent={this.state.cartCount ? this.state.cartCount : 0}
								primary={true}
								onClick={this.openCart}
								style={{ flex: 0, padding: '10px 0 0 0' }}
							>
								<IconButton tooltip="MyCart" >
									{shoppingIcon}
								</IconButton>

							</Badge>

							<BottomNavigationItem
								label="My Wallet"
								icon={walletIcon}
								onClick={this.openFav}
								style={{ zIndex: 0 }}
							/>

						</BottomNavigation>
					</Paper>
				)
			}
			else {
				return (
					<div className="desktop-header-icons" >
						<BottomNavigation style={{backgroundColor: 'rgb(240, 240, 240)'}}>
							<FullScreenSearch show={this.state.showSearchBar} />
							<BottomNavigationItem
								label="Search"
								icon={<IconSearch />}
								onClick={this.showSeaech}
								style={{ right: '-18px', top: '0px', zIndex: 0 }}
							/>
							<BottomNavigationItem
								label={lableSignIn}
								icon={accountIcon}
								onClick={this.openAccountOrSignInPop}
								style={{ zIndex: 0 }}
							/>
							<Badge
								badgeContent={this.state.cartCount ? this.state.cartCount : 0}
								primary={true}
								style={{ flex: 0, padding: '10px 0 0 0' }}
								onClick={this.openCart}
							>
								<IconButton tooltip="MyCart" style={{ zIndex: 0 }} >
									{shoppingIcon}
								</IconButton>
							</Badge>

							<BottomNavigationItem
								label="My Wallet"
								icon={walletIcon}
								onClick={this.openFav}
								style={{ zIndex: 0 }}
							/>
						</BottomNavigation>
					</div>
				)
			}
		}.bind(this)();

		return (
			<div className={className}>
				<Notify />
				{card}
				{dropdownComponent}
				<FullscreenDialog
					open={this.state.openPopup}
					onRequestClose={() => {
						this.setState({ openPopup: false });
						setCookie('popupSeen', true, 3);
					}
					}
					title={title}
					style={{ marginTop: '60px' }}
					appBarStyle={{ backgroundColor: 'rgb(11, 168, 155)' }}
					actionButton={<FlatButton
						label='Done'
						onTouchTap={() => {
							this.setState({ openPopup: false });
							setCookie('popupSeen', true, 3);
						}
						}
					/>}
				>
					<SignInAndUp />
				</FullscreenDialog>
			</div>
		);
	}
}

export default HeaderUserCard;