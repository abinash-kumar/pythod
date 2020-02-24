import React from 'react';
import IconButton from 'material-ui/IconButton';

const SelectSize = ({ sizeList, callbackFunction, selectedValues }) => {
    const sizeMap = {
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
    const styleSize = {
        borderStyle: 'solid',
        borderRadius: 3,
        borderWidth: 1,
        width: 50,
        padding: 3,
        margin: 7,
        textAlign: 'center',
        borderColor: 'black',
        cursor: 'pointer',
        // boxShadow: '0px 0px 16px 0px grey',
    };
    const styleSelected = {
        borderStyle: 'solid',
        borderRadius: 3,
        borderWidth: 1,
        width: 50,
        padding: 3,
        margin: 7,
        textAlign: 'center',
        background: 'grey',
        borderColor: 'black',
        color: 'floralwhite',
        cursor: 'pointer',
        // boxShadow: '0px 0px 16px 0px grey',
    };
    console.log('selectedValue', selectedValues)
    const sizes = objectKeys(sizeMap).reduce((accumulator, currentValue) => {
        if (sizeList.indexOf(currentValue) >= 0) {
            accumulator.push(
                <div
                    key={currentValue}
                    tooltip={sizeMap[currentValue]}
                    touch={true}
                    style={selectedValues.indexOf(currentValue) >= 0 ? styleSelected : styleSize}
                    // tooltipPosition="top-center"
                    onClick={() => { callbackFunction({ type: 'SIZE', values: [currentValue] }) }}
                    iconClassName={currentValue}
                >
                    {currentValue}
                </div >
            );
        }
        return accumulator;
    }, []);
    return (<div className="color-pallet-container"><br />
        <div className="pallet-text">{"SIZE: " + String(selectedValues)}<br /></div>
        <div style={{ display: 'flex', flexWrap: 'wrap' }}>{sizes}</div></div>);
};

export default SelectSize;