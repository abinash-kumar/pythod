import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'
import AutoComplete from 'material-ui/AutoComplete';
import auraaiStore from '../../store/AuraaiStore.jsx';
import Search from 'material-ui/svg-icons/action/search';
import * as AuraaiActions from "../../actions/AuraaiAction.jsx"
import UserStore from '../../store/UserStore.jsx';
import IconSearch from 'material-ui/svg-icons/action/search';
import IconButton from 'material-ui/IconButton';

const lightMuiTheme = getMuiTheme(lightBaseTheme);


class ProductSearch extends React.Component {
    constructor(props) {
        super(props);
        this.getAutocompleteKeys = this.getAutocompleteKeys.bind(this);
        this.getMagicSearchBtnStatus = this.getMagicSearchBtnStatus.bind(this);
        this.isMin = this.props['mini'] == undefined ? false : this.props['mini'];
        this.state = {
            autoComplete: [],
            magicSearchBtnText: null,
            magicSearchBtnLink: null,
            searchKey: getValueOfParam('search') == null ? '' : getValueOfParam('search'),
            miniFocus: true,
        };
    }

    getAutocompleteKeys() {
        this.setState({
            autoComplete: auraaiStore.getAutocompleteKeys()
        })
    }

    getMagicSearchBtnStatus() {
        this.setState({
            magicSearchBtnText: UserStore.getMagicSearchBtnText(),
            magicSearchBtnLink: UserStore.getMagicSearchBtnLink(),
        });
    }
    setFocusMini() {
        setTimeout(function () { $('#myInput').focus(); }, 800);
    }
    componentWillMount() {
        auraaiStore.on("change", this.getAutocompleteKeys);
        UserStore.on("change", this.getMagicSearchBtnStatus);
        console.log('Component WILL MOUNT!')
    }

    _handleAutoCompleteChange(e) {

        const searchKey = e;
        console.log(searchKey)
        this.setState({ searchKey })
        auraaiStore.fetchAutocompleteKeys(searchKey);
    }
    _handleSearchSubmit(e) {
        if (this.state.searchKey.length > 0) {
            var linkUrl = window.location.origin + '/aura/product/search/?search=' + encodeURI(this.state.searchKey);
            window.location.assign(linkUrl);
        }
    }

    render() {
        const magicSearchBtnLink = this.state.magicSearchBtnLink;
        const magicSearchBtnText = this.state.magicSearchBtnText;
        const AutoCompleteSearch = function () {
            if (this.isMin) {
                return (
                    <AutoComplete
                        searchText={this.state.searchKey}
                        floatingLabelText="Search"
                        filter={AutoComplete.fuzzyFilter}
                        dataSource={this.state.autoComplete}
                        maxSearchResults={8}
                        id="myInput"
                        autoFocus={this.state.miniFocus}
                        onUpdateInput={(e) => this._handleAutoCompleteChange(e)}
                        onNewRequest={(e) => this._handleSearchSubmit(e)}
                    />
                );
            }
            else {
                return (
                    <div className="container">
                        <div className="row">
                            <div className="container-90">
                                <div className="col-sm-7 col-xs-7">
                                    <AutoComplete
                                        searchText={this.state.searchKey}
                                        floatingLabelText="Search"
                                        filter={AutoComplete.fuzzyFilter}
                                        dataSource={this.state.autoComplete}
                                        maxSearchResults={8}
                                        fullWidth={true}
                                        autoFocus={true}
                                        onUpdateInput={(e) => this._handleAutoCompleteChange(e)}
                                        onNewRequest={(e) => this._handleSearchSubmit(e)}
                                    />
                                </div>
                                <div className="col-sm-4 col-xs-4">
                                    <RaisedButton
                                        onClick={(e) => this._handleSearchSubmit(e)}
                                        label="Search"
                                        style={{ marginTop: 27 }}
                                    />
                                    &nbsp;
                                    <a href={magicSearchBtnLink != null ? magicSearchBtnLink : ""} >
                                        <RaisedButton
                                            label={magicSearchBtnText != null ? magicSearchBtnText : ""}
                                            style={window.location.host.split('.')[0] != 'test' ? { marginTop: 27, display: 'none' } : { marginTop: 27 }}
                                        />
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        }.bind(this)();
        return (
            <MuiThemeProvider muiTheme={lightMuiTheme}>
                {AutoCompleteSearch}
            </MuiThemeProvider>
        )
    }
}
export default ProductSearch;