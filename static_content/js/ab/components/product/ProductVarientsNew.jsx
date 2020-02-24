import React from 'react';
import ColorPallets from './ColorPallets.jsx';
import SizePallets from './SizePallets.jsx';
import CommonPallets from './CommonPallets.jsx';
import SelectGenger from './productDetailSmallComponents/SelectGender.jsx';
import SelectSize from './productDetailSmallComponents/SelectSize.jsx';
import SelectColor from './productDetailSmallComponents/SelectColor.jsx';
import ProductStore from '../../store/ProductStore.jsx';
import API from '../../store/API'

class ProductVarients extends React.Component {
    constructor(props) {
        super(props);
        this.varients = this.props.varients;
        this.showTitle = this.props.showTitle;
        this.handleVarients = this.handleVarients.bind(this);
        this.checkAllSelected = this.checkAllSelected.bind(this);
        this.listToStringVarients = this.listToStringVarients.bind(this);
        this.getPriceAndVarientId = this.getPriceAndVarientId.bind(this);
        this.updateImage = this.updateImage.bind(this);
        this.state = {
            selectedVarients: null,
        }
    }
    componentWillReceiveProps(nextProps) {
        if (!nextProps.varients) {
            throw new Error("varients Prop is mandetory");
        }
        else {
            if (!nextProps.varients.product_id) {
                throw new Error("product_id is missing in varients");
            }
            if (!nextProps.varients.varient_values) {
                throw new Error("varient_values is missing in varients");
            }
        }
        this.setVarients(nextProps.varients.varient_values);
    }
    updateImage(type, value) {
        let productId = this.varients.product_id
        this.props.varientChange({ id: productId, type, value });
    }
    setVarients(varients) {
        // update state only for first time 
        if (this.state.selectedVarients === null) {
            let selectedVarients = {};
            let allKeys = objectKeys(varients);
            for (let i = 0; i < allKeys.length; i++) {
                if (varients[allKeys[i]].length <= 1) {
                    selectedVarients[allKeys[i]] = varients[allKeys[i]];
                }
                else {
                    selectedVarients[allKeys[i]] = [];
                }
            }
            this.setState({ selectedVarients });
        }
    }
    getPriceAndVarientId(data) {
        this.props.getPriceAndVarientId(data);
    }
    handleVarients(data) {
        let productId = this.varients.product_id
        let selectedVarients = this.state.selectedVarients;
        selectedVarients[data.type] = data.values
        this.setState({ selectedVarients }, this.updateImage(data.type, String(data.values)));
        if (this.checkAllSelected(selectedVarients)) {
            //Get product viarent Id
            API.fetchProductPriceVarientID(productId, this.listToStringVarients(selectedVarients), this.getPriceAndVarientId);
        }
    }
    checkAllSelected(selectedVarients) {
        let all_keys = objectKeys(this.varients.varient_values);
        for (let i = 0; i < all_keys.length; i++) {
            if (this.varients.varient_values[all_keys[i]].length > 1) {
                if (selectedVarients[all_keys[i]].length < 1) {
                    return false;
                }
            }
        }
        return true;
    }
    listToStringVarients(varients) {
        const newVarients = {};
        let allKeys = objectKeys(varients);
        for (let i = 0; i < allKeys.length; i++) {
            newVarients[allKeys[i]] = String(varients[allKeys[i]])
        }
        return newVarients;
    }

    render() {
        const allVarients = [];
        const varient_values = this.varients.varient_values;
        if (varient_values.COLOR && varient_values.COLOR.length > 1) {
            allVarients.push(<SelectColor key="color" callbackFunction={this.handleVarients} colorList={varient_values.COLOR} selectedValues={this.state.selectedVarients ? this.state.selectedVarients.COLOR : []} />)
        }
        if (varient_values.SIZE && varient_values.SIZE.length > 1) {
            allVarients.push(<SelectSize key="size" callbackFunction={this.handleVarients} sizeList={varient_values.SIZE} selectedValues={this.state.selectedVarients ? this.state.selectedVarients.SIZE : []} />)
        }
        if (varient_values.GENDER && varient_values.GENDER.length > 1) {
            allVarients.push(<SelectGenger key="gender" callbackFunction={this.handleVarients} genderList={varient_values.GENDER} selectedValues={this.state.selectedVarients ? this.state.selectedVarients.GENDER : []} />)
        }
        const allKeys = objectKeys(varient_values);
        for (let i = 0; i < allKeys.length; i++) {
            if (allKeys[i] !== 'SIZE' && allKeys[i] !== 'COLOR' && allKeys[i] !== 'GENDER' && varient_values[allKeys[i]].length > 1) {
                allVarients.push(<CommonPallets key={allKeys[i]} callbackFunction={this.handleVarients} varientType={allKeys[i]} varients={varient_values[allKeys[i]]} />);
            }
        }

        return (<div>
            {this.showTitle ? this.varients.title : null}
            {allVarients}
        </div>);
    }
}
export default ProductVarients;