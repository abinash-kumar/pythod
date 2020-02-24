import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import ContentAdd from 'material-ui/svg-icons/content/add';
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField';
var injectTapEventPlugin = require("react-tap-event-plugin");
injectTapEventPlugin();


/**
 * Dialog with action buttons. The actions are passed in as an array of React objects,
 * in this example [FlatButtons](/#/components/flat-button).
 *
 * You can also close this dialog by clicking outside the dialog, or with the 'Esc' key.
 */


class LoginBox extends React.Component {
  
  render () {

    return (
      <div>
      <TextField
      hintText=""
      floatingLabelText="Email"/>
      <TextField
      hintText=""
      floatingLabelText="Password"
      type="password"/>
      <br></br>
      <RaisedButton label="Login" primary={true}/>
      </div>
      );
  }
}


 class Login extends React.Component {

   constructor(props) {
     // code...
     super(props);
     this.state = {
       open: false,
     };
   }
   handleOpen ()  {
     this.setState({open: true});
   };

   handleClose ()  {
     this.setState({open: false});
   };


   render() {
     const actions = [
     <FlatButton
     label="Cancel"
     primary={true}
     onTouchTap={this.handleClose.bind(this)}
     />,
     ];

     return (
       <div>
       <RaisedButton label="Login" onTouchTap={this.handleOpen.bind(this)} />

       <Dialog
       title="Login in your account"
       actions={actions}
       modal={true}
       open={this.state.open}
       onRequestClose={this.handleClose.bind(this)}
       >
       <LoginBox></LoginBox>
       </Dialog>
       </div>
       );
   }
 }

 export default Login;