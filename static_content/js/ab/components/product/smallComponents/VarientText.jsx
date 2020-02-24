import React from 'react';

const VarientText = (props) => (
    <div>
        <h3 className={props.isMobile ? "artist-designedby-product-page-mobile" : "artist-designedby-product-page"}>100% Cotton</h3>
        <h3 className={props.isMobile ? "artist-designedby-product-page-mobile" : "artist-designedby-product-page"}>Regular Fit</h3>
        <h3 className={props.isMobile ? "artist-designedby-product-page-mobile" : "artist-designedby-product-page"}
            style={props.isMobile ? {
                overflow: 'hidden',
                whiteSpace: 'nowrap',
                textOverflow: 'ellipsis'
            } : {}}>Perfect fit not too tight not too loose.</h3>
    </div>
);

export default VarientText;