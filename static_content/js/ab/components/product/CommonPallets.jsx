import React from 'react';

class CommonPallets extends React.Component {
    constructor(props) {
        super(props);
        this.handleSelectedValue = this.handleSelectedValue.bind(this);
        this.multiselect = this.props.multiSelect;
        if (!this.props.callbackFunction) {
            throw new Error("callbackFunction(Function) Prop is mandetory");
        }
        this.callbackFunction = this.props.callbackFunction;
        this.state = {
            selectedValues: props.selectedValues ? props.selectedValues : [],
            showingDropdown: false,
        }
    }
    componentWillReceiveProps(nextProps) {
        if (nextProps.selectedValues) {
            this.setState({ selectedValues: nextProps.selectedValues });
        }
    }

    componentDidMount() {
        const self = this;
        $('body').click(function () {
            self.setState({ showingDropdown: false });
        });
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
        this.setState({ selectedValues, showingDropdown: false });
        this.callbackFunction({ type: this.props.varientType, values: selectedValues });
    }
    toggleDropdown() {
        let showingDropdown = this.state.showingDropdown;
        this.setState({ showingDropdown: !showingDropdown })
    }

    render() {
        const self = this;
        if (!this.props.varientType) {
            throw new Error("varientType(String) Prop is mandetory");
        }
        const palletText = this.props.varientType;
        const pallets = !this.props.varients ? null : this.props.varients.map(function (key, i) {
            let styleSelect = self.state.selectedValues.includes(key) ? self.multiselect ? 'common-pallet-div size-pallet-div-selected' : 'common-pallet-div common-pallet-div-selected' : 'common-pallet-div';
            return (<li key={i} value={key} onClick={(e) => self.handleSelectedValue(e)} className={styleSelect}>{key}</li>);
        });
        return (
            <div className="col-sm-12 col-md-12" >
                <br />
                {this.multiselect ? null : <div className="common-pallet-text col-sm-5 col-md-5 col-xs-5">{palletText + ": "}</div>}
                <div className="common-pallet-container col-sm-6 col-md-6 col-xs-6">
                    <div className="pallet-text" onClick={(e) => this.toggleDropdown()}>{this.multiselect ? <div className="pallet-text-multiselect"> {palletText}</div> : this.state.selectedValues.length !== 0 ? this.state.selectedValues : <u>{'Select ' + palletText}</u>}</div>
                    <ul className={this.multiselect ? "common-pallet-dropdown-ul-multiselect" : "common-pallet-dropdown-ul"} style={this.multiselect || this.state.showingDropdown ? { display: 'inherit' } : { display: 'none' }}>
                        {pallets}
                    </ul>
                </div>
            </div>
        )
    }
}
export default CommonPallets;