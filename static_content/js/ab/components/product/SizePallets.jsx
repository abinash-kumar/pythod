import React from 'react';
// import RaisedButton from 'material-ui/RaisedButton';
// import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
// import getMuiTheme from 'material-ui/styles/getMuiTheme'
// import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'


class SizePallets extends React.Component {
    constructor(props) {
        super(props);
        this.handleSelectedValue = this.handleSelectedValue.bind(this);
        this.multiselect = this.props.multiSelect;
        if (!this.props.callbackFunction) {
            throw new Error("callbackFunction(Function) Prop is mandetory");
        }
        this.callbackFunction = this.props.callbackFunction;
        this.sizeMap = {
            'XXS': 'EXTRA EXTRA SMALL',
            'XS': 'EXTRA SMALL',
            'S': 'SMALL',
            'M': 'MEDIUM',
            'L': 'LARGE',
            'XL': 'EXTRA LARGE',
            'XXL': 'EXTRA EXTRA LARGE',
            '3XL': 'PLUS SIZE',
            '4XL': 'PLUS SIZE',
            '5XL': 'PLUS SIZE',
        }
        this.state = {
            selectedValues: props.selectedValues ? props.selectedValues : [],
        }
    }
    handleSelectedValue(e) {
        let val = e.target.getAttribute('value');
        let selectedValues = this.state.selectedValues;
        if (this.multiselect) {
            var index = selectedValues.indexOf(val);
            if (index !== -1) {
                selectedValues.splice(index, 1);
            }
            else {
                selectedValues.push(val);
            }
        }
        else {
            selectedValues = [val];
        }
        this.setState({ selectedValues });
        this.callbackFunction({ type: 'SIZE', values: selectedValues });
    }
    componentWillReceiveProps(nextProps) {
        if (nextProps.selectedValues) {
            this.setState({ selectedValues: nextProps.selectedValues });
        }
    }
    render() {
        const self = this;
        const sizeText = this.state.selectedValues.map(function (key) {
            if (self.sizeMap[key]) {
                return self.sizeMap[key];
            }
            else {
                return key;
            }
        });
        const sizes = this.props.sizeList ? this.props.sizeList : [];
        const sizeList = objectKeys(this.sizeMap).map(function (key, i) {
            if (sizes.indexOf(key) >= 0) {
                let styleSelect = self.state.selectedValues.includes(key) ? 'size-pallet-div size-pallet-div-selected' : 'size-pallet-div';
                return (<div key={i} value={key} onClick={(e) => self.handleSelectedValue(e)} className={styleSelect}>{key}</div>);
            }
            else {
                return null;
            }
        });
        return (
            <div>
                {this.multiselect ? <div className="pallet-text-multiselect">SIZE:</div> : <div className="pallet-text">{"SIZE: " + String(sizeText)}</div>}
                <div className="size-pallet-container" style={this.multiselect ? { width: '100%' } : { display: "inline-flex" }} >
                    {sizeList}
                </div>
                <br />
            </div>
        )
    }
}
export default SizePallets;