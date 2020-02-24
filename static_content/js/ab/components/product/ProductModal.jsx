import React from 'react';
import ReactDOM from 'react-dom';
import Modal from 'react-responsive-modal';
import ProductStore from '../../store/ProductStore.jsx';
import Slider from 'react-slick';

import RaisedButton from 'material-ui/RaisedButton';
import Menu from 'material-ui/Menu';
import MenuItem from 'material-ui/MenuItem';
import ProductVarientsContainer from './ProductVarients.jsx';
import ColorPalletsMini from './ColorPalletsMini.jsx';

import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import ProgressiveImage from "react-progressive-image-loading";


class SampleNextArrow extends React.Component {
	constructor(props) {
		super(props);
	}
	render() {
		const className = this.props.className
		const style = this.props.style
		const onClick = this.props.onClick
		const mystyle = function () {
			console.log(className)
			if (className.indexOf("slick-disabled") >= 0) {
				return { display: 'none' };
			}
		}();
		return (
			<div
				className={'right-arrow'}
				style={mystyle}
				onClick={onClick}
			></div>
		)
	}
}


class SamplePrevArrow extends React.Component {
	constructor(props) {
		super(props);
	}
	render() {
		const className = this.props.className
		const style = this.props.style
		const onClick = this.props.onClick
		const mystyle = function () {
			console.log(className)
			if (className.indexOf("slick-disabled") >= 0) {
				return { display: 'none' };
			}
		}();
		return (
			<div
				className={'left-arrow'}
				style={mystyle}
				onClick={onClick}
			></div>
		)
	}
}


class DialogVarients extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			open: false,
			varients: this.props['varients'],
			product_id: this.props['product_id'],
			productSlug: this.props['productSlug'],
			type: this.props['type']
		};
	}

	handleOpen = () => {
		this.setState({ open: true });
	};

	handleClose = () => {
		this.setState({ open: false });
	};

	render() {
		const actions = [
			<FlatButton
				label="Cancel"
				primary={true}
				onClick={this.handleClose}
			/>,
		];

		return (
			<div>
				<RaisedButton label={this.state.type} onClick={this.handleOpen} className="buy-now-btn" />
				<Dialog
					title="Select Varient"
					actions={actions}
					modal={false}
					open={this.state.open}
					onRequestClose={this.handleClose}
					contentStyle={{ width: '350px' }}
				>
					<div>
						<ProductVarientsContainer product_id={this.state.product_id} productSlug={this.state.productSlug} req_close={this.handleClose} submitType={this.state.type} req_close_modal={this.props.req_close_modal} />
					</div>
				</Dialog>
			</div>
		);
	}
}


class ProductModal extends React.Component {

	constructor(props) {
		super(props);
		this.onOpenModal = this.onOpenModal.bind(this);
		this.productSlug = props['productSlug'];
		this.productID = props['productID'];
		this.onCloseModal = this.onCloseModal.bind(this);
		this.getProductDetail = this.getProductDetail.bind(this);
		this.getProductVarientDetail = this.getProductVarientDetail.bind(this);
		this.product = this.props['product']
		this.state = {
			open: false,
			productData: null,
			productVarient: null,
		};
	}
	componentWillReceiveProps(nextProps) {
		debugger
	}

	getProductVarientDetail() {
		this.setState({
			productVarient: ProductStore.getProductVarientDetail()
		});
	}
	componentWillMount() {
		ProductStore.on("change", this.getProductDetail);
		ProductStore.on("change", this.getProductVarientDetail);
	}

	componentWillUnmount() {
		ProductStore.removeListener("change", this.getProductDetail);
		ProductStore.removeListener("change", this.getProductVarientDetail);
	}

	getProductDetail() {
		this.setState({
			productData: ProductStore.getProductDetail()
		});
	}

	onOpenModal() {
		ProductStore.fetchProduct(this.productSlug, this.productID);
		//ProductStore.fetchProductVarient('tshirt', this.productID); //TODO
		this.setState({ open: true });
	}

	onCloseModal() {
		this.setState({ open: false, productData: null });
	}

	render() {
		const { open } = this.state;
		const productTitle = !this.state.productData ? null : this.state.productData['product_name'];
		const productDescription = !this.state.productData ? null : this.state.productData['product_main_description'];
		const productPrice = !this.state.productData ? null : parseInt(this.state.productData['product_price']).toLocaleString('en-IN', {
			maximumFractionDigits: 2,
			style: 'currency',
			currency: 'INR'
		});;

		var settings = {
			dots: true,
			infinite: false,
			arrows: true,
			nextArrow: <SampleNextArrow />,
			prevArrow: <SamplePrevArrow />,
		}


		const imagesComponent = !this.state.productData || this.state.productData.length == 0 ? null : this.state.productData['product_images_url'].map((image) => (
			<img src={image.url} alt="Product image - Addiction Bazaar" style={{ minHeight: '100%' }} />
		)
		);

		const slider = function () {
			if (imagesComponent) {
				return (
					<div>
						<Slider  {...settings}>
							{imagesComponent}
						</Slider>
						<div className='ab-price-btn'>{productPrice}</div>
						<div className='btn-container-popup'>


							<DialogVarients product_id={this.productID} productSlug={this.productSlug} type="Add to Cart" req_close_modal={this.onCloseModal} />
							<DialogVarients product_id={this.productID} productSlug={this.productSlug} type="Buy Now" />

						</div>
						<div className='product-modal-detail'>
							<h2>{productTitle}</h2>
							<h3>{productDescription}</h3>
						</div>
					</div>
				)
			}
		}.bind(this)();
		const product = this.product;
		return (
			<div>

				<div className='background-masker loader card-1'>

					<div className='product1'>
						<a href={"/product/" + product['slug'] + "/" + product['id'] + "/"}>
							<img className='pd' src={product['product_photo_url'][0]} alt={"Product " + product['name'] + " at Addiction Bazaar"} />
						</a>
						<a>
							<img className='quick' onClick={this.onOpenModal} src={staticImage("/static/img/quick_view.png")} alt="" />
						</a>
					</div>

					<div className='product1'>
						<p className="cust-text"><b>{product['name']}</b></p>
						<span className="p-price" style={product['price'] > product['price_after_discount'] ? { textDecoration: 'line-through' } : { textDecoration: 'none' }}>
							{
								product['price'].toLocaleString('en-IN', {
									maximumFractionDigits: 2,
									style: 'currency',
									currency: 'INR'
								})}
						</span>
						<span className="p-discount">{product['price'] > product['price_after_discount'] ? product['price_after_discount'].toLocaleString('en-IN', {
							maximumFractionDigits: 2,
							style: 'currency',
							currency: 'INR'
						}) : null}
						</span>
						<ColorPalletsMini colorList={product['colors']} />
						<p className="cust-text" >{product['artist'] == "" ? <td dangerouslySetInnerHTML={{ __html: '&nbsp;' }} /> : "by-" + product['artist']}</p>
						<div className="offer-text" style={{ position: 'inherit', }}>
							{product['offers'][0] == undefined ? <td dangerouslySetInnerHTML={{ __html: '&nbsp;' }} /> : product['offers'][0]}
						</div>
					</div>

				</div>
				<Modal modalClassName='modal-product' open={open} onClose={this.onCloseModal} little>
					<div className='modal-product'>
						{slider}
					</div>
				</Modal>
			</div>
		);
	}

}

export default ProductModal;