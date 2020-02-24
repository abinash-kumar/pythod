import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'
import { Card, CardHeader, CardMedia, CardTitle, CardText } from 'material-ui/Card';
import Home from '../../components/Home.jsx';

import { FadeInUp } from "animate-components";

import AuraaiStore from '../../store/AuraaiStore.jsx';
import { BrowserRouter } from 'react-router-dom';
import { Switch, Route } from 'react-router-dom';
import { Link } from 'react-router-dom';
import ProductListing from '../product/ProductListing.jsx'

const lightMuiTheme = getMuiTheme(lightBaseTheme);

class TagBanner extends React.Component {
    constructor(props) {
        super(props);
        this.getAllBanners = this.getAllBanners.bind(this);
        this.state = {
            allBanners: null,
        };
        AuraaiStore.fetchAllBanners();
    }

    getAllBanners() {
        this.setState({
            allBanners: AuraaiStore.getAllBanners()
        })
    }

    componentWillMount() {
        AuraaiStore.on("change", this.getAllBanners);
    }



    render() {
        self = this;
        const allBanners = self.state.allBanners
        const CardExampleWithAvatar = (i) => (
            <FadeInUp duration="1s" timingFunction="ease-out" as="div">
                <a href={"/product/tag/" + allBanners.banners[i].slug}>
                    <Card>
                        <CardMedia
                            overlay={<CardTitle title={allBanners.banners[i].name} titleStyle={{ fontFamily: "'Montserrat', sans-serif", color: 'rgb(11, 168, 155)', fontSize: '2vh', lineHeight: '12px' }} />}
                            overlayContentStyle={{ background: 'None' }}
                            overlayStyle={{ background: 'None', font: "'Montserrat', sans-serif", color: '#000' }}
                        >
                            <img src={allBanners != null ? allBanners.banners[i].image : ""} alt={"Addiction Bazaar Prosucts - " + allBanners.banners[i].name} style={{ width: '100%' }} />
                        </CardMedia>
                    </Card>
                </a>
            </FadeInUp>
        );
        const l = allBanners != null ? allBanners.banners.length : 0
        var lis = [];
        for (var i = 0; i < l; i++) {
            lis.push(<div key={i} className="col-sm-3 col-xs-6 pad-10">
                {CardExampleWithAvatar(i)}
            </div>);
        }
        const banner = <div className="container-full">
            <div className="row">
                {lis}
            </div>
        </div>
        return (
            <div>
                <div>
                    {banner}
                </div>
            </div>
        )
    }
}
export default TagBanner;