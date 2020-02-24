import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'
import HeaderUserCard from './myaccount/HeaderUserCard.jsx'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'

const lightMuiTheme = getMuiTheme(lightBaseTheme);

class HeaderMenu extends React.Component {
    constructor(props){
        super(props);
    }

    componentWillMount() {
    }

   componentDidMount() {
   }

    render(){
        self=this;
        return (
            <MuiThemeProvider muiTheme={lightMuiTheme}>
                <div>
                    <HeaderUserCard/>
                </div>
            </MuiThemeProvider>
        )
    }
}
export default HeaderMenu;