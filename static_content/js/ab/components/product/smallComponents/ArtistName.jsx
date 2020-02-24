import React from 'react';

const ArtistName = (props) => (
    <div className={"fl left-bar"} style={props.isMobile ? { height: '20vw' } : { height: '8vw' }}>
        <a className="product-page-artist-link" href={props.link ? props.link : ""}>
            <center>
                <h3 className={props.isMobile ? "artist-designedby-product-page-mobile" : "artist-designedby-product-page"} > {props.artistName == "" ? "" : "Designed by"}</h3>
                <h3 className={props.isMobile ? "artist-name-product-page-mobile" : "artist-name-product-page"} > {props.artistName == "" ? "" : props.artistName}</h3>
            </center>
        </a>
    </div>
);

export default ArtistName;