import React from 'react';
import ColorPallets from './ColorPallets.jsx';
import SizePallets from './SizePallets.jsx';
import CommonPallets from './CommonPallets.jsx';
import ProductStore from '../../store/ProductStore.jsx';

class ProductFilter extends React.Component {
    constructor(props) {
        super(props);
        this.varients = this.props.allVarients ? this.props.allVarients : {};
        this.selectedVarients = this.props.selectedVarients ? this.props.selectedVarients : {};
        this.handleShowFilter = this.handleShowFilter.bind(this);
        this.handleVarients = this.handleVarients.bind(this);
        this.state = {
            isMobile: this.props.isMobile,
            showFilter: false,
        }
    }

    componentWillReceiveProps(nextProps) {
        this.varients = nextProps.allVarients ? nextProps.allVarients : {};
        this.selectedVarients = nextProps.selectedVarients ? nextProps.selectedVarients : {};
        this.setState({ isMobile: nextProps.isMobile });
    }
    handleShowFilter() {
        this.setState({ showFilter: !this.state.showFilter });
    }
    handleVarients(data) {
        this.selectedVarients[data.type] = data.values;
        // send varients object to parent component
        this.props.getVarients(this.selectedVarients);
    }
    render() {
        const self = this;
        const allVarients = [];
        const varient_values = this.varients;
        if (varient_values.COLOR) {
            allVarients.push(<ColorPallets multiSelect={true} key="color" callbackFunction={this.handleVarients} selectedValues={this.selectedVarients.COLOR} colorList={varient_values.COLOR} />);
            allVarients.push(<br key="color-br" />);
        }
        if (varient_values.SIZE) {
            allVarients.push(<SizePallets multiSelect={true} key="size" callbackFunction={this.handleVarients} selectedValues={this.selectedVarients.SIZE} sizeList={varient_values.SIZE} />);
            allVarients.push(<br key="size-br" />);
        }
        const allKeys = objectKeys(varient_values);
        for (let i = 0; i < allKeys.length; i++) {
            if (allKeys[i] !== 'SIZE' && allKeys[i] !== 'COLOR') {
                allVarients.push(<CommonPallets multiSelect={true} key={allKeys[i]} callbackFunction={this.handleVarients} selectedValues={this.selectedVarients[allKeys[i]]} varientType={allKeys[i]} varients={varient_values[allKeys[i]]} />);
                allVarients.push(<br key={i} />);
            }
        }
        if (this.state.isMobile) {
            return (
                <div className="filter-mobile">
                    <div className="filter-mobile-icon" onClick={(e) => this.handleShowFilter()}>
                        <img src="/static/img/resource/filter-icon.png" style={{ width: 20 }} alt="filter-icon" />
                        Filter
                     </div>
                    <hr />
                    <div className="filter-mobile-body" style={this.state.showFilter ? { display: 'inherit' } : { display: 'none' }}>
                        <div>
                            {allVarients}
                        </div>
                    </div>
                </div>
            )
        }
        else {
            return (
                <div >
                    {allVarients}
                </div>
            )
        }
    }
}
export default ProductFilter;