import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import UploadDesign from './UploadDesign.jsx';
import TextField from 'material-ui/TextField';
import {orange500, blue500} from 'material-ui/styles/colors';
import RefreshIndicator from 'material-ui/RefreshIndicator';
import API from '../../store/API.js';
import ArtistStore from '../../store/ArtistStore.jsx';
import Edit from 'material-ui/svg-icons/editor/mode-edit';


/**
 * Dialog with action buttons. The actions are passed in as an array of React objects,
 * in this example [FlatButtons](/#/components/flat-button).
 *
 * You can also close this dialog by clicking outside the dialog, or with the 'Esc' key.
 */
export default class EditDesign extends React.Component {
  constructor(props){
    super(props);
    this.handleClose = this.handleClose.bind(this);
    this.state = {
      open: false,
      imagePreviewUrl: this.props.imageUrl,
      file: '',
      designID:this.props.designID,
      title:this.props.title,
      comment:this.props.comment,
      tags:this.props.tags,
      loader_status:'hide',
      submitButtonStatus:true,
    };
  }

  handleOpen = () => {
    this.setState({
      open: true,
      imagePreviewUrl: this.props.imageUrl,
      file: '',
      designID:this.props.designID,
      title:this.props.title,
      comment:this.props.comment,
      tags:this.props.tags,
      loader_status:'hide',
      submitButtonStatus:true,
    });
  };

  handleClose = () => {
    this.setState({open: false});
  };

  handleSubmit(e) {
    self = this;
    e.preventDefault();
    // TODO: do something with -> this.state.file
    console.log('handle uploading-', this.state.file);
    this.setState({'loader_status':"loading"})
    this.setState({'submitButtonStatus':true})
    API.editArtistDesignForm(this.state.designID,this.state.file,this.state.title,this.state.comment,this.state.tags,function(data){
        if(data.success)
        {
          location.reload();
          //ArtistStore.fetchArtistDesigns();
          self.handleClose()
        }
        else{
          console.log('BBB')
        }
        self.setState({"loader_status":"hide"})
        self.setState({'submitButtonStatus':false})
     });
  }

  _activateSubmitButton(){
    if( this.state.title != ""){
      this.setState({'submitButtonStatus':false})
    }
    else{
      this.setState({'submitButtonStatus':true})
    }
  }

  _handleTitleChange(e) {
    const title=e.target.value;
    this.setState({title},() => {this._activateSubmitButton();});
  }

  _handleCommentChange(e) {
    const comment=e.target.value;
    this.setState({comment},() => {this._activateSubmitButton();})
  }
  _handleTagChange(e) {
    const tags=e.target.value;
    this.setState({tags},() => {this._activateSubmitButton();})
  }

  _handleImageChange(e) {
    e.preventDefault();

    let reader = new FileReader();
    let file = e.target.files[0];
    reader.onloadend = (upload) => {
      this.setState({
        file: file,
        imagePreviewUrl: reader.result
      },() => {this._activateSubmitButton();});

    }
    reader.readAsDataURL(file)
    this._activateSubmitButton();
  }

  render() {
    console.log(this.state.title)
    const actions = [
      <FlatButton
        label="Cancel"
        primary={true}
        onClick={this.handleClose}
      />,
    ];

    let {imagePreviewUrl} = this.state;
    let $imagePreview = null;
    if (imagePreviewUrl) {
      $imagePreview = (<img src={imagePreviewUrl} style={{width:'100%'}}/>);
    } else {
      $imagePreview = (<div className="previewText">Please select an Image for Preview</div>);
    }

    const body =  <div>
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
                    defaultValue = {this.state.title}
                    onChange={(e)=>this._handleTitleChange(e)}
                    />
                    <br/>
                    <TextField
                    hintText="Description"
                    floatingLabelText="Description"
                    defaultValue = {this.state.comment}
                    onChange={(e)=>this._handleCommentChange(e)}
                    />
                    <br/>
                    <TextField
                    floatingLabelText="Enter Tags separated by comma (,)"
                    defaultValue = {this.state.tags}
                    floatingLabelStyle={{ color: orange500 }}
                    floatingLabelFocusStyle={{color: blue500,}}
                    onChange={(e)=>this._handleTagChange(e)}
                    />
                    <br/>
                    <RaisedButton label="Upload Image" primary={true}
                    onClick={(e)=>this.handleSubmit(e)}
                    disabled={this.state.submitButtonStatus}
                    />
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

    return ( 
      <div>
        <Edit  onClick={this.handleOpen}/>
        <Dialog
          title="Upload Your design"
          actions={actions}
          modal={false}
          open={this.state.open}
          onRequestClose={this.handleClose}
          autoScrollBodyContent={true}
          contentStyle={{maxWidth: "none",height:"100%",maxHeight:"100%"}}
        >
         {body} 
        </Dialog>
      </div>
    );
  }
}