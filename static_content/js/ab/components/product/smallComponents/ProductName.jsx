import React from 'react';

const ProductName = (props) => (
    <h4 className={props.isMobile ? "product-title-mobile" : "product-title"}>{props.name}</h4>
);

export default ProductName;