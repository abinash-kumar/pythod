import React from 'react';

const styles = {
    expandable: {
        overflowY: 'hidden',
        maxHeight: 500,
        transitionProperty: 'all',
        transitionDuration: '.1s',
        'transition-timing-function': 'cubic- bezier(0, 1, 0.5, 1)',

    },
    expandableTarget: {
        overflowY: 'hidden',
        transitionProperty: 'all',
        transitionDuration: '.1s',
        'transition-timing-function': 'cubic- bezier(0, 1, 0.5, 1)',
        maxHeight: 0,
    },
    arrow: {
        float: 'right',
        padding: 3,
        paddingRight: 10,
        transition: 'opacity 0.5s linear',
    },
    listPoint: {
        padding: 6,
        fontSize: 9,
        color: 'grey',
    }
};

class Accordian extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            showText: !this.props.show,
        }
    }

    renderText = (text) => (<p style={this.props.pStye}>{text}</p>);
    renderMarkDown = (markDownText) => (<div style={{ padding:10, paddingLeft:15 }} dangerouslySetInnerHTML={this.createMarkup(markDownText)} />);
    renderList = (list) => (
        <div style={this.props.listStye}><ul>
            {list.map(text => (<li style={this.props.listItemStyle}><i style={styles.listPoint} className="fa fa-circle"></i>{text}</li>))}
        </ul></div>
    );
    renderObject = (obj) => (
        <div style={this.props.listStye}><ul>
            {objectKeys(obj).map(title => (<li><b>{title}</b> &nbsp; {obj[title]}</li>))}
        </ul></div>
    );
    renderBody = () => {
        const description = this.props.description;
        let body;
        if (typeof (description) === 'string') {
            body = this.props.markDown ? this.renderMarkDown(description) : this.renderText(description);
        } else if (Array.isArray(description)) {
            body = this.renderList(description);
        } else if (typeof (description) === 'object') {
            body = this.renderObject(description);
        }
        return (<div style={this.state.showText ? styles.expandableTarget : styles.expandable}>{body}</div>
        );
    };

    handleClick = () => {
        this.setState({ showText: !this.state.showText })
    };

    createMarkup = (text) => {
        return {__html: text};
    };

    render() {
        return (<div style={this.props.bodyStyle}>
            <div style={this.props.headerStyle} onClick={this.handleClick}>
                <b>{this.props.title}</b>
                <div style={styles.arrow}>
                    <i className={`fa fa-angle-${this.state.showText ? 'down' : 'up'}`} aria-hidden="true"></i>
                </div>
            </div>
            {this.renderBody()}
        </div>);
    }
}

Accordian.propTypes = {
    bodyStyle: React.PropTypes.object,
    listStye: React.PropTypes.object,
    listItemStyle: React.PropTypes.object,
    pStye: React.PropTypes.object,   
    headerStyle: React.PropTypes.object,  
    show: React.PropTypes.bool,
    markDown: React.PropTypes.bool,
};

Accordian.defaultProps = {
    bodyStyle: {
        width: '100%',
        paddingTop: 20,
        // margin: 6,
    },
    listStye: {
        margin: 0,
        marginLeft: 30,
        columnCount: 2,
    },
    listItemStyle: {
        // listStyleType: 'circle',
        paddingTop: 10,
        paddingBottom: 0,
        whiteSpace: 'nowrap', 
        overflow: 'hidden',
        textOverflow: 'ellipsis',
    },
    pStye: {
        margin: 0,
        marginLeft: 17,
    },
    headerStyle: {
        borderStyle: 'solid',
        borderRadius: 13,
        borderWidth: 1,
        paddingLeft: 10,
    },
    markDown: false,
    show: true,
};

export default Accordian;