import React from 'react';

const ProducOffer = (props) => (
    <div>{props.offer ? <div className="left-bar">{String(props.offer)}</div> : null}</div>
);

export default ProducOffer;