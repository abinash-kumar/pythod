import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'
import Chip from 'material-ui/Chip';
import ProductModal from '../product/ProductModal.jsx'
import API from '../../store/API.js';
import Masonry from 'react-masonry-component';
import HeaderUserCard from '../myaccount/HeaderUserCard.jsx'

const lightMuiTheme = getMuiTheme(lightBaseTheme);



class FbMagicSearch extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            allProductData: [],
        };
        this.getMagicSearchData();
    }

    getMagicSearchData = () => {
        self = this;
        API.fetchFbMagicSearchData(function (data) {
            self.setState({ allProductData: data.product_detail_list });
        });

    };

    render() {
        const allProductData = this.state.allProductData;
        const products = [];
        for (var i = 0; i < allProductData.length; i++) {
            var likes = []
            for (var j = 0; j < allProductData[i].fb_likes.length; j++) {
                likes.push(
                    <Chip
                        style={{ margin: 4, }}
                    >
                        {allProductData[i].fb_likes[j]}
                    </Chip>
                );
            }
            products.push(
                <div className='col-sm-4 col-xs-6 pad-10'>
                    <div className='col-sm-12 col-xs-12'>
                        <ProductModal productSlug={allProductData[i].slug} productID={allProductData[i].id} product={allProductData[i]} />
                    </div>
                    <div className='col-sm-12 col-xs-12' style={{ display: 'flex', flexWrap: 'wrap', }}>
                        {likes}
                    </div>
                </div>);
        }
        return (
            <MuiThemeProvider muiTheme={lightMuiTheme}>
                <div className="container-fw">
                    <HeaderUserCard />
                    <nav>
                        <ul className="breadcrumb">
                            <li><a href="/" rel="index up up up">home</a></li>
                            <li><a href="#" rel="up up">magic-search</a></li>
                        </ul>
                    </nav>
                    <center>
                        <h2 style={{ fontSize: "25px", }}>Products Based On Your Facebook Likes</h2>
                    </center>
                    <Masonry>
                        {products}
                    </Masonry>
                </div>
            </MuiThemeProvider>
        )
    }
}
export default FbMagicSearch;