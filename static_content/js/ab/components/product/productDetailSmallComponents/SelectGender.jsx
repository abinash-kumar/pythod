import React from 'react';
import IconButton from 'material-ui/IconButton';

const SelectGender = ({ genderList, callbackFunction, selectedValues }) => {
    const genders = [];
    const styleSelected = { background: 'grey' };
    if (genderList.indexOf('MALE') >= 0) {
        genders.push(
            <IconButton
                key="MALE"
                tooltip="MALE"
                touch={true}
                style={selectedValues.indexOf('MALE') >= 0 ? styleSelected : null}
                // tooltipPosition="top-center"
                onClick={() => { callbackFunction({ type: 'GENDER', values: ['MALE'] }) }}
                iconClassName="fa fa-mars" />
        );
    }
    if (genderList.indexOf('FEMALE') >= 0) {
        genders.push(
            <IconButton
                key="FEMALE"
                tooltip="FEMALE"
                touch={true}
                style={selectedValues.indexOf('FEMALE') >= 0 ? styleSelected : null}
                // tooltipPosition="top-center"
                onClick={() => { callbackFunction({ type: 'GENDER', values: ['FEMALE'] }) }}
                iconClassName="fa fa-venus" />
        );
    }

    return (<div className="color-pallet-container"><br />
        <div className="pallet-text">{"GENDER: " + String(selectedValues)}<br /></div>
        {genders}</div>);
};

export default SelectGender;