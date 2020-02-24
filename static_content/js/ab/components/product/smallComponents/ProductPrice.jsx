import React from 'react';

const ProductPrice = (props) => (
    <div>
        {props.discount > 0 ? <div>
            <div>
                <label className="price-product-page">{props.productPriceAfterdiscount}</label>
                <label className="discounted-price line-through">{props.productPrice}</label>
            </div>
            <p className="discount-text-product-page" > &#8377;{props.discount} off</p>
        </div> : <div>
                <p className="price-product-page">{props.productPrice}</p>
            </div>}

    </div>
);

export default ProductPrice;