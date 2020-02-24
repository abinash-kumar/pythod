import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'
import { List, ListItem } from 'material-ui/List';
import Avatar from 'material-ui/Avatar';
import Paper from 'material-ui/Paper';

import API from '../../store/API.js';
import ArtistStore from '../../store/ArtistStore.jsx';

import Call from 'material-ui/svg-icons/communication/call';
import Email from 'material-ui/svg-icons/communication/email';
import Link from 'material-ui/svg-icons/content/link';
import UserIcon from 'material-ui/svg-icons/action/account-circle';

import Divider from 'material-ui/Divider';
import Slider from 'react-slick';


const lightMuiTheme = getMuiTheme(lightBaseTheme);
const stylePaper = {
    display: 'inline-block',
    width: '100%',
    height: '350px',
    borderRadius: '10px',
    opacity: '1',
};

const style = { margin: 1 };
const styleList = { padding: '16px 16px 16px 50px' }

class SampleNextArrow extends React.Component {
    constructor(props) {
        super(props);
    }
    render() {
        const className = this.props.className
        const style = this.props.style
        const onClick = this.props.onClick
        const mystyle = function () {
            console.log(className)
            if (className.indexOf("slick-disabled") >= 0) {
                return { opacity: '0.4' };
            }
        }();
        return (
            <div
                className={'right-arrow'}
                style={mystyle}
                onClick={onClick}
            ></div>
        )
    }
}


class SamplePrevArrow extends React.Component {
    constructor(props) {
        super(props);
    }
    render() {
        const className = this.props.className
        const style = this.props.style
        const onClick = this.props.onClick
        const mystyle = function () {
            console.log(className)
            if (className.indexOf("slick-disabled") >= 0) {
                return { opacity: '0.4' };
            }
        }();
        return (
            <div
                className={'left-arrow'}
                style={mystyle}
                onClick={onClick}
            ></div>
        )
    }
}


const paperBody = (name, no_of_arts, about, link, imageUrl) => (<div>
    <a target='__blank' href={link}>
        <div className="col-sm-12 col-xs-12 pad-10" >
            <center>
                <Avatar
                    src={imageUrl}
                    size={230}
                    alt={"Addiction Bazaar artist - " + name}
                    style={style} />
            </center>
        </div>
        <div className="col-sm-12 col-xs-12 ells" >
            <center>
                <h1 className="artist-all-name">{name}</h1>
            </center>
        </div>
    </a>
</div>);


class ArtistAllMin extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            artist_data: [],
            noOfArtists: 5,
        };
        API.fetchAllArtists();
    }

    componentWillMount() {
        ArtistStore.on("change", this.setAllArtist);
    }

    setAllArtist = () => {
        self = this;
        self.setState({ artist_data: ArtistStore.getAllArtist() });
    };



    render() {
        const isMobile = window.innerWidth <= 500 || getValueOfParam('mobile');
        const artist_data = this.state.artist_data.artist_data;
        const allArtists = [];
        const l = !artist_data ? 0 : artist_data.length > this.state.noOfArtists ? this.state.noOfArtists : artist_data.length

        var settings = {
            dots: true,
            infinite: true,
            arrows: true,
            slidesToShow: isMobile ? 1 : 3,
            slidesToScroll: isMobile ? 1 : 3,
            nextArrow: <SampleNextArrow />,
            prevArrow: <SamplePrevArrow />,
        }
        for (var i = 0; i < l; i++) {
            allArtists.push(
                <div key={i} className="col-sm-4 col-xs-12 pad-10 artist-all-hover" >
                    <Paper style={stylePaper}
                        rounded={true}
                        zDepth={2}
                        rounded={false}
                        children={paperBody(artist_data[i].first_name + ' ' + artist_data[i].last_name,
                            artist_data[i].no_of_arts,
                            artist_data[i].about,
                            artist_data[i].link,
                            artist_data[i].user_photo)} />
                </div>
            );
        }
        return (
            <div className="container">
                <div className="row">
                    <a className="btn btn-primary abtn side" target="_blank" href="/artist/all">View all artist</a>
                    <Slider autoplay="true"  {...settings}>
                        {allArtists}
                    </Slider>
                </div>
            </div>
        )
    }
}
export default ArtistAllMin;