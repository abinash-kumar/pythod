import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'
import { List, ListItem } from 'material-ui/List';
import Avatar from 'material-ui/Avatar';
import Paper from 'material-ui/Paper';
import Divider from 'material-ui/Divider';
import HeaderUserCard from '../myaccount/HeaderUserCard.jsx'
import API from '../../store/API.js';
import BreadCrumb from '../abcomponents/BreadCrumb.jsx';
import Stagger from 'react-css-stagger';
import ArtistStore from '../../store/ArtistStore.jsx';

const lightMuiTheme = getMuiTheme(lightBaseTheme);
const stylePaper = {
    display: 'inline-block',
    width: '100%',
    height: '400px',
    borderRadius: '10px',
    opacity: '1',
};

const style = { margin: 1 };
const styleList = { padding: '16px 16px 16px 50px' }

const paperBody = (name, no_of_arts, about, link, imageUrl) => (<div>
    <a target='__blank' href={link}>
        <div className="col-sm-12 col-xs-12 pad-10" >
            <center>
                <Avatar
                    src={imageUrl}
                    size={230}
                    alt={"Addiction Bazaar Artist - " + name}
                    style={style} />
            </center>
        </div>
        <div className="col-sm-12 col-xs-12 ells" >
            <center>
                <h1 className="artist-all-name">{name}</h1>
                <h2 className="artist-all-art-count">Arts- {no_of_arts}</h2>
                <div className="artist-all-about">
                    <h3 className="ellsps">{about}</h3>
                </div>
            </center>
        </div>
    </a>
</div>);


class ArtistAll extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            artist_data: [],
            breadCrumb: []
        };
        API.fetchAllArtists();
    }

    componentWillMount() {
        ArtistStore.on("change", this.setAllArtist);
    }

    // getAllArtist = () => {
    //     self = this;
    //     API.fetchAllArtists(function (data) {
    //         self.setState({ artist_data: data.artist_data, breadCrumb: data.breadcrumb });
    //     });
    // };

    setAllArtist = () => {
        self = this;
        let artist_data = ArtistStore.getAllArtist().artist_data;
        let breadCrumb = ArtistStore.getAllArtist().breadcrumb;
        self.setState({ artist_data, breadCrumb });
    };


    render() {
        const image = <div style={{ overflow: 'hidden', }} className="col-sm-4 col-xs-4 fr">
            <img height="300px" src="/static/img/artistallbanner.png" alt="Artist Banner- Addiction Bazaar" />
        </div>
        const artist_data = this.state.artist_data;
        const allArtists = [];
        for (var i = 0; i < this.state.artist_data.length; i++) {
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
            <MuiThemeProvider muiTheme={lightMuiTheme}>
                <div>
                    <HeaderUserCard />
                    <BreadCrumb bList={this.state.breadCrumb} />
                    <div className="container">
                        <div className="row">
                            <div className="col-sm-12 col-xs-12">
                                <Stagger transition="fadeIn" delay={200}>
                                    <div className="col-sm-8 col-xs-8">
                                        <div className="artist-all-quote">
                                            <p className="artist-all-quote-text">You Don't Take a Photograph.</p>
                                            <h1 className="artist-all-quote-text2">you make it...</h1>
                                        </div>
                                    </div>
                                    {image}
                                </Stagger>
                            </div>
                            <br />
                            <h1 className="artist-all-quote-meet-text artist-all-quote">Meet Our Artists and Explore their Ideas</h1>
                            <Stagger transition="fadeIn" delay={200}>
                                {allArtists}
                            </Stagger>
                        </div>
                    </div>
                </div>
            </MuiThemeProvider>
        )
    }
}
export default ArtistAll;