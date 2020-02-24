import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'
import TextField from 'material-ui/TextField';
import { orange500, blue500 } from 'material-ui/styles/colors';
import Paper from 'material-ui/Paper';
import Divider from 'material-ui/Divider';
import DatePicker from 'material-ui/DatePicker';
import { RadioButton, RadioButtonGroup } from 'material-ui/RadioButton';
import Avatar from 'material-ui/Avatar';
import AppBar from 'material-ui/AppBar';
import RefreshIndicator from 'material-ui/RefreshIndicator';
import Edit from 'material-ui/svg-icons/editor/mode-edit';
import Done from 'material-ui/svg-icons/action/done';
import userstore from '../../store/UserStore.jsx';
import ArtistStore from '../../store/ArtistStore.jsx';
import API from '../../store/API.js';
import AvatarCrop from './AvatarCrop.jsx'
import VerifyOTP from './VerifyOTP.jsx'

import TextFieldIcon from 'material-ui-textfield-icon';


const lightMuiTheme = getMuiTheme(lightBaseTheme);



class EditProfile extends React.Component {
    constructor(props) {
        super(props);
        this.getUserDetails = this.getUserDetails.bind(this);
        this.getArtistOtherDetails = this.getArtistOtherDetails.bind(this);
        this.getArtistBankDetails = this.getArtistBankDetails.bind(this);
        this.handleUserDetailBtn = this.handleUserDetailBtn.bind(this);
        this.handleArtistDetailBtn = this.handleArtistDetailBtn.bind(this);
        this.handleArtistBankDetailBtn = this.handleArtistBankDetailBtn.bind(this);
        this.unlockUserDetailsActives = this.unlockUserDetailsActives.bind(this);
        this.lockUserDetailsActives = this.lockUserDetailsActives.bind(this);
        this.unlockArtistDetailsActives = this.unlockArtistDetailsActives.bind(this);
        this.lockArtistDetailsActives = this.lockArtistDetailsActives.bind(this);
        this.unlockArtistBankDetailsActives = this.unlockArtistBankDetailsActives.bind(this);
        this.lockArtistDetailsActives = this.lockArtistDetailsActives.bind(this);
        this.getEmailSentStaus = this.getEmailSentStaus.bind(this);
        this.getMobileVerifyStaus = this.getMobileVerifyStaus.bind(this);
        this.state = {
            user_details: null,
            artist_detail: { 'success': false },
            artist_bank_detail: { 'success': false },
            user_details_active: true,
            artist_detail_active: true,
            artist_bank_detail_active: true,
            hide_user_details: { display: 'none' },
            hide_artist_details: { display: 'none' },
            hide_artist_bank_details: { display: 'none' },
            btn_txt_user_details: 'EDIT',
            btn_txt_artist_details: 'EDIT',
            loader_status: 'hide',
            openDialog: false,
            openDialogFor: null,
            emailSentStaus: false,
        };
        userstore.fetchArtistDetails();
        ArtistStore.fetchArtistOtherDetails();
        ArtistStore.fetchArtistBankDetails();

    }

    getUserDetails() {
        this.setState({
            user_details: userstore.getArtistDetails()
        })
    }

    getArtistOtherDetails() {
        this.setState({
            artist_detail: ArtistStore.getArtistOtherDetails()
        })
    }
    getArtistBankDetails() {
        this.setState({
            artist_bank_detail: ArtistStore.getArtistBankDetails()
        })
    }
    getEmailSentStaus() {
        this.setState({
            emailSentStaus: userstore.get_email_sent_status()
        })
    }
    getMobileVerifyStaus() {
        let temp = this.state.user_details;
        if (temp !== null) {
            temp.is_mobile_verified = (temp ? temp.is_mobile_verified : false) || userstore.isUserAuthenticatedAndMobileVerified();
            this.setState({ user_details: temp });
        }
    }

    componentWillMount() {
        userstore.on("change", this.getUserDetails);
        userstore.on("change", this.getEmailSentStaus);
        userstore.on("change", this.getMobileVerifyStaus);
        ArtistStore.on("change", this.getArtistOtherDetails);
        ArtistStore.on("change", this.getArtistBankDetails);
        console.log('Component WILL MOUNT!')
    }

    handleUserDetailChange(e) {
        const user_details = this.state.user_details
        const key = e.target.name;
        const val = e.target.value;
        user_details[key] = val;
        console.log(key + '-' + val)
        this.setState({ "user_details": user_details })
    }

    handleEmailVerifyChange(e) {
        this.setState({ openDialog: true });
        this.setState({ openDialogFor: 'email' });
    }

    handleMobileVerifyChange(e) {
        this.setState({ openDialog: true });
        this.setState({ openDialogFor: 'mobile' });
    }

    handleCloseDialog = () => {
        this.setState({ openDialog: false });
    };
    handleSendDialog = () => {
        if (this.state.openDialogFor === 'email' && !this.state.emailSentStaus) {
            API.sendEmailLink();
        }
        else if (this.state.openDialogFor === 'mobile') {
            alert("Ha ha mob");
        }
        this.handleCloseDialog();
    };

    handleUserDetailDateChange(e, date) {
        const user_details = this.state.user_details
        const key = 'dob';
        const val = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate()
        user_details[key] = val;
        console.log(key + '-' + val)
        this.setState({ "user_details": user_details })
        console.log(date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate())
    }

    handleArtistDetailChange(e) {
        const artist_detail = this.state.artist_detail
        const key = e.target.name;
        const val = e.target.value;
        artist_detail[key] = val;
        console.log(key + '-' + val)
        this.setState({ "artist_detail": artist_detail })
    }

    handleArtistBankDetailChange(e) {
        const artist_bank_detail = this.state.artist_bank_detail
        const key = e.target.name;
        const val = e.target.value;
        artist_bank_detail[key] = val;
        artist_bank_detail['success'] = true;
        console.log(key + '-' + val)
        this.setState({ "artist_bank_detail": artist_bank_detail })
    }


    unlockUserDetailsActives() {
        if (this.state.btn_txt_user_details === "EDIT") {
            this.setState({ "user_details_active": false })
            this.setState({ "hide_user_details": { visible: 'visible' } })
            this.setState({ "btn_txt_user_details": "DISCARD" })
        }
        else {
            userstore.fetchArtistDetails();
            this.lockUserDetailsActives();
        }
    }

    lockUserDetailsActives() {
        this.setState({ "user_details_active": true })
        this.setState({ "hide_user_details": { display: 'none' } })
        this.setState({ "btn_txt_user_details": "EDIT" })
    }

    unlockArtistDetailsActives() {
        if (this.state.btn_txt_artist_details === "EDIT") {
            this.setState({ "artist_detail_active": false })
            this.setState({ "hide_artist_details": { visible: 'visible' } })
            this.setState({ "btn_txt_artist_details": "DISCARD" })
        }
        else {
            ArtistStore.fetchArtistOtherDetails();
            this.lockArtistDetailsActives();
        }
    }

    lockArtistDetailsActives() {
        this.setState({ "artist_detail_active": true })
        this.setState({ "hide_artist_details": { display: 'none' } })
        this.setState({ "btn_txt_artist_details": "EDIT" })
    }

    unlockArtistBankDetailsActives() {
        if (!this.state.artist_bank_detail.success) {
            this.setState({ "artist_bank_detail_active": false })
            this.setState({ "hide_artist_bank_details": { visible: 'visible' } })
        }
    }

    lockArtistBankDetailsActives() {
        this.setState({ "artist_bank_detail_active": true })
        this.setState({ "hide_artist_bank_details": { display: 'none' } })
    }


    handelIfsc(e) {
        self = this
        this.setState({ 'loader_status': "loading" })
        const key = e.target.name;
        const val = e.target.value;
        console.log('Length ' + val.length)
        if (val.length === 11) {
            API.fetchIfscDetails(val, function (data) {
                if (data.success) {
                    const artist_bank_detail = self.state.artist_bank_detail
                    artist_bank_detail.branch_name = data.BRANCH
                    artist_bank_detail.bank_name = data.BANK
                    artist_bank_detail.bank_branch_address = data.ADDRESS
                    self.setState({ "artist_bank_detail": artist_bank_detail })
                }
                self.setState({ "loader_status": "hide" })
            });
        }
    }

    handleUserDetailBtn() {
        self = this
        API.setUserDetails(this.state.user_details.first_name,
            this.state.user_details.last_name,
            this.state.user_details.gender,
            this.state.user_details.dob,
            function (data) {
                if (data.success) {
                    console.log('data Saved...')
                    self.lockUserDetailsActives();
                    userstore.fetchArtistDetails();
                }
            });



    }

    handleArtistDetailBtn() {
        self = this
        API.setArtistDetails(this.state.artist_detail.about,
            this.state.artist_detail.address,
            this.state.artist_detail.pin_code,
            this.state.artist_detail.city,
            this.state.artist_detail.state,
            this.state.artist_detail.artist_type,
            function (data) {
                if (data.success) {
                    console.log('data Saved...Artist')
                    self.lockArtistDetailsActives();
                    ArtistStore.fetchArtistOtherDetails();
                }
            });
    }

    handleArtistBankDetailBtn() {
        self = this
        API.setArtistBankDetails(this.state.artist_bank_detail.account_holder_name,
            this.state.artist_bank_detail.ifsc_code,
            this.state.artist_bank_detail.account_no,
            this.state.artist_bank_detail.pan,
            this.state.artist_bank_detail.bank_name,
            this.state.artist_bank_detail.branch_name,
            this.state.artist_bank_detail.bank_branch_address,
            this.state.artist_bank_detail.account_type,
            function (data) {
                if (data.success) {
                    console.log('data Saved...Artist....Bank')
                    self.lockArtistBankDetailsActives();
                    ArtistStore.fetchArtistBankDetails();
                }
            });
    }

    copyLink(e) {
        var $temp = $("<input>");
        $("body").append($temp);
        $temp.val(e.target.innerText).select();
        document.execCommand("copy");
        $temp.remove();
        alert('Link Copied...')
    }
    render() {
        const user_details = this.state.user_details
        const artist_detail = this.state.artist_detail
        const artist_bank_detail = this.state.artist_bank_detail

        const style_paper = {
            //width: '90vw',
            textAlign: 'center',
            display: 'inline-block',
            zDepth: 1,
            width: '100%',
        };

        const actionsDialog = [
            <FlatButton
                label="Cancel"
                primary={true}
                onClick={this.handleCloseDialog}
            />,
        ];

        if (this.state.openDialogFor === 'mobile'
            && this.state.user_details.is_mobile_verified === true
            && this.state.openDialog == true) {
            this.setState({ openDialog: false });
        }
        const dialogBody = function () {
            if (this.state.openDialogFor === 'email') {
                if (this.state.emailSentStaus) {
                    return (<div>
                        Email is Already Sent to {user_details != null ? user_details.email : ""}
                    </div>)
                }
                return (
                    <div>
                        Send a varification Email to {user_details != null ? user_details.email : ""}
                        <br />
                        <RaisedButton
                            label="Send"
                            onClick={this.handleSendDialog}
                        />
                    </div>
                )
            }
            else if (this.state.openDialogFor === 'mobile') {
                return (
                    <div>
                        Send a verification message to {user_details != null ? user_details.mobile : ""}
                        <VerifyOTP mobile={user_details != null ? user_details.mobile : ""} enable={true} />
                    </div>
                )
            }
            else {
                return (<div></div>)
            }
        }.bind(this)();

        const customer_details = function () {
            if (user_details != null) {
                return (
                    <div>
                        <AppBar
                            title="Profile Details"
                            showMenuIconButton={false}
                            style={{ backgroundColor: 'rgb(255, 255, 255)' }}
                            titleStyle={{ fontSize: '20px', color: '#000000' }}
                        />
                        <div className="container-full">
                            <div className="row">
                                <div className="col-md-3 col-sm-12">
                                    <div>
                                        <br />
                                        <br />
                                        <h5>Share link and get Rs. 50 on each user signup</h5>
                                        <div className="social-btns t-center">
                                            <a className="btn facebook" target="_blank" href={'https://www.facebook.com/sharer/sharer.php?u=' + user_details.share_link}><i className="fa fa-facebook"></i></a>
                                            <a className="btn whatsapp" target="_blank" href={'whatsapp://send?text=' + user_details.share_link}><i className="fa fa-whatsapp"></i></a>
                                        </div>
                                        <h5>--or--</h5>
                                        <h5>Copy below link to share</h5>
                                        <a className="btn " onClick={(e) => this.copyLink(e)} ><i className="fa">{user_details.share_link}</i></a>
                                        <input type="hidden" value={user_details.share_link} id="shanreLink" />
                                    </div>
                                    <div>
                                        <h5>Your CODE</h5>
                                        <i className="fa">{user_details.code}</i>
                                    </div>
                                </div>
                                <div className='col-md-3 col-sm-12'>
                                    <br />
                                    {user_details != null ? <AvatarCrop img={user_details.user_photo} /> : null}
                                </div>
                                <div className="col-md-6 col-sm-12">
                                    <div className='l-top'>
                                        <Edit onClick={this.unlockUserDetailsActives} />
                                    </div>
                                    <TextField
                                        floatingLabelText="FirstName"
                                        name="first_name"
                                        value={user_details != null ? user_details.first_name : ""}
                                        onChange={(e) => this.handleUserDetailChange(e)}
                                        underlineFocusStyle={{ borderColor: orange500 }}
                                        disabled={this.state.user_details_active}
                                    /> <br />
                                    <TextField
                                        floatingLabelText="LastName"
                                        name="last_name"
                                        value={user_details != null ? user_details.last_name : ""}
                                        onChange={(e) => this.handleUserDetailChange(e)}
                                        underlineFocusStyle={{ borderColor: orange500 }}
                                        disabled={this.state.user_details_active}
                                    />
                                    <br />
                                    <a
                                        onClick={user_details != null ? user_details.is_email_verified ? "" : (e) => this.handleEmailVerifyChange(e) : ""}
                                    >
                                        <TextFieldIcon
                                            floatingLabelText="E-mail"
                                            name="email"
                                            value={user_details != null ? user_details.email : ""}
                                            errorText={user_details != null ? user_details.is_email_verified ? "" : (this.state.emailSentStaus ? "Email Sent Check Your Inbox" : "Email not verified Click to verify") : ""}
                                            onChange={(e) => this.handleUserDetailChange(e)}
                                            disabled={true}
                                            underlineFocusStyle={{ borderColor: orange500 }}
                                            icon={user_details != null ? user_details.is_email_verified ? <Done /> : <Edit /> : ""}
                                            fullWidth={false}
                                        />
                                    </a>
                                    <br />
                                    <a
                                        onClick={user_details != null ? user_details.is_mobile_verified ? "" : (e) => this.handleMobileVerifyChange(e) : ""}
                                    >
                                        <TextFieldIcon
                                            floatingLabelText="Mobile"
                                            name="mobile"
                                            value={user_details != null ? user_details.mobile : ""}
                                            errorText={user_details != null ? user_details.is_mobile_verified ? "" : "Mobile not verified Click to verify" : ""}
                                            onChange={(e) => this.handleUserDetailChange(e)}
                                            disabled={true}
                                            underlineFocusStyle={{ borderColor: orange500 }}
                                            icon={user_details != null ? user_details.is_mobile_verified ? <Done /> : <Edit /> : ""}
                                            fullWidth={false}
                                        />
                                    </a>
                                    <br />
                                    <DatePicker
                                        floatingLabelText="Date of Birth"
                                        name="dob"
                                        value={new Date(user_details != null ? user_details.dob : null)}
                                        onChange={(e, date) => this.handleUserDetailDateChange(e, date)}
                                        maxDate={new Date()}
                                        okLabel="Set DoB"
                                        disabled={this.state.user_details_active}
                                        defaultDate={null}
                                    />
                                    <br />
                                    <RadioButtonGroup
                                        name="gender"
                                        valueSelected={user_details != null ? user_details.gender : "MALE"}
                                        name="gender"
                                        onChange={(e) => this.handleUserDetailChange(e)}
                                        disabled={this.state.user_details_active}
                                    >
                                        <RadioButton
                                            value="MALE"
                                            label="Male"
                                            style={{ display: 'inline-block', width: '90px' }}
                                            disabled={this.state.user_details_active}
                                        />
                                        <RadioButton
                                            value="FEMALE"
                                            label="Female"
                                            style={{ display: 'inline-block', width: '90px' }}
                                            disabled={this.state.user_details_active}
                                        />
                                        <RadioButton
                                            value="OTHER"
                                            label="Other"
                                            style={{ display: 'inline-block', width: '90px' }}
                                            disabled={this.state.user_details_active}
                                        />
                                    </RadioButtonGroup>
                                    <br />
                                    <div className="pad-10">
                                        <RaisedButton
                                            label={this.state.btn_txt_user_details}
                                            onClick={this.unlockUserDetailsActives}
                                        />
                                        <RaisedButton
                                            label="Save"
                                            primary={true}
                                            onClick={this.handleUserDetailBtn}
                                            disabled={this.state.user_details_active}
                                            style={this.state.hide_user_details}
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                )
            }
            else {
                return null
            }
        }.bind(this)();

        const artist_details = <div>
            <AppBar
                title="Other Details"
                showMenuIconButton={false}
                style={{ backgroundColor: 'rgb(255, 255, 255)' }}
                titleStyle={{ fontSize: '20px', color: '#000000' }}
            />
            <TextField
                floatingLabelText="About"
                name="about"
                value={artist_detail.success ? artist_detail.about : ""}
                multiLine={true}
                rowsMax={5}
                onChange={(e) => this.handleArtistDetailChange(e)}
                underlineFocusStyle={{ borderColor: orange500 }}
                style={{ textAlign: 'left' }}
                disabled={this.state.artist_detail_active}
            /> <br />
            <TextField
                floatingLabelText="Address"
                name="address"
                value={artist_detail.success ? artist_detail.address : ""}
                multiLine={true}
                rowsMax={3}
                maxLength="200"
                onChange={(e) => this.handleArtistDetailChange(e)}
                underlineFocusStyle={{ borderColor: orange500 }}
                style={{ textAlign: 'left' }}
                disabled={this.state.artist_detail_active}
            />
            <br />
            <TextField
                floatingLabelText="Pincode"
                name="pin_code"
                value={artist_detail.success ? artist_detail.pin_code : ""}
                onChange={(e) => this.handleArtistDetailChange(e)}
                underlineFocusStyle={{ borderColor: orange500 }}
                disabled={this.state.artist_detail_active}
            />
            <br />
            <TextField
                floatingLabelText="City"
                name="city"
                value={artist_detail.success ? artist_detail.city : ""}
                maxLength="60"
                onChange={(e) => this.handleArtistDetailChange(e)}
                underlineFocusStyle={{ borderColor: orange500 }}
                disabled={this.state.artist_detail_active}
            />
            <br />
            <TextField
                floatingLabelText="State"
                name="state"
                value={artist_detail.success ? artist_detail.state : ""}
                maxLength="60"
                onChange={(e) => this.handleArtistDetailChange(e)}
                underlineFocusStyle={{ borderColor: orange500 }}
                disabled={this.state.artist_detail_active}
            />
            <br />
            <RadioButtonGroup
                name="artist_type"
                onChange={(e) => this.handleArtistDetailChange(e)}
                valueSelected={artist_detail.success ? artist_detail.artist_type : ""}
                disabled={this.state.artist_detail_active}
            >
                <RadioButton
                    value="INDEPENDENT"
                    label="Independent"
                    style={{ display: 'inline-block', width: '130px' }}
                    disabled={this.state.artist_detail_active}
                />
                <RadioButton
                    value="YOUTUBER"
                    label="Youtuber"
                    style={{ display: 'inline-block', width: '100px' }}
                    disabled={this.state.artist_detail_active}
                />
                <RadioButton
                    value="BLOGGER"
                    label="Blogger"
                    style={{ display: 'inline-block', width: '100px' }}
                    disabled={this.state.artist_detail_active}
                />
                <RadioButton
                    value="NGO"
                    label="NGO"
                    style={{ display: 'inline-block', width: '80px' }}
                    disabled={this.state.artist_detail_active}
                />
                <RadioButton
                    value="OTHER"
                    label="Other"
                    style={{ display: 'inline-block', width: '100px' }}
                    disabled={this.state.artist_detail_active}
                />
            </RadioButtonGroup>
            <br />
            <RaisedButton
                label={this.state.btn_txt_artist_details}
                onClick={this.unlockArtistDetailsActives}
            />
            <RaisedButton
                label="Save"
                primary={true}
                onClick={this.handleArtistDetailBtn}
                disabled={this.state.artist_detail_active}
                style={this.state.hide_artist_details}
            />
        </div>
        const artist_bank_details = <div>
            <AppBar
                title="Bank Details"
                showMenuIconButton={false}
                style={{ backgroundColor: 'rgb(255, 255, 255)' }}
                titleStyle={{ fontSize: '20px', color: '#000000' }}
            />
            <center>
                <RefreshIndicator
                    size={40}
                    left={0}
                    top={300}
                    status={this.state.loader_status}
                    style={{ position: 'relative', }}
                />
            </center>
            <TextField
                floatingLabelText="Account Holder Name"
                name="account_holder_name"
                value={artist_bank_detail.success ? artist_bank_detail.account_holder_name : ""}
                maxLength="60"
                onChange={(e) => this.handleArtistBankDetailChange(e)}
                underlineFocusStyle={{ borderColor: orange500 }}
                style={{ textAlign: 'left' }}
                disabled={this.state.artist_bank_detail_active}
            /> <br />
            <TextField
                floatingLabelText="IFSC Code"
                name="ifsc_code"
                value={artist_bank_detail.success ? artist_bank_detail.ifsc_code : ""}
                maxLength="11"
                onChange={(e) => this.handleArtistBankDetailChange(e)}
                onBlur={(e) => this.handelIfsc(e)}
                underlineFocusStyle={{ borderColor: orange500 }}
                style={{ textAlign: 'left' }}
                disabled={this.state.artist_bank_detail_active}
            />

            <br />
            <TextField
                floatingLabelText="Account No."
                name="account_no"
                value={artist_bank_detail.success ? artist_bank_detail.account_no : ""}
                maxLength="30"
                onChange={(e) => this.handleArtistBankDetailChange(e)}
                underlineFocusStyle={{ borderColor: orange500 }}
                style={{ textAlign: 'left' }}
                disabled={this.state.artist_bank_detail_active}
            />
            <br />
            <TextField
                floatingLabelText="Bank Name"
                name="bank_name"
                value={artist_bank_detail.success ? artist_bank_detail.bank_name : ""}
                maxLength="100"
                onChange={(e) => this.handleArtistBankDetailChange(e)}
                underlineFocusStyle={{ borderColor: orange500 }}
                disabled={this.state.artist_bank_detail_active}
            />
            <br />
            <TextField
                floatingLabelText="Branch Name"
                name="branch_name"
                value={artist_bank_detail.success ? artist_bank_detail.branch_name : ""}
                maxLength="60"
                onChange={(e) => this.handleArtistBankDetailChange(e)}
                underlineFocusStyle={{ borderColor: orange500 }}
                disabled={this.state.artist_bank_detail_active}
            />
            <br />
            <TextField
                floatingLabelText="Branch Address"
                name="bank_branch_address"
                value={artist_bank_detail.success ? artist_bank_detail.bank_branch_address : ""}
                maxLength="200"
                multiLine={true}
                rowsMax={3}
                style={{ textAlign: 'left' }}
                onChange={(e) => this.handleArtistBankDetailChange(e)}
                underlineFocusStyle={{ borderColor: orange500 }}
                disabled={this.state.artist_bank_detail_active}
            />
            <br />
            <TextField
                floatingLabelText="PAN No."
                name="pan"
                value={artist_bank_detail.success ? artist_bank_detail.pan : ""}
                maxLength="15"
                onChange={(e) => this.handleArtistBankDetailChange(e)}
                underlineFocusStyle={{ borderColor: orange500 }}
                style={{ textAlign: 'left' }}
                disabled={this.state.artist_bank_detail_active}
            />
            <br />
            <RadioButtonGroup
                name="account_type"
                onChange={(e) => this.handleArtistBankDetailChange(e)}
                valueSelected={artist_bank_detail.success ? artist_bank_detail.account_type : "SAVING"}
                disabled={this.state.artist_bank_detail_active}
            >
                <RadioButton
                    value="SAVING"
                    label="Saving Account"
                    style={{ display: 'inline-block', width: '200px' }}
                    disabled={this.state.artist_bank_detail_active}
                />
                <RadioButton
                    value="CURRENT"
                    label="Current Account"
                    style={{ display: 'inline-block', width: '200px' }}
                    disabled={this.state.artist_bank_detail_active}
                />
            </RadioButtonGroup>
            <br />

            <RaisedButton
                label="Edit"
                onClick={this.unlockArtistBankDetailsActives}
            />
            <RaisedButton
                label="Save"
                primary={true}
                onClick={this.handleArtistBankDetailBtn}
                disabled={this.state.artist_bank_detail_active}
                style={this.state.hide_artist_bank_details}
            />
            <br />
        </div>


        const artistDetailComponent = artist_detail.success ? <Paper style={style_paper} children={artist_details} /> : null;
        const artistBankdetailComponent = artist_detail.success ? <Paper style={style_paper} children={artist_bank_details} /> : null;

        return (
            <MuiThemeProvider muiTheme={lightMuiTheme}>

                <div className="row">
                    <div className="col-sm-12">
                        <Paper style={style_paper} children={customer_details} />
                        <Dialog
                            title="   "
                            actions={actionsDialog}
                            modal={false}
                            open={this.state.openDialog}
                            onRequestClose={this.handleCloseDialog}
                        >
                            {dialogBody}
                        </Dialog>
                    </div>
                    <div className="col-sm-6">
                        {artistBankdetailComponent}
                    </div>
                    <div className="col-sm-6">{artistDetailComponent}</div>
                </div>

            </MuiThemeProvider>
        )
    }
}
export default EditProfile;