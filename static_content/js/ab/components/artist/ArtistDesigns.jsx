import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'
import {
    Card,
    CardActions,
    CardHeader,
    CardMedia,
    CardTitle,
    CardText
} from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';
import Dialog from 'material-ui/Dialog';
import Delete from 'material-ui/svg-icons/action/delete';
import * as UserActions from "../../actions/UserActions.jsx";
import ArtistStore from '../../store/ArtistStore.jsx';
import API from '../../store/API.js';
import EditDesign from './EditDesign.jsx';
import Masonry from 'react-masonry-component';

const lightMuiTheme = getMuiTheme(lightBaseTheme);

class ArtistDesigns extends React.Component {
    constructor(props) {
        super(props);
        this.getArtistDesigns = this
            .getArtistDesigns
            .bind(this);
        this.removeArtistDesign = this
            .removeArtistDesign
            .bind(this);
        this.state = {
            artistDesigns: null,
            open: false
        };
        ArtistStore.fetchArtistDesigns();

    }
    getArtistDesigns() {
        this.setState({
            artistDesigns: ArtistStore.getArtistDesign()
        })
    }

    handleOpen = () => {
        this.setState({open: true});
    };

    handleClose = () => {
        this.setState({open: false});
    };

    removeArtistDesignPopup(id) {
        this.setState({deleteID: id, open: true});
    }

    removeArtistDesign() {
        const id = this.state.deleteID;
        var self = this;
        var index = -1;
        var artistDesignTmp = this.state.artistDesigns;
        API.removeArtistDesign(id, function (data) {
            if (data.success) {
                for (var i in self.state.artistDesigns.designs) {
                    if (self.state.artistDesigns.designs[i].id == id) {
                        index = i;
                    }
                    if (index > -1) {
                        artistDesignTmp
                            .designs
                            .splice(index, 1)
                        self.setState({artistDesigns: artistDesignTmp})
                        UserActions.getArtistDesigns(artistDesignTmp)
                    }
                }
            } else {
                console.log('Error')
            }
        });
        console.log("XxX" + id);
        this.handleClose();
    }
    componentWillMount() {
        ArtistStore.on("change", this.getArtistDesigns);
        console.log('Component WILL MOUNT!')
    }
    render() {
        self = this;

        const deletePopup = function () {
            const actions = [ < FlatButton label = "No" primary = {
                    true
                }
                onClick = {
                    this.handleClose
                } />, < FlatButton label = "Yes" primary = {
                    true
                }
                onClick = {
                    self.removeArtistDesign
                } />
            ];
            return (
                <Dialog
                    title="Delete Design"
                    actions={actions}
                    modal={true}
                    open={this.state.open}
                    onRequestClose={this.handleClose}>
                    You want to Delete The Design ?
                </Dialog>
            )
        }.bind(this)();
        const artistDesigns = self.state.artistDesigns
        const DesignCard = (i) => (
            <Card >
                <CardMedia>
                    <img
                        className="artist-design-image"
                        src={artistDesigns.designs[i].image}
                        alt=""/>
                </CardMedia>
                <CardTitle
                    titleStyle={{
                    whiteSpace: 'nowrap',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis'
                }}
                    title={artistDesigns.designs[i].title}/>
                <CardText
                    style={{
                    overflow: 'hidden',
                    whiteSpace: 'nowrap',
                    textOverflow: 'ellipsis'
                }}>
                    {artistDesigns.designs[i].comment}
                </CardText>
                <CardActions
                    style={{
                    display: 'inline-block',
                    width: '100%',
                    padding: '18px 8px 1px 8px'
                }}>

                    {artistDesigns.designs[i].status == 'PENDING'
                        ? <div>
                                <div className="fr">
                                    <EditDesign
                                        imageUrl={artistDesigns.designs[i].image}
                                        title={artistDesigns.designs[i].title}
                                        comment={artistDesigns.designs[i].comment}
                                        tags={artistDesigns.designs[i].tags}
                                        designID={artistDesigns.designs[i].id}/>
                                </div>
                                <div className="fr">
                                    <Delete
                                        onClick={(e) => this.removeArtistDesignPopup(artistDesigns.designs[i].id)}/></div>
                            </div>
                        : null}
                    <label>{artistDesigns.designs[i].status}</label>
                </CardActions>
            </Card>
        );
        const l = artistDesigns != null
            ? artistDesigns.designs.length
            : 0
        var lis = [];
        const introText = <h2>No Design Yet !! Click on Upload Button and start the business wih us.</h2>
        for (var i = 0; i < l; i++) {
            lis.push(
                <div className="col-sm-4 col-xs-12 pad-10">
                    {DesignCard(i)}
                </div>
            );
        }
        return (
            <MuiThemeProvider muiTheme={lightMuiTheme}>
                <div>
                    {deletePopup}

                    <div className="row">
                        <Masonry>
                            {lis.length
                                ? lis
                                : introText}
                        </Masonry>
                    </div>
                </div>
            </MuiThemeProvider>
        )
    }
}
export default ArtistDesigns;