import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'
import { Tabs, Tab } from 'material-ui/Tabs';
import Divider from 'material-ui/Divider';
import { Card, CardMedia, CardTitle } from 'material-ui/Card';
import Avatar from 'material-ui/Avatar';
import HeaderUserCard from '../myaccount/HeaderUserCard.jsx'
import ProductModal from '../product/ProductModal.jsx'
import API from '../../store/API.js';
import Stagger from 'react-css-stagger';
import Masonry from 'react-masonry-component';
import BreadCrumb from '../abcomponents/BreadCrumb.jsx';

const lightMuiTheme = getMuiTheme(lightBaseTheme);

const styles = {
    headline: {
        fontSize: 24,
        paddingTop: 16,
        marginBottom: 12,
        fontWeight: 400
    }
};

const DesignCard = (title, url, link, i) => (
    <div className="col-sm-4 col-xs-6 pad-10" key={i}>
        <a href={link} target="_blank">
            <Card>
                <CardMedia>
                    <img className="artist-design-image" src={url} alt={"tshirt Design -" + title + " at Addiction Bazaar"} />
                </CardMedia>
                <CardTitle
                    titleStyle={{
                        'fontSize': '2vh',
                        'lineHeight': '16px'
                    }}
                    title={title} />
            </Card>
        </a>
    </div>
);

class ArtistProfile extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: 'a',
            firstName: '',
            lastName: '',
            about: '',
            userPhotoUrl: '',
            artistDesigns: [],
            allProductData: [],
            breadCrumb: []
        };
        this.getArtistDesigns();
    }

    getArtistDesigns = () => {
        self = this;
        const id = window
            .location
            .href
            .split("/")[5];
        API.fetchArtistDesignsPublic(id, function (data) {
            self.setState({
                artistDesigns: data.designs,
                allProductData: data.product_detail_list,
                firstName: data.first_name,
                lastName: data.last_name,
                about: data.about,
                userPhotoUrl: data.user_photo,
                breadCrumb: data.breadcrumb
            });
        });

    };

    handleChange = (value) => {
        this.setState({ value: value });
    };

    render() {
        const allProductData = this.state.allProductData;
        const products = [];
        for (var i = 0; i < allProductData.length; i++) {
            products.push(
                <div className='col-sm-4 col-xs-6' key={i}>
                    <ProductModal
                        productSlug={allProductData[i].slug}
                        productID={allProductData[i].id}
                        product={allProductData[i]} />
                </div>
            );
        }
        const cards = [];
        for (var i = 0; i < this.state.artistDesigns.length; i++) {
            cards.push(DesignCard(this.state.artistDesigns[i].title, this.state.artistDesigns[i].image, this.state.artistDesigns[i].link, i));
        }
        return (
            <MuiThemeProvider muiTheme={lightMuiTheme}>
                <div>
                    <HeaderUserCard />
                    <BreadCrumb bList={this.state.breadCrumb} />
                    <div className="container-fw grad">
                        <br /><br /><br />
                        <div className="row container-full">
                            <div className="col-sm-4 col-xs-12 fr">
                                <center>
                                    <Avatar src={this.state.userPhotoUrl} alt={this.state.firstName + " " + this.state.lastName + " - Artist at Addiction Bazaar"} size={200} />
                                </center>
                            </div>
                            <div className="col-sm-8 col-xs-12 fl">
                                <center>
                                    <h1 className="master-heading">{this.state.firstName}<br />{this.state.lastName}</h1>
                                    <h2 className="master-subheading">{this.state.about}</h2>
                                </center>
                            </div>
                        </div>
                        <br /><br /><br />
                    </div>
                    <br />
                    <div className="container-full">
                        <Tabs value={this.state.value} onChange={this.handleChange}>
                            <Tab label="Designs" value="a">
                                <div className="container">
                                    <Masonry>
                                        {cards}
                                    </Masonry>
                                </div>
                            </Tab>
                            <Tab label="T-Shirts" value="b">
                                <div className="container">
                                    <Stagger transition="fadeIn" delay={200}>
                                        {products}
                                    </Stagger>
                                </div>
                            </Tab>
                        </Tabs>

                    </div>
                </div>
            </MuiThemeProvider>
        )
    }
}
export default ArtistProfile;