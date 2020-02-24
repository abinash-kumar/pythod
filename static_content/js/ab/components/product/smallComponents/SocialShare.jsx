import React from 'react';

const SocialShare = (props) => (
    <div className="col-sm-12 col-md-12 col-xs-12 social">
        <center><h3 className="social-sahare-heading">Share And Earn</h3></center>
        <div className="col-sm-3 col-md-3 col-xs-3">
            <a href={props.fbLink} >
                <img className="social-icons" src="/static/img/resource/facebook.png" />
            </a>
        </div>
        <div className="col-sm-3 col-md-3 col-xs-3">
            <a href="#" >
                <img className="social-icons" src="/static/img/resource/insta.png" />
            </a>
        </div>
        <div className="col-sm-3 col-md-3 col-xs-3">
            <a href="#" >
                <img className="social-icons" src="/static/img/resource/pintrest.png" />
            </a>
        </div>
        <div className="col-sm-3 col-md-3 col-xs-3">
            <a href={props.twitterLink} >
                <img className="social-icons" src="/static/img/resource/twitter.png" />
            </a>
        </div>

    </div>
);

export default SocialShare;