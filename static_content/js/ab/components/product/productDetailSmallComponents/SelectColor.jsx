import React from 'react';
import IconButton from 'material-ui/IconButton';

const SelectColor = ({ colorList, callbackFunction, selectedValues }) => {
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
    // const styleSelected = { background: 'grey' };
    // console.log('selectedValue', selectedValues)
    const sizes = objectKeys(colorMap).reduce((accumulator, currentValue) => {
        if (colorList.indexOf(currentValue) >= 0) {
            accumulator.push(
                <img
                    key={currentValue}
                    // tooltip={currentValue}
                    src={colorMap[currentValue]}
                    // touch={true}
                    className={selectedValues.indexOf(currentValue) >= 0 ? 'color-pallet-image color-pallet-image-selected' : 'color-pallet-image'}
                    // tooltipPosition="top-center"
                    onClick={() => { callbackFunction({ type: 'COLOR', values: [currentValue] }) }}
                // iconClassName={currentValue}
                />
            );
        }
        return accumulator;
    }, []);
    return (<div className="color-pallet-container"><br />
        <div className="pallet-text">{"COLOR: " + String(selectedValues)}<br /></div>
        {sizes}</div>);
};

export default SelectColor;