import React from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'

import RaisedButton from 'material-ui/RaisedButton';
import FlatButton from 'material-ui/FlatButton';

import UserDetailStore from '../../store/UserStore.jsx';
import OrderStore from '../../store/OrderStore.jsx';

import {RadioButton, RadioButtonGroup} from 'material-ui/RadioButton';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import ContentAdd from 'material-ui/svg-icons/content/add';
import TextField from 'material-ui/TextField';
import List from 'material-ui/List/List';
import ListItem from 'material-ui/List/ListItem';
import Subheader from 'material-ui/Subheader';
import Avatar from 'material-ui/Avatar';
import Paper from 'material-ui/Paper';
import Divider from 'material-ui/Divider';

import Dialog from 'material-ui/Dialog';

import VerifyOTP from '../myaccount/VerifyOTP.jsx'
import SignUp from '../myaccount/SignUp.jsx'
import SignIn from '../myaccount/SignIn.jsx'


import {
  Step,
  Stepper,
  SteButton,
  StepContent,
  StepLabel,
} from 'material-ui/Stepper';


const styles = {
  block: {
    maxWidth: 250,
  },
  radioButton: {
    marginBottom: 16,
  },
  radioButton1: {
    marginBottom: 16,
    display: 'none',
  },
  addAddress: {
    lineHeight: 4,
  }
};

const lightMuiTheme = getMuiTheme(lightBaseTheme);

class OrderCheckout extends React.Component {

  constructor() {
    super();
    UserDetailStore.fetchUserBasicDetails()
    this.getSignInStep = this.getSignInStep.bind(this);
    this.handlePayment = this.handlePayment.bind(this);
    this.state = {
      stepIndex: 0,
      selectedAddress: false,
      openAddAddressPopup: false,
      open: false,
      orders: null,
      order_price: null,
      signedIn: false,
      isMobile: false,
      mobileVerified: false,
      isVerifyMobileEnable: false,
      mobileNumber: null,
      isSignUpDialogue: false,
      selectedPaymentMethod: "payu",
    }
  }

  componentWillMount() {
    UserDetailStore.on("change", this.getSignInStep);
    OrderStore.on('change', this.getOrderUserDetail)
  }

  componentWillUnmount() {
    UserDetailStore.removeListener("change", this.getSignInStep);
    OrderStore.removeListener('change', this.getOrderUserDetail)
  }

  getOrderUserDetail = () => {
    this.setState({
      orders : OrderStore.getOrderDetailOfUser(),
      order_price : OrderStore.getordersPrice()
    })
  }

  getSignInStep(){
    this.setState({
      signedIn: UserDetailStore.is_user_authenticated(),
      isMobile: UserDetailStore.getUserDetail()[2] != '',
      mobileVerified: UserDetailStore.isUserAuthenticatedAndMobileVerified(),
      mobileNumber: UserDetailStore.getUserDetail()[2],
      isVerifyMobileEnable: UserDetailStore.getUserDetail()[2] != '',
    })
  }

  onChangeMobileNumber = (event) => {
    var mobileNoRegex = new RegExp("\\d{10}$");
        if (mobileNoRegex.test(event.target.value) && event.target.value.length == 10 ){
          this.setState({ mobileErrorText: '', mobileNumber: event.target.value, isVerifyMobileEnable: true })
        }
        else if (event.target.value == ''){
          this.setState({ mobileErrorText: 'This field is required', isVerifyMobileEnable: false })
        }
        else {
          this.setState({ mobileErrorText: 'Please enter a valid 10 digit number',isVerifyMobileEnable: false }) 
        }
  }

  getUserDetailOrderPage(){
    const currentPath = window.location.pathname;
    const googleSignInPath = "/login/google-oauth2/?next=" + currentPath ;
    const facebookCurrentPath = "/login/facebook/?next=" + currentPath ;
     if(this.state.signedIn){
        if (!this.state.isMobile){
          return (
          <div>
          <p>You are Signed In, Please verify your mobile no to proceed</p>
          <TextField
            hintText="Mobile Number"
            errorText= {this.state.mobileErrorText}
            onChange={this.onChangeMobileNumber.bind(this)}
          />
          <br/>
          <br/>
          <VerifyOTP mobile={this.state.mobileNumber} enable = {this.state.isVerifyMobileEnable} isUserLoggedIn = {true}/> 
          </div>
         )
        }
        else if (this.state.mobileVerified){
          return (
            <div>
            <p>You are signed in, Please click next and select Address</p>
            <RaisedButton
                label="Next"
                disableTouchRipple={true}
                disableFocusRipple={true}
                primary={true}
                onTouchTap={this.handleNext}
                style={{marginRight: 12}}
              />
            </div>
            )
        }
        else{
          console.log('user is signed in and mobile not verified')
          console.log(this.state.mobileNumber)
          return (
            <div>
            <p>You are Signed In, Please verify your mobile no to proceed</p>
            <TextField
              hintText="Mobile Number"
              errorText= {this.state.mobileErrorText}
              onChange={this.onChangeMobileNumber.bind(this)}
              defaultValue={this.state.mobileNumber}
            />
            <br/>
            <br/>
            <VerifyOTP mobile={this.state.mobileNumber} enable = {this.state.isVerifyMobileEnable}/> 
            </div>
           )
        }
      }
      else{
        return (
          <div>
             <SignIn />
          <p>Dont have account ?
              <SignUp enabled = {this.state.isSignUpDialogue}/> 
              </p>
              <div >
                <a href={facebookCurrentPath} className="btn-default facebook"> <i className="fa fa-facebook modal-icons"></i> Sign In with Facebook </a>
                <br />
                <a href={googleSignInPath} className="btn-default google"> <i className="fa fa-google-plus modal-icons"></i> Sign In with Google </a>
              </div> 
              </div>
          )
      }
  }

  getUserAddresses(){
    return !UserDetailStore.getUserDetail()[5] ? null : UserDetailStore.getUserDetail()[5]['customer_address_list'];
  }

  handleNext = () => {
    const stepIndex = this.state.stepIndex;
    if (stepIndex < 2) {
      this.setState({stepIndex: stepIndex + 1});
    }
  };

  handlePrev = () => {
    const {stepIndex} = this.state;
    if (stepIndex > 0) {
      this.setState({stepIndex: stepIndex - 1});
    }
  };

  handlePayment = () => {
    if (this.state.selectedPaymentMethod == 'pay'){
      window.location.href = "/process-payment/" + this.state.order_price.txid;
    }
    else if (this.state.selectedPaymentMethod == 'paytm'){
     window.location.href = "/paytm/payment/" + this.state.order_price.txid; 
    }
    else if (this.state.selectedPaymentMethod == 'cod'){
      window.location.href = "/process-cod/" + this.state.order_price.txid;
    }
  }
  
  handleAddressPopUpValidation = () => {
    if (this.refs.txtName.getValue().length > 0 
        && this.refs.txtAddress.getValue().length > 0
        && this.refs.txtAddressCity.getValue().length > 0
        && this.refs.txtAddressState.getValue().length > 0
        && this.refs.txtAddressPincode.getValue().length == 6
        && this.refs.txtAddressMobile.getValue().length == 10 )
    {
      UserDetailStore.updateCustomerAddress(
        this.refs.txtName.getValue(),
        this.refs.txtAddress.getValue(),
        this.refs.txtAddressCity.getValue(),
        this.refs.txtAddressState.getValue(),
        this.refs.txtAddressPincode.getValue(),
        this.refs.txtAddressMobile.getValue()
      );
      this.setState({openAddAddressPopup: false});
    }
    else{
      alert('fill all fields');
    }
  }

  handleContinueAddress = () => {
    OrderStore.fetchOrderDetailOfUser(
      window.location.pathname.split('/')[2],
      this.state.selectedAddress['name'],
      this.state.selectedAddress['address'],
      this.state.selectedAddress['city'],
      this.state.selectedAddress['state'],
      this.state.selectedAddress['pincode'],
      this.state.selectedAddress['mobile'],
      );
    this.setState({stepIndex: 2});
  }

  renderStepActions(step) {
    var lableText = step == 2 ? 'Change Delivery Address' : 'Back'
    return (
      <div style={{margin: '12px 0'}}>
      {step != 2 && (
        <RaisedButton
          label="Next"
          disableTouchRipple={true}
          disableFocusRipple={true}
          primary={true}
          onTouchTap={this.handleNext}
          style={{marginRight: 12}}
        />)}
        {step > 0 && (
          <FlatButton
            label={lableText}
            disableTouchRipple={true}
            disableFocusRipple={true}
            onTouchTap={this.handlePrev}
          />
        )}
      </div>
    );
  }

  render() {
    const {stepIndex} = this.state;
    const addressDailogue = this.state.openAddAddressPopup;

    const order_subtotal = !this.state.order_price ? null : this.state.order_price['order_subtotal'];
    const order_total_amount = !this.state.order_price ? null : this.state.order_price['order_total_amount'];
    const promotionalMoney = !this.state.order_price ? null : this.state.order_price['discount'];
    const tax = !this.state.order_price ? null : this.state.order_price['tax'];
    const total_shipping_charge = !this.state.order_price ? null : this.state.order_price['total_shipping_charge'];
    const final_price = !this.state.order_price ? null : this.state.order_price['final_price'];
    const cod_charges = !this.state.order_price ? null : this.state.order_price['cod_charges'];
    const total_price = !this.state.order_price ? null : this.state.selectedPaymentMethod != 'cod' ? parseInt(final_price) : parseInt(final_price) + parseInt(cod_charges);

    const addressRadioButton = !this.getUserAddresses() ? null : this.getUserAddresses().map(function(address, map){
      return (
      <RadioButton
                  value={address}
                  label={address['name'] + ', ' + address['address'] + ', ' + address['city'] + ' ' + address['state'] + '\n' + address['pincode'] + '\n +91 ' + address['mobile'] }
                  style={styles.radioButton}
      />)
    });

    const signIn = this.getUserDetailOrderPage();

    const addAddressDialogue = (function(){
      return (
        <Dialog
            title="Enter a New Shipping Address"
            modal={true}
            open={addressDailogue}
          >
          <TextField
            hintText="Name"
            ref="txtName"
            type='text'
          /><br />
          <TextField
            hintText="Area/ Locality/ Landmark"
            ref="txtAddress"
            type='text'
            maxLength="200"
          /><br />
          <TextField
            hintText="City"
            ref="txtAddressCity"
            type='text'
            maxLength="60"
          /><br />
          <TextField
            hintText="State"
            ref="txtAddressState"
            type='text'
            maxLength="60"
          /><br />
          <TextField
            hintText="Pincode"
            ref="txtAddressPincode"
            type='number'
            maxLength="6"
          /><br />
          <TextField
            hintText="Mobile Number"
            ref="txtAddressMobile"
            type='tel'
            maxLength="10"
          /><br />
          <FlatButton
            label="Cancel"
            primary={true}
            onTouchTap={() => this.setState({openAddAddressPopup: false})}
          />
          <FlatButton
            label="Submit"
            primary={true}
            keyboardFocused={true}
            onTouchTap={this.handleAddressPopUpValidation.bind(this)}
          />
          </Dialog>
        )
    }).bind(this)();
    const orders = this.state.orders
    const orderComponents =  !orders ? null : orders.map(function(order, index){
      var orderProperty = [];
      for(var p in order){
        if(order.hasOwnProperty(p) && p != 'product' && p != 'photo'){
          orderProperty.push(p);
        }
      }
      const orderPropertyComponents =  !orderProperty ? null : orderProperty.map(function(orderProperty, index){
      return (
              <div>
                <p>{orderProperty} : {order[orderProperty]} </p>
              </div>
          )
      });
      return (
      <ListItem
        key={index + 1}
        primaryText={order['name']}
        secondaryText={order['price_without_shipping_charge']}
        leftAvatar={<Avatar src={order['image']} />}
        // nestedItems={[<Paper style={styles.orderdetail} zDepth={1}>
        //   {orderPropertyComponents}
        //   </Paper>
        // ]}
      />)
    })

    return (
      <MuiThemeProvider muiTheme={lightMuiTheme}>
      <Paper>
      <div style={{maxWidth: 500, margin: 'auto'}}>
        
        <Stepper
          activeStep={stepIndex}
          linear={false}
          orientation="vertical"
        >

          <Step>
            <StepLabel>
              Sign In
            </StepLabel>
            <StepContent>
              {signIn}
            </StepContent>
          </Step>


          <Step>
            <StepLabel>Select Address</StepLabel>
            <StepContent>
              <RadioButtonGroup name="address" onChange={(event, value)=> this.setState({selectedAddress: value})} defaultSelected={this.state.selectedAddress}>
              {addressRadioButton}
              </RadioButtonGroup>
              <br/>
              <div>
              <FloatingActionButton mini={true} style={{margin: 10}} onTouchTap={()=> this.setState({openAddAddressPopup: true})}>
                <ContentAdd />
              </FloatingActionButton>
              <a style={styles.addAddress}>Add Address</a>
              </div>
              <br/>
              <FlatButton
                label="Back"
                disableTouchRipple={true}
                disableFocusRipple={true}
                onTouchTap={this.handlePrev}
              />
              <RaisedButton label="Continue" disabled={(this.state.selectedAddress == false)} onTouchTap={this.handleContinueAddress} />
            </StepContent>

          </Step>

          <Step>
            <StepLabel>
              Review Order
            </StepLabel>
            <StepContent>
              <p>
                Your Order will be delivered on below address: 
              </p>
              <p>
                {this.state.selectedAddress['name'] + ', ' + this.state.selectedAddress['this.state.selectedAddress'] + ', ' + this.state.selectedAddress['city'] + ' ' + this.state.selectedAddress['state'] + '\n' + this.state.selectedAddress['pincode'] + '\n +91 ' + this.state.selectedAddress['mobile'] }
              </p>
              <div style={{marginLeft:20, padding:10}}>
              <Paper  style={{width: 300, padding:20}} zDepth={1} rounded={false} >
                <p><i className='bold'> Sum </i> - {convertToINR(order_subtotal)} </p>
                 
                <p><i className='bold'>Shipping Charge</i> - {convertToINR(total_shipping_charge)} </p>
                 
                 <p><i className='bold'>Promotional Money</i> - Rs. {convertToINR(promotionalMoney)} </p>
                 
                 <p><i className='bold'>AB Cash</i> - {convertToINR(order_total_amount - final_price)} </p>
                 
                <p><i className='bold'>Payble Amount</i> - Rs. {convertToINR(final_price)} </p>
                 <Divider />
              </Paper>
              </div>
              {this.renderStepActions(2)}
              <List>
                <Subheader>Products :</Subheader>
                {orderComponents}
              </List>
              <br/>
              <br/>
              <Divider />
              <h3>Easy Payment :</h3>
              <Divider />
              <br/>
              <RadioButtonGroup name="payment" onChange={(event, value)=> this.setState({selectedPaymentMethod: value})} defaultSelected={this.state.selectedPaymentMethod}>
                <RadioButton
                    value="pay"
                    label="Credit/Debit Card or NetBanking"
                    style={styles.radioButton}
                />
               <RadioButton
                            value="paytm"
                            label="Paytm Wallet"
                            style={styles.radioButton}
                        />
                <RadioButton
                    value="cod"
                    label={"Cash On Delivery (Extra COD Charges will be applicable : " + convertToINR(parseInt(cod_charges)) + ")"}
                    style={styles.radioButton}
                />
              </RadioButtonGroup>

              <RaisedButton
                label={this.state.selectedPaymentMethod + " " + convertToINR(total_price)} 
                disableTouchRipple={true}
                disableFocusRipple={true}
                primary={true}
                onTouchTap={this.handlePayment}
                style={{marginRight: 12}}
              />
              <br/>
              <br/>
              <br/>
              <Divider />
              <br/>
              <br/>
              <br/>
            </StepContent>
          </Step>


        </Stepper>
        {addAddressDialogue}
      </div>
      </Paper>
      </MuiThemeProvider>
    );
  }
}

export default OrderCheckout;
