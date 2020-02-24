import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'
import Avatar from 'material-ui/Avatar';
import Paper from 'material-ui/Paper';
import {List, ListItem} from 'material-ui/List';
import Divider from 'material-ui/Divider';
import Call from 'material-ui/svg-icons/communication/call';
import Email from 'material-ui/svg-icons/communication/email';
import Link from 'material-ui/svg-icons/content/link';
import UserIcon from 'material-ui/svg-icons/action/account-circle';
import userstore from '../../store/UserStore.jsx';

const lightMuiTheme = getMuiTheme(lightBaseTheme);



class ArtistDetails extends React.Component {
    constructor(props){
        super(props);
        this.getAartistDetails = this.getAartistDetails.bind(this);
        this.state = {
            artistDetails:null,
        };
        userstore.fetchArtistDetails();
    }  
    
    getAartistDetails(){
        this.setState({
            artistDetails: userstore.getArtistDetails()
        })
    }

    componentWillMount() {
        userstore.on("change", this.getAartistDetails);
      console.log('Component WILL MOUNT!')
   }

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
        const artistDetails = self.state.artistDetails
        const stylePaper = {
                        margin: 20,
                        display: 'inline-block',
                        };
        const style = {margin: 1};
        const styleList = {padding:'16px 16px 16px 50px'} 
        
        const paperBody = <div>
                            <div className="col-sm-6 col-xs-12 pad-10" >
                            <Avatar
                                src={artistDetails != null ? artistDetails.user_photo : "" }
                                size={150}
                                style={style}/>
                                </div>
                            <div className="col-sm-6 col-xs-12 ells" >
                            <List>
                                    <ListItem style={{ fontSize: '12px', textOverflow: 'ellipsis' }} leftIcon = {<UserIcon />} innerDivStyle={styleList} primaryText= {artistDetails != null ? artistDetails.first_name + " " + artistDetails.last_name : ""} />
                                    <ListItem style={{ fontSize: '12px', textOverflow: 'ellipsis' }} leftIcon={<Email />} innerDivStyle={styleList} primaryText= {artistDetails != null ? artistDetails.email  : ""} />
                                    <ListItem style={{ fontSize: '12px', textOverflow: 'ellipsis' }} leftIcon={<Call />} innerDivStyle={styleList} primaryText= {artistDetails != null ? artistDetails.mobile : ""} />
                                    <ListItem style={{ fontSize: '12px' }} leftIcon={<Link />} innerDivStyle={styleList}  >
-                                    <a target='__blank' href={artistDetails != null ? artistDetails.link  : ""}>Your Public Profile</a></ListItem>
                            </List>
                            </div>
                        </div>

        const body = <div >
                            <Paper style={stylePaper} zDepth={2} rounded={false} children={ paperBody }/>
                    </div>
        return (
            <MuiThemeProvider muiTheme={lightMuiTheme}>
                { body }
            </MuiThemeProvider>
        )
    }
}
export default ArtistDetails;