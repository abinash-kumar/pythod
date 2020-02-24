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
import EditProfile from './EditProfile.jsx'
import RedeemPromoCode from './RedeemPromoCode.jsx'



import API from '../../store/API'
import UserDetailStore from '../../store/UserStore.jsx';

import VerifyOTP from './VerifyOTP.jsx'


import {
  blue300,
  indigo900,
  orange200,
  deepOrange300,
  pink400,
  purple500,
} from 'material-ui/styles/colors';

const style = { margin: 5 };

const styles = {
  headline: {
    fontSize: 24,
    paddingTop: 16,
    marginBottom: 12,
    fontWeight: 400,
  },
  slide: {
    padding: 0,
  },
  button: {
    marginBotton: 10,
    height: 40,
    margin: 0,
  },
  orderdetail: {
    width: 300,
    padding: 10,
  },
  tab: {
    backgroundColor: indigo900,
  },
};


class UserProfileCard extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      slideIndex: getValueOfParam('tab') ? parseInt(getValueOfParam('tab')) : 0,
      notifyOTPVerification: false,
      otpValue: '',
      mailSent: false,
    };
  }

  componentWillMount() {
    UserDetailStore.on("change", this.setUserState);
  }

  componentWillUnmount() {
    UserDetailStore.removeListener("change", this.setUserState);
  }

  setUserState = () => {
    this.setState({
      mailSent: UserDetailStore.get_email_sent_status()
    })
  }

  handleChange = (value) => {
    this.setState({
      slideIndex: value,
    });
  };

  handleRequestClose = () => {
    this.setState({
      handleRequestClose: false
    })
  }

  handleNestedListToggle = (item) => {
    this.setState({
      open: item.state.open,
    });
  };

  handleVerifyEmail = () => {
    API.sendEmailLink();
  }


  render() {
    const addresses = !this.props['customer_details'] ? null : this.props['customer_details']['customer_address_list']
    const addressComponent = !addresses ? null : addresses.map(function (address, index) {
      return (
        <div className='col-md-6' key={index}>
          <Paper style={styles.orderdetail} zDepth={1}>
            <p>{address['name']}</p>
            <p>{address['address']}</p>
            <p>{address['city'] + ', ' + address['state']}</p>
            <p>{address['pincode']}</p>
            <p>{address['mobile']}</p>
          </Paper>
        </div>
      )
    });
    const addressComponentBlock = !this.props['customer_details'] ? null : this.props['customer_details']['customer_address_list'].length == 0 ? null : [this.props['customer_details']].map(function (value, i) {
      return (
        <div className='container' key={i}>
          <Divider />
          <h3> Address </h3>
          {addressComponent}
        </div>
      )
    });
    const verifyMobile = !this.props['customer_details'] ? null : this.props['customer_details']['is_mobile_verified'] ? null : <VerifyOTP mobile={this.props['mobile']} isUserLoggedIn={true} enable={true} />;
    const verifyEmail = !this.props['customer_details'] ?
      null : this.props['customer_details']['is_email_verified'] ?
        null : this.state.mailSent ?
          <p style={styles.textEmail} >Please check inbox</p> :
          <RaisedButton
            label="Verify"
            key="email-Key-verify"
            onTouchTap={this.handleVerifyEmail.bind(this)}
            ref="emailField"
          />;
    const orders = this.props['orders']
    const orderComponents = !orders ? null : orders.map(function (order, index) {
      var orderProperty = [];
      for (var p in order) {
        if (order.hasOwnProperty(p) && p != 'product' && p != 'photo') {
          orderProperty.push(p);
        }
      }
      const orderPropertyComponents = !orderProperty ? null : orderProperty.map(function (orderProperty, idex) {
        return (
          <div key={idex}>
            <p key={idex} >{orderProperty} : {order[orderProperty]} </p>
          </div>
        )
      });
      return (
        <ListItem
          key={index + 1}
          primaryText={order['product']}
          leftAvatar={<Avatar src={order['photo']} />}
          nestedItems={[<Paper key={index + 100} style={styles.orderdetail} zDepth={1}>
            {orderPropertyComponents}
          </Paper>
          ]}
        />)
    })



    const mobileItem = !this.props['mobile'] ? null : <ListItem
      key="mobile-Key"
      disabled={true}
      leftIcon={<Call />}
      rightIcon={verifyMobile}
    >
      {this.props['mobile']}
    </ListItem>

    const emailItem = !this.props['email'] ? null :
      <div>
        <ListItem
          key="email-Key"
          disabled={true}
          leftIcon={<Email />}
        >
          {this.props['email']}
        </ListItem>
        <div style={{ marginLeft: 70 }} key="email-Key">
          {verifyEmail}
        </div>
      </div>
    const walletData = this.props['wallet'];
    const walletRow = !walletData ? null : walletData.money_list.map((row, i) => (
      <tr key={i}>
        <td>{row.created_on}</td>
        <td>{row.amount_type}</td>
        <td>{row.particular}</td>
        <td>{row.expiry}</td>
        <td>{row.amount}</td>
        <td>{row.closing_money}</td>
      </tr>
    ));
    const walletComponent = function () {
      if (walletData) {
        return (
          <div className="container">
            <div>
              <h2>Addiction Bazaar Wallet</h2>
            </div>
            <div className="dabba fl">
              <h5>Promotional Money</h5>
              <p>Rs. {walletData.closing_promotional_money}</p>
            </div>
            <div className="dabba fl">
              <h5>Loyality Money</h5>
              <p>Rs. {walletData.closing_cash_money}</p>
            </div>
            <RedeemPromoCode type='PROMOTIONAL' />
            <br />
            <div className='container'>
              <p>Details of Wallet</p>
              <table className="table table-bordered">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Type</th>
                    <th>Particulars</th>
                    <th>Expiry</th>
                    <th>Amount</th>
                    <th>Closing Balance</th>
                  </tr>
                </thead>
                <tbody>
                  {walletRow}
                </tbody>
              </table>
            </div>
          </div>
        )
      }
      else {
        return null;
      }
    }.bind(this)();
    return (
      <div>

        <Tabs
          onChange={this.handleChange}
          value={this.state.slideIndex}
          initialSelectedIndex={0}
          inkBarStyle={{ background: '#48a89b', height: '4px' }}
        >
          <Tab label="Your Profile" value={0} style={{ background: 'rgb(181, 182, 184)', fontSize: '13px', color: '#000', textTransform: 'initial', fontWeight: '800' }} />
          <Tab label="Order History" value={1} style={{ background: 'rgb(181, 182, 184)', fontSize: '13px', color: '#000', textTransform: 'initial', fontWeight: '800' }} />
          <Tab label="My Wallet" value={2} style={{ background: 'rgb(181, 182, 184)', fontSize: '13px', color: '#000', textTransform: 'initial', fontWeight: '800' }} />
        </Tabs>
        <SwipeableViews
          index={this.state.slideIndex}
          onChangeIndex={this.handleChange}
        >
          <div style={styles.slide}>
            <div className='container-full'>
              <br />
              <EditProfile />
              {addressComponentBlock}
            </div>

          </div>
          <div style={styles.slide}>
            <List>
              <Subheader>Recents Orders</Subheader>
              {orderComponents}
            </List>
          </div>
          <div style={styles.slide}>
            {walletComponent}
          </div>
        </SwipeableViews>

      </div>
    )
  }
}

export default UserProfileCard;




