import React from 'react';
import ImageStore from '../../store/Store.jsx';
import UserProfileCard from './UserProfileCard.jsx'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'
const lightMuiTheme = getMuiTheme(lightBaseTheme);


import UserDetailStore from '../../store/UserStore.jsx';
import HeaderUserCard from './HeaderUserCard.jsx'


class UserProfile extends React.Component {

  constructor() {
    super();
    this.getUserDetail = this.getUserDetail.bind(this);
    UserDetailStore.fetchUserBasicDetails()
    UserDetailStore.fetchUserWallet()
    this.state = {
      user_full_name : null,
      user_email : null,
      user_mobile : null,
      user_photo : null,
      orders : null,
    }
  }

  componentWillMount() {
    UserDetailStore.on("change", this.getUserDetail);
  }

  componentWillUnmount() {
    UserDetailStore.removeListener("change", this.getUserDetail);
  }

  getUserDetail() {
    this.setState({
      user_full_name : UserDetailStore.getUserDetail()[0],
      user_email : UserDetailStore.getUserDetail()[1],
      user_mobile : UserDetailStore.getUserDetail()[2],
      user_photo : UserDetailStore.getUserDetail()[3],
      orders : UserDetailStore.getUserDetail()[4],
      customer_details : UserDetailStore.getUserDetail()[5],
      walletData: UserDetailStore.getUserWallet(),
    });
  }

  render() {
    return (
      <MuiThemeProvider muiTheme={lightMuiTheme}>
        <div>
          <HeaderUserCard/>
            <UserProfileCard 
               name={this.state.user_full_name}
               email={this.state.user_email}
               mobile={this.state.user_mobile}
               photo={this.state.user_photo}
               orders={this.state.orders}
               customer_details={this.state.customer_details}
               wallet = {this.state.walletData}
            />
        </div>
     </MuiThemeProvider>
    );
  }

}

export default UserProfile;
