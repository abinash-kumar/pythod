import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'

import ArtistDetails from '../myaccount/ArtistDetails.jsx';
import ArtistDesigns from './ArtistDesigns.jsx';
import UploadDesignPopUp from './UploadDesignPopUp.jsx';
import HeaderUserCard from '../myaccount/HeaderUserCard.jsx'

import Divider from 'material-ui/Divider';

const lightMuiTheme = getMuiTheme(lightBaseTheme);

class ArtistHome extends React.Component {
    constructor(props) {
        super(props);

    }

    render() {
        return (
            <MuiThemeProvider muiTheme={lightMuiTheme}>
                <div>
                    <HeaderUserCard/>
                    <div className="container">
                        <div className="row">
                            <div className="col-sm-6 col-xs-12 pad-10 els">
                                <ArtistDetails/>
                            </div>
                            <div className="col-sm-6 col-xs-12 pad-10 els">
                                <div className="pad-10">
                                    <UploadDesignPopUp/>
                                </div>
                            </div>
                        </div>
                        <ArtistDesigns/>
                    </div>
                </div>
            </MuiThemeProvider>
        )
    }
}
export default ArtistHome;