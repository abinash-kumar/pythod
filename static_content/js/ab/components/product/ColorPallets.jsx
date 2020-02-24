import React from 'react';
// import RaisedButton from 'material-ui/RaisedButton';
// import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
// import getMuiTheme from 'material-ui/styles/getMuiTheme'
// import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'


const colorMap = {
    'Antra Grey': '/static/img/colorpallets/antra-grey.png',
    'BLACK': '/static/img/colorpallets/black.png',
    'DARK GREY': '/static/img/colorpallets/dark-grey.png',
    'GREY MELANGE': '/static/img/colorpallets/grey-milange.png',
    'LIGHT GREY': '/static/img/colorpallets/light-grey.png',
    'MAROON': '/static/img/colorpallets/maroon.png',
    'ORANGE': '/static/img/colorpallets/orange.png',
    'RED': '/static/img/colorpallets/red.png',
    'NAVY BLUE': '/static/img/colorpallets/navy-blue.png',
    'ROYAL BLUE': '/static/img/colorpallets/royal-blue.png',
    'SKY BLUE': '/static/img/colorpallets/sky-blue.png',
    'WHITE': '/static/img/colorpallets/white.png',
    'YELLOW': '/static/img/colorpallets/yellow.png',
    'PINK': '/static/img/colorpallets/pink.png',
    'ORANGE YELLOW': '/static/img/colorpallets/orange-yellow.png',
    'OLIVE GREEN': '/static/img/colorpallets/olive-green.png',
}

class ColorPallets extends React.Component {
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
        }
    }
    componentWillReceiveProps(nextProps) {
        if (nextProps.selectedValues) {
            this.setState({ selectedValues: nextProps.selectedValues });
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
        this.callbackFunction({ type: 'COLOR', values: selectedValues });
    }

    render() {
        const self = this;
        const colorList = !this.props.colorList ? null : this.props.colorList.map(function (key, i) {
            if (colorMap[key]) {
                let styleSelect = self.state.selectedValues.includes(key) ? 'color-pallet-image color-pallet-image-selected' : 'color-pallet-image';
                return (<img key={i} value={key} onClick={(e) => self.handleSelectedValue(e)} className={styleSelect} src={colorMap[key]} />);
            }
            else {
                console.log(key + "- Color Not In ColorMap")
                return ''
            }
        });
        return (
            <div className="color-pallet-container">
                {this.multiselect ? <div className="pallet-text-multiselect">COLOR:</div> : <div className="pallet-text">{"COLOR: " + String(this.state.selectedValues)}<br /></div>}
                {colorList}
            </div>
        )
    }
}
export default ColorPallets;