import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'
import Avatar from 'material-ui/Avatar';
import Paper from 'material-ui/Paper';
import {List, ListItem} from 'material-ui/List';
import Divider from 'material-ui/Divider';

import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import TextField from 'material-ui/TextField';

import API from '../../store/API.js';
import ArtistStore from '../../store/ArtistStore.jsx';

const lightMuiTheme = getMuiTheme(lightBaseTheme);



class ArtistSocialLinks extends React.Component {
    constructor(props){
        super(props);
        this.getAartistSocialLinks = this.getAartistSocialLinks.bind(this);
        this.state = {
            url:null,
            artistSocialLinks:null,
            open: false,
        };
        ArtistStore.fetchArtistSocialLinks();
    }  
    
    getAartistSocialLinks(){
        this.setState({
            artistSocialLinks: ArtistStore.getArtistSocialLinks()
        })
    }

    componentWillMount() {
        ArtistStore.on("change", this.getAartistSocialLinks);
      console.log('Component WILL MOUNT!')
   }

   handleOpen = () => {
    this.setState({open: true});
  };

  handleClose = () => {
    this.setState({open: false});
  };

  _handleUrlChange(e) {
    const url=e.target.value;
    this.setState({url})
  }

  handleSubmit = () => {
      self = this
    API.setArtistSocialLinks(this.state.url,function(data){
                                if(data.success)
                                {
                                  ArtistStore.fetchArtistSocialLinks();
                                  self.handleClose();
                                }
                                else{
                                  console.log('Error')
                                }
     });
  };

   componentDidMount() {
      console.log('Component DID MOUNT!')
   }

   componentWillReceiveProps(newProps) {    
      console.log('Component WILL RECIEVE PROPS!')
   }


   componentWillUpdate(nextProps, nextState) {
      console.log('Component WILL UPDATE!');
   }

   componentDidUpdate(prevProps, prevState) {
      console.log('Component DID UPDATE!')
   }

   componentWillUnmount() {
      console.log('Component WILL UNMOUNT!')
   }


    render(){
        self = this
        const artistSocialLinks = self.state.artistSocialLinks
        const stylePaper = {
                        margin: 20,
                        display: 'inline-block',
                        maxHeight: 200,
                        overflow: 'auto',
                        };
        const style = {margin: 1};
        const styleList = {width:'300px'} 
        const l = artistSocialLinks != null ? artistSocialLinks.social_links.length : 0
        var lis = [];
        for (var i=0;i<l;i++)
            {
                lis.push(
                  <div>
                    <a href={artistSocialLinks != null ? artistSocialLinks.social_links[i]: '' }>{artistSocialLinks != null ? artistSocialLinks.social_links[i]: '' }</a>
                    <Divider />
                  </div>
                );
            }
        if (l <=0 ){
           lis = [
            <div>
            <a href='https://www.facbook.com/profile/' target="_blank" >www.facbook.com</a>
            <Divider />
          </div>,
          <div>
            <a href='https://www.instagram.com/' target="_blank" >www.instagram.com</a>
            <Divider />
          </div>
           ] 
        }

        const actions = [
            <FlatButton
                label="Cancel"
                primary={true}
                onClick={this.handleClose}
            />,
            <FlatButton
                label="Submit"
                primary={true}
                keyboardFocused={true}
                onClick={this.handleSubmit}
            />,
            ];
        const addLink = <Dialog
                            title="Paste Your Social Link"
                            actions={actions}
                            modal={false}
                            open={this.state.open}
                            onRequestClose={this.handleClose}
                            >
                            <label>Go to your Social Site Profile Page like facebook, twitter. Copy Url and paste it here</label> <br />
                            <TextField
                                    floatingLabelText="Enter Link (URL)"
                                    floatingLabelFixed={true}
                                    onChange={(e)=>this._handleUrlChange(e)}
                                    />
                            </Dialog>

        const paperBody = <div >
                            <RaisedButton label="Submit Your Social Links" onClick={this.handleOpen} fullWidth={true} />
                            <List>
                                 {lis}  
                            </List>
                            {addLink}
                            </div>

        const body = <div >
                            { paperBody }
                    </div>
        return (
            <MuiThemeProvider muiTheme={lightMuiTheme}>
                { body }
            </MuiThemeProvider>
        )
    }
}
export default ArtistSocialLinks;