import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'
import { Tabs, Tab } from 'material-ui/Tabs';

const lightMuiTheme = getMuiTheme(lightBaseTheme);

const stylesTabs = {
    headline: {
        fontSize: 24,
        paddingTop: 16,
        marginBottom: 12,
        fontWeight: 400,
    },
};


class TabView extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const searchBox = <div> <input type="text" /> </div>
        return (
            <MuiThemeProvider muiTheme={lightMuiTheme}>
                <div>
                    Being REACTIVE !!!
                    {searchBox}
                </div>
            </MuiThemeProvider>
        )
    }
}
export default TabView;