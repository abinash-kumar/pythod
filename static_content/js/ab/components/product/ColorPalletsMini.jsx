import React from 'react';
// import RaisedButton from 'material-ui/RaisedButton';
// import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
// import getMuiTheme from 'material-ui/styles/getMuiTheme'
// import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'


const colorMap = {
    'Antra Grey': '/static/img/colorpallets/antra-grey.png',
    'BLACK': '/static/img/colorpallets/black.png',
    'DARK GREY': '/static/img/colorpallets/dark-grey.png',
    'GREY MILANGE': '/static/img/colorpallets/grey-milange.png',
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

class ColorPalletsMini extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const colorList = !this.props.colorList ? null : this.props.colorList.map(function (key, i) {
            if (colorMap[key]) {
                return (<img key={i} className="color-pallet-image-mini" src={colorMap[key]} />);
            }
            else {
                return ''
            }
        });
        return (
            <div className="color-pallet-container-mini">
                {colorList}
            </div>
        )
    }
}
export default ColorPalletsMini;