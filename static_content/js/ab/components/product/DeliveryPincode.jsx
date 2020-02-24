import React from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'
import RefreshIndicator from 'material-ui/RefreshIndicator';
import ProductStore from '../../store/ProductStore.jsx';

import API from '../../store/API.js';

const lightMuiTheme = getMuiTheme(lightBaseTheme);



class DeliveryPincode extends React.Component {
    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
        this.handlePincodeChange = this.handlePincodeChange.bind(this);
        this.getPincodeDetails = this.getPincodeDetails.bind(this);
        if (window.getCookie("pincode")) {
            ProductStore.fetchPincode(window.getCookie("pincode"))
            this.loader = 'loading';
        }
        else {
            this.loader = 'hide'
        }
        this.state = {
            callback: this.props.callback,
            pincodeDetails: null,
            pincode: window.getCookie("pincode"),
            loader_status: 'hide',
            error_message: false,
        }
    }
    getPincodeDetails() {
        this.setState({
            pincodeDetails: ProductStore.getPincodeDetails()
        })
        this.setState({ 'loader_status': "hide" })
    }

    componentWillMount() {
        ProductStore.on("change", this.getPincodeDetails);
        console.log('Component WILL MOUNT!')
    }

    handlePincodeChange(e) {
        const pincode = e.target.value;
        this.setState({ pincode: pincode, error_message: false})
    }
    handleClick() {
        self = this;
        const pincode = this.state.pincode;
        if (pincode.length === 6) {
            setCookie("pincode", pincode, 10);
            this.setState({ 'loader_status': "loading" })
            ProductStore.fetchPincode(pincode)
        }
        else{
            this.setState({error_message: "Enter 6 digit pincode", pincodeDetails: null})
        }
    }

    render() {
        const pincodeDetails = this.state.pincodeDetails;
        const yesTick = <img src="/static/img/resource/yes.png" style={{ width: 15 }} alt="Yes Correct Tick" />
        const noCross = <img src="/static/img/resource/no.png" style={{ width: 15, paddingTop: 3 }} alt="No Cross Tick" />

        const body = <div className="col-sm-12 col-md-12">
            <div className="col-sm-5 col-md-5">
                <input style={{ borderStyle: 'solid',
                                borderRadius: 3,
                                borderWidth: 1,
                                paddingLeft: 10,}} 
                    className="delivery-input" ref="input"
                    placeholder={this.state.pincode != "" ? this.state.pincode : "Enter Pincode"}
                    onChange={(e) => this.handlePincodeChange(e)}
                />
                <button className="delivery-btn" onClick={this.handleClick}>CHECK</button>
                <label className='err'>{this.state.error_message}</label>
                <center>
                    <RefreshIndicator
                        size={30}
                        left={0}
                        top={10}
                        status={this.state.loader_status}
                        style={{ position: 'relative', }}
                    />
                </center>
            </div>
            <div className="col-sm-6 col-md-6">
                <ul className={this.props.isMobile ? "delivery-check" : "delivery-check left-bar"}>
                    {pincodeDetails != null ? pincodeDetails.online ? <li>Online Payment- Free Delivery &nbsp;{yesTick} </li> : null : null}
                    {pincodeDetails != null ? pincodeDetails.cod ? <li>COD Available: Charges- &#8377; 65 &nbsp; {yesTick} </li> : <li>COD not available &nbsp; {noCross}</li> : null}
                    {pincodeDetails != null ? pincodeDetails.cod || pincodeDetails.online ? <li>Expected Delivery Time 7 Days &nbsp;{yesTick}</li> : <li>Sorry Currently we dont have delivery service at this pincode&nbsp;{noCross}</li> : null}
                </ul>
                <br />
            </div>
        </div>
        return (
            <MuiThemeProvider muiTheme={lightMuiTheme}>
                <div>
                    {body}
                </div>
            </MuiThemeProvider>
        )
    }
}
export default DeliveryPincode;