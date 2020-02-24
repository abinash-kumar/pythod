import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'
import ProductSearch from './ProductSearch.jsx'
import auraaiStore from '../../store/AuraaiStore.jsx';
import ProductListing from '../product/ProductListing.jsx'
import * as AuraaiActions from "../../actions/AuraaiAction.jsx";

const lightMuiTheme = getMuiTheme(lightBaseTheme);



class ProductSearchPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            searchKey: '',
        };
    }

    render() {
        return (
            <MuiThemeProvider muiTheme={lightMuiTheme}>
                <div>
                    <nav>
                        <ul className="breadcrumb">
                            <li><a href="/" rel="index up up up">home</a></li>
                            <li><a href="#" rel="up up">search</a></li>
                        </ul>
                    </nav>
                    <ProductSearch searchKey={this.setState.searchKey} />
                    <div className="container">
                        <div className="row">
                            <ProductListing product="search" banner={false} />
                        </div>
                    </div>
                </div>
            </MuiThemeProvider>
        )
    }
}
export default ProductSearchPage;