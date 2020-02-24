import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'

const lightMuiTheme = getMuiTheme(lightBaseTheme);
const constValues = {
    "home": "/"
}


class BreadCrumb extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        let breadCrumbComponent = []
        let breadcrumb = this.props['bList'] ? this.props['bList'] : [];
        for (let i = 0; i < breadcrumb.length; i++) {
            breadCrumbComponent.push(<li key={i}><a href={breadcrumb[i]['link']}>{breadcrumb[i]['value']}</a></li>);
        }


        return (
            <MuiThemeProvider muiTheme={lightMuiTheme}>
                <nav>
                    <ul className="breadcrumb">
                        {breadCrumbComponent}
                    </ul>
                </nav>
            </MuiThemeProvider>
        )
    }
}
export default BreadCrumb;