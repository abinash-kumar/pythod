import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'

const lightMuiTheme = getMuiTheme(lightBaseTheme);



class ProductTagSearch extends React.Component {
    constructor(props){
        super(props);

    }
    
    render(){
        const searchBox =<div> <input type="text" /> </div>
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
export default ProductTagSearch;