import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'

import TextField from 'material-ui/TextField';
import {orange500, blue500} from 'material-ui/styles/colors';
import Snackbar from 'material-ui/Snackbar';

import API from '../../store/API'


const lightMuiTheme = getMuiTheme(lightBaseTheme);

export default class ForgetPasswordPopUp extends React.Component {
  state = {
    open: false,
    isSubmitEnable: true,
    email:"",
    showMailSent:false,
  };

    onChangeEmail = (event) => {
        var emailRegex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if (emailRegex.test(event.target.value)){
            this.setState({
                email : event.target.value,
                errorTextEmail: '',
                isSubmitEnable: false,
            });
        }
        else if (event.target.value == ''){
            this.setState({
                errorTextEmail: 'Please Enter Eamil',
                mobile : event.target.value,
                isSubmitEnable: true,
            })	
        }
        else{
            this.setState({
                errorTextEmail: 'Please Enter valid Email',
                email : event.target.value,
                isSubmitEnable: true,
            })	
        }
        console.log(this.state.email)
    }


  handleOpen = () => {
    this.setState({open: true});
  };

  handleClose = () => {
    this.setState({open: false});
  };

  handleMailNotification = () => {
      this.setState({showMailSent:true})
  }

  handleSubmit = () => {
      self = this;
    API.resetPasswordSendMail(
        this.state.email,
        function(data){
        if (data.success){
            console.log('Done')
            self.handleClose();
        }
        else{
            console.log('Not Done')
        }
    })
    self.handleMailNotification();
  }

  render() {
    const actions = [
      <FlatButton
        label="Cancel"
        primary={true}
        onClick={this.handleClose}
      />,
      <FlatButton
        label="Submit"
        primary={true}
        keyboardFocused={true}
        onTouchTap={this.handleSubmit}
        disabled = {this.state.isSubmitEnable}
      />,
    ];

    return (
        <MuiThemeProvider muiTheme={lightMuiTheme}>
            <div>
                <a className="clickable fr" onClick={this.handleOpen} >Reset Password</a>
                <Dialog
                title="Dont worry just enter your registered email."
                actions={actions}
                modal={false}
                open={this.state.open}
                onRequestClose={this.handleClose}
                >
                <TextField
                floatingLabelText="Enter Your Email Here"
                floatingLabelStyle={{color: blue500,}}
                floatingLabelFocusStyle={{color: blue500,}}
                onChange={this.onChangeEmail.bind(this)}
                errorText= {this.state.errorTextEmail}
                />
                </Dialog>
                <Snackbar
                    open={this.state.showMailSent}
                    message="Email Sent Successfully Please Check Your Inbox "
                    autoHideDuration={2000}
                    bodyStyle={{zIndex:2000}}
                />
            </div>
        </MuiThemeProvider>
    );
  }
}