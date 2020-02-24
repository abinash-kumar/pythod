import React from 'react';
import ReactDOM from 'react-dom';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import MyAwesomeReactComponent from './MyAwesomeReactComponent.jsx';
import Login from './Login.jsx';

 
const App = () => (
  <MuiThemeProvider>
  	<Login />
  </MuiThemeProvider>
);
 
ReactDOM.render(
  <App />,
  document.getElementById("login")
);