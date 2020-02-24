import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField';
import {orange500, blue500} from 'material-ui/styles/colors';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'
import API from '../../store/API.js';
import Divider from 'material-ui/Divider';
import ArtistStore from '../../store/ArtistStore.jsx';
import RefreshIndicator from 'material-ui/RefreshIndicator';
import Chip from 'material-ui/Chip';


const lightMuiTheme = getMuiTheme(lightBaseTheme);



class UploadDesign extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            file: '',
            imagePreviewUrl: '',
            title:'',
            comment:'',
            tags:'',
            loader_status:'hide',
            submitButtonStatus:true,
        };
    }
    
  handleSubmit(e) {
    self = this;
    e.preventDefault();
    // TODO: do something with -> this.state.file
    console.log('handle uploading-', this.state.file);
    this.setState({'loader_status':"loading"})
    this.setState({'submitButtonStatus':true})
     API.uploadArtistDesignForm(this.state.file,this.state.title,this.state.comment,this.state.tags,function(data){
                                if(data.success)
                                {
                                  console.log('AAA')
                                  ArtistStore.fetchArtistDesigns();
                                  self.props.req_close()
                                }
                                else{
                                  console.log('BBB')
                                }
                                self.setState({"loader_status":"hide"})
                                self.setState({'submitButtonStatus':false})
     });
  }

  _activateSubmitButton(){
    if(this.state.file != "" && this.state.title != ""
       && this.state.comment != "" ){
      this.setState({'submitButtonStatus':false})
    }
    else{
      this.setState({'submitButtonStatus':true})
    }
  }

  _handleTitleChange(e) {
    const title=e.target.value;
    this.setState({title},()=>{this._activateSubmitButton();});
  }

  _handleCommentChange(e) {
    const comment=e.target.value;
    this.setState({comment},()=>{this._activateSubmitButton();})
  }
  _handleTagChange(e) {
    const tags=e.target.value;
    this.setState({tags},()=>{this._activateSubmitButton();}) 
  }

  _handleImageChange(e) {
    e.preventDefault();

    let reader = new FileReader();
    let file = e.target.files[0];

    reader.onloadend = (upload) => {
      this.setState({
        file: file,
        imagePreviewUrl: reader.result
      },()=>{this._activateSubmitButton();});

    }
    reader.readAsDataURL(file);
  }
    render(){
    let {imagePreviewUrl} = this.state;
    let $imagePreview = null;
    if (imagePreviewUrl) {
      $imagePreview = (<img src={imagePreviewUrl} style={{width:'50%'}}/>);
    } else {
      $imagePreview = (<div className="previewText">Please select an Image for Preview</div>);
    }

    const chips = [];

    for (var i=0; i<this.state.tags.split(",").length;i++){
      if(this.state.tags.split(",")[i] != "")
        chips.push(
          <Chip
        >
        {this.state.tags.split(",")[i]}
        </Chip>
        );
    }

        return (
                <MuiThemeProvider muiTheme={lightMuiTheme}>
                  <div>
                    <div className="previewComponent">
                      <br/>
                      
                        <div className="row">
                          <div className='col-sm-4 pad-10'>
                            <input className="fileInput" 
                              type="file" 
                              onChange={(e)=>this._handleImageChange(e)} />
                            <br/>
                            <TextField
                              hintText="Title"
                              floatingLabelText="Enter Design Title"
                              onChange={(e)=>this._handleTitleChange(e)}
                            />
                            <br/>
                            <TextField
                              hintText="Description"
                              floatingLabelText="Description"
                              onChange={(e)=>this._handleCommentChange(e)}
                            />
                            <br/>
                            <TextField
                              floatingLabelText="Enter Tags Separated by Comma(,)"
                              floatingLabelStyle={{ color: orange500 }}
                              floatingLabelFocusStyle={{color: blue500,}}
                              onChange={(e)=>this._handleTagChange(e)}
                            />
                            <br/>
                            <RaisedButton label="Upload Image" primary={true}
                            onClick={(e)=>this.handleSubmit(e)}
                            disabled={this.state.submitButtonStatus}
                            />
                            <div style={{display: 'flex',flexWrap: 'wrap',}}>
                            {chips}
                            </div>
                            <RefreshIndicator
                              size={40}
                              left={50}
                              top={20}
                              status={this.state.loader_status}
                              style={{position: 'relative', }}
                            />
                          </div>
                          <div className="col-sm-8 pad-10">
                            {$imagePreview}
                          </div>
                        </div>
                    
                  </div>
                </div>
              </MuiThemeProvider>
        )
    }
}
export default UploadDesign;