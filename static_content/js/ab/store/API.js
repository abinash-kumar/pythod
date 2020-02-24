import request from 'superagent';
import * as SliderActions from "../actions/SliderActions.jsx";
import * as UserActions from "../actions/UserActions.jsx";
import * as DesignerActions from "../actions/DesignerAction.jsx";
import * as ProductActions from "../actions/ProductAction.jsx";
import * as AuraaiActions from "../actions/AuraaiAction.jsx"
import * as ArtistAction from "../actions/ArtistAction.jsx";

const API = {
	getImages: function (onPage, path, callback) {
		var url = '/apis/get-slider-image/';
		if (onPage == 'designer') {
			url = '/designers/apis/slider-image/' + path + '/';
		}
		request
			.post(url)
			.set('Accept', 'application/json')
			.send({ 'csrfmiddlewaretoken': window.getCookie('csrftoken') })
			.type('form')
			.end(function (err, res) {
				if (res.ok) {
					callback(res.body)
				} else {
					alert("Error! Pleasecheck console")
				}
			});
	},


	getUserDetail: function (callback) {
		request
			.post("/user/apis/get-user-details/")
			.set('Accept', 'application/json')
			.type('form')
			.send({ 'csrfmiddlewaretoken': window.getCookie('csrftoken') })
			.end(function (err, res) {
				if (res.ok) {
					callback(res.body)
				} else {
					alert("Error! Pleasecheck console")
					console.log(err);
				}
			});
	},

	sendOTP: function (mobile, callback) {
		request
			.post("/user/apis/send-otp/")
			.set('Accept', 'application/json')
			.type('form')
			.send({ 'mobile': mobile, 'csrfmiddlewaretoken': window.getCookie('csrftoken') })
			.end(function (err, res) {
				if (res.ok) {
					callback(res.body)
				} else {
					alert("Error! Pleasecheck console")
					console.log(err);
				}
			});
	},

	verifyOTP: function (otp, mobile, callback) {
		request
			.post("/user/apis/verify-otp/")
			.set('Accept', 'application/json')
			.type('form')
			.send({ 'otp': otp, 'mobile': mobile, 'csrfmiddlewaretoken': window.getCookie('csrftoken') })
			.end(function (err, res) {
				if (res.ok) {
					callback(res.body)
				} else {
					alert("Error! Pleasecheck console")
					console.log(err);
				}
			});
	},

	updateNewAddress: function (name, address, city, state, pincode, mobile, email, callback) {
		request
			.post("/user/apis/add-new-address/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'name': name,
				'address': address,
				'city': city,
				'state': state,
				'pincode': pincode,
				'mobile': mobile,
				'email': email,
				'csrfmiddlewaretoken': window.getCookie('csrftoken')
			})
			.end(function (err, res) {
				if (res.ok) {
					callback(res.body)
				} else {
					alert("Error! Pleasecheck console")
					console.log(err);
				}
			});
	},

	getOrderDetailOfUser: function (
		transaction_id,
		name,
		address,
		city,
		state,
		pincode,
		mobile,
		email,
		callback) {
		request
			.post("/apis/review-order/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'transaction_id': transaction_id,
				'name': name,
				'address': address,
				'city': city,
				'state': state,
				'pincode': pincode,
				'mobile': mobile,
				'email': email,
				'csrfmiddlewaretoken': window.getCookie('csrftoken')
			})
			.end(function (err, res) {
				if (res.ok) {
					console.log(res.body)
					callback(res.body)
				} else {
					alert("Error! Pleasecheck console")
					console.log(err);
				}
			});
	},

	signUpCustomer: function (
		name,
		email,
		mobile,
		password,
		callback) {
		request
			.post("/user/apis/signup-user/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'name': name,
				'email': email,
				'mobile': mobile,
				'password': password,
				'coupon': getCookie('code'),
				'csrfmiddlewaretoken': window.getCookie('csrftoken')
			})
			.end(function (err, res) {
				if (res.ok) {
					if (res.body.success) {
						UserActions.updateUserDetails(
							res.body['user_full_name'],
							res.body['user_email'],
							res.body['user_mobile'],
							res.body['user_photo'],
							res.body['orders_list'],
							res.body['customer_details'],
						)
						callback(res.body)
					}
					else {
						alert(res.body.msg)
					}
				} else {
					alert("Error! Pleasecheck console")
					console.log(err);
				}
			});
	},

	signUpDesigner: function (
		name,
		email,
		mobile,
		password,
		brand,
		pincode,
		callback
	) {
		request
			.post("/designers/apis/designer-signup-api/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'name': name,
				'email': email,
				'mobile': mobile,
				'password': password,
				'brand': brand,
				'pincode': pincode,
				'csrfmiddlewaretoken': window.getCookie('csrftoken')
			})
			.end(function (err, res) {
				if (res.ok) {
					callback(res.body)
				} else {
					alert("Error! Pleasecheck console")
					console.log(err);
				}
			});
	},

	signUpArtist: function (
		name,
		email,
		mobile,
		password,
		artist_type,
		callback
	) {
		request
			.post("/artist/apis/artist-signup/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'name': name,
				'email': email,
				'mobile': mobile,
				'password': password,
				'password': password,
				'csrfmiddlewaretoken': window.getCookie('csrftoken')
			})
			.end(function (err, res) {
				if (res.ok) {
					callback(res.body)
				} else {
					alert("Error! Pleasecheck console")
					console.log(err);
				}
			});
	},

	signInCustomer: function (username, password, callback) {
		request
			.post("/user/apis/signin-user/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'name': username,
				'password': password,
				'csrfmiddlewaretoken': window.getCookie('csrftoken')
			})
			.end(function (err, res) {
				if (res.ok) {
					if (res.body['success']) {
						UserActions.updateUserDetails(
							res.body['user_full_name'],
							res.body['user_email'],
							res.body['user_mobile'],
							res.body['user_photo'],
							res.body['orders_list'],
							res.body['customer_details'],
						)
						setCookie("isSignIn", "true", 365);
						callback(res.body);
					}
					else {
						setCookie("isSignIn", "", -1);
						callback(res.body);
					}
				}
				else {
					console.log(err);
				}
			});
	},

	checkMobileExistForUser: function (mobile, callback) {
		request
			.post("/user/apis/check-mobile/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'mobile': mobile,
				'csrfmiddlewaretoken': window.getCookie('csrftoken')
			})
			.end(function (err, res) {
				if (res.ok) {
					callback(res.body);
				}
				else {
					console.log(err);
				}
			});

	},

	resetPasswordSendMail: function (email, callback) {
		request
			.post("/user/apis/reset-password/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'email': email,
				'csrfmiddlewaretoken': window.getCookie('csrftoken')
			})
			.end(function (err, res) {
				if (res.ok) {
					callback(res.body);
				}
				else {
					console.log(err);
				}
			});

	},

	sendEmailLink: function () {
		request
			.post("/user/apis/send-email/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'csrfmiddlewaretoken': window.getCookie('csrftoken')
			})
			.end(function (err, res) {
				if (res.ok) {
					UserActions.getEmailSentStatus(res.body)
					console.log(res);
				}
				else {
					console.log(err);
				}
			});
	},


	fetchDesigners: function (data) {
		request
			.post("/designers/apis/get-all-designers/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
				'designers': data,
			})
			.end(function (err, res) {
				if (res.ok) {
					DesignerActions.getAllDesignerDetails(res.body)
					console.log(res);
				}
				else {
					console.log(err);
				}
			});
	},

	fetchProduct: function (slug, id) {
		request
			.post("/product/apis/get-product-detail/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
				'slug': slug,
				'id': id,
			})
			.end(function (err, res) {
				if (res.ok) {
					ProductActions.getProductDetails(res.body)
					console.log(res);
				}
				else {
					console.log(err);
				}
			});
	},

	fetchAllProducts: function (product, tag, varients, page, slug) {
		if (product == 'search') {
			request
				.post("/aura/apis/product/search/")
				.set('Accept', 'application/json')
				.type('form')
				.send({
					'search_key': getValueOfParam('search'),
					'csrfmiddlewaretoken': window.getCookie('csrftoken'),
				})
				.end(function (err, res) {
					if (res.ok) {
						ProductActions.getAllProductDetails(res.body)
						//AuraaiActions.getSearchResult(res.body.product_detail_list)
					}
					else {
						console.log(err);
					}
				});
		}
		else {
			request
				.post("/product/apis/tshirt/list/")
				.set('Accept', 'application/json')
				.type('form')
				.send({
					'csrfmiddlewaretoken': window.getCookie('csrftoken'),
					'varients': JSON.stringify(varients),
					'page': page,
					'category': product,
					'slug': slug,
				})
				.end(function (err, res) {
					if (res.ok) {
						ProductActions.getAllProductDetails(res.body)
					}
					else {
						console.log(err);
					}
				});
		}
	},

	fetchFbMagicSearchData: function (callback) {
		request
			.post("/aura/apis/magic/search/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
			})
			.end(function (err, res) {
				if (res.ok) {
					console.log(res);
					callback(res.body);
				}
				else {
					console.log(err);
				}
			});
	},

	fetchProductVarient: function (product, id) {

		if (product = 'tshirt') {
			request
				.post("/product/apis/tshirt/varient/byid/")
				.set('Accept', 'application/json')
				.type('form')
				.send({
					'id': id,
					'csrfmiddlewaretoken': window.getCookie('csrftoken'),
				})
				.end(function (err, res) {
					if (res.ok) {
						ProductActions.getAllProductVarient(res.body)
						console.log(res);
					}
					else {
						console.log(err);
					}
				});
		}
	},

	fetchProductPriceVarientID: function (id, varients, callback) {
		request
			.post("/product/apis/tshirt/varient/id-price/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'id': id,
				'varients': JSON.stringify(varients),
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
			})
			.end(function (err, res) {
				if (res.ok) {
					callback(res.body);
					console.log(res);
				}
				else {
					console.log(err);
				}
			});
	},

	addToCart: function (varinetId) {
		request
			.post("/product/apis/add-cart/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
				'productvarientids': varinetId,
				'update_in': 'CART',
			})
			.end(function (err, res) {
				if (res.ok) {
					setCookie("token", res.body.token, 365)
					UserActions.updateCart()
				}
				else {
					console.log(err);
				}
			});
	},

	fetchTagProduct: function (product, tag, varients, page) {
		request
			.post("/aura/apis/tags/products/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
				'product': product,
				'tag': tag,
				'varients': varients,
				'page': page,
			})
			.end(function (err, res) {
				if (res.ok) {
					ProductActions.getAllProductDetails(res.body)
					console.log(res);
				}
				else {
					console.log(err);
				}
			});
	},

	fetchAllBanners: function () {
		request
			.post("/aura/apis/tags/get/all-banners/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
			})
			.end(function (err, res) {
				if (res.ok) {
					console.log(res);
					AuraaiActions.getAllBanners(res.body)

				}
				else {
					console.log(err);
				}
			});
	},

	fetchAutocompleteKeys: function (autocomplete_key) {
		request
			.post("/aura/apis/autocomplete/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'autocomplete_key': autocomplete_key,
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
			})
			.end(function (err, res) {
				if (res.ok) {
					console.log(res);
					AuraaiActions.getAutocompleteKeys(res.body.autocomplete_values)
				}
				else {
					console.log(err);
				}
			});
	},

	fetchArtistDetails: function () {
		request
			.post("/user/apis/customer/details/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
			})
			.end(function (err, res) {
				if (res.ok) {
					console.log(res);
					UserActions.getArtistDetails(res.body)

				}
				else {
					console.log(err);
				}
			});
	},

	fetchArtistDesigns: function () {
		request
			.post("/artist/apis/get/designs/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
			})
			.end(function (err, res) {
				if (res.ok) {
					console.log(res);
					UserActions.getArtistDesigns(res.body)
				}
				else {
					console.log(err);
				}
			});
	},

	fetchArtistDesignsPublic: function (artistID, callback) {
		request
			.post("/artist/apis/get/designs/public")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
				'artistID': artistID,
			})
			.end(function (err, res) {
				if (res.ok) {
					console.log(res);
					callback(res.body);
				}
				else {
					console.log(err);
				}
			});
	},

	fetchAllArtists: function () {
		request
			.post("/artist/apis/all-artists/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
			})
			.end(function (err, res) {
				if (res.ok) {
					console.log(res);
					ArtistAction.getAllArtist(res.body)
				}
				else {
					console.log(err);
				}
			});
	},

	fetchArtistOtherDetails: function () {
		request
			.post("/artist/apis/get/other/details/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
			})
			.end(function (err, res) {
				if (res.ok) {
					console.log(res);
					ArtistAction.getArtistOtherDetails(res.body)
				}
				else {
					console.log(err);
				}
			});
	},

	fetchArtistBankDetails: function () {
		request
			.post("/artist/apis/get/bank/details/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
			})
			.end(function (err, res) {
				if (res.ok) {
					console.log(res);
					ArtistAction.getArtistBankDetails(res.body)
				}
				else {
					console.log(err);
				}
			});
	},

	fetchIfscDetails: function (ifsc_code, callback) {
		request
			.post("/ab/apis/bank/ifsc/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
			})
			.send({
				'ifsc': ifsc_code,
			})
			.end(function (err, res) {
				if (res.ok) {
					console.log(res);
					callback(res.body)
				}
				else {
					console.log(err);
				}
			});
	},

	setUserDetails: function (first_name, last_name, gender, dob, callback) {
		request
			.post("/user/apis/customer/details/save/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
			})
			.send({
				'first_name': first_name,
				'last_name': last_name,
				'gender': gender,
				'dob': dob,
			})
			.end(function (err, res) {
				if (res.ok) {
					console.log(res);
					callback(res.body)
				}
				else {
					console.log(err);
				}
			});
	},

	setArtistBankDetails: function (account_holder_name,
		ifsc_code,
		account_no,
		pan,
		bank_name,
		branch_name,
		bank_branch_address,
		account_type,
		callback) {
		request
			.post("/artist/apis/set/bank/details/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
			})
			.send({
				'account_holder_name': account_holder_name,
				'ifsc_code': ifsc_code,
				'account_no': account_no,
				'pan': pan,
				'bank_name': bank_name,
				'branch_name': branch_name,
				'bank_branch_address': bank_branch_address,
				'account_type': account_type,
			})
			.end(function (err, res) {
				if (res.ok) {
					console.log(res);
					callback(res.body)
				}
				else {
					console.log(err);
				}
			});
	},

	setArtistDetails: function (about, address, pin_code, city, state, artist_type, callback) {
		request
			.post("/artist/apis/set/other/details/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
			})
			.send({
				'about': about,
				'address': address,
				'pin_code': pin_code,
				'city': city,
				'state': state,
				'artist_type': artist_type,
			})
			.end(function (err, res) {
				if (res.ok) {
					console.log(res);
					callback(res.body)
				}
				else {
					console.log(err);
				}
			});
	},


	fetchArtistSocialLinks: function () {
		request
			.post("/artist/apis/get/social-links/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
			})
			.end(function (err, res) {
				if (res.ok) {
					console.log(res);
					ArtistAction.getArtistSocialLinks(res.body)
				}
				else {
					console.log(err);
				}
			});
	},

	setArtistSocialLinks: function (url, callback) {
		request
			.post("/artist/apis/set/social-links/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'url': url,
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
			})
			.end(function (err, res) {
				if (res.ok) {
					console.log(res);
					callback(res.body);
				}
				else {
					console.log(err);
				}
			});
	},

	removeArtistDesign: function (designId, callback) {
		request
			.post("/artist/apis/remove/design/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'design_id': designId,
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
			})
			.end(function (err, res) {
				if (res.ok) {
					console.log(res);
					callback(res.body);
				}
				else {
					console.log(err);
				}
			});
	},

	uploadArtistDesign: function (file) {
		request
			.post("/product/apis/artist/design/upload/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'user_name': 'shubhroshekhar@gmail.com',
				'file': file,
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
			})
			.end(function (err, res) {
				if (res.ok) {
					console.log(res);
					UserActions.getArtistDesigns(res.body)
				}
				else {
					console.log(err);
				}
			});
	},

	uploadArtistDesignForm: function (filePath, title, comment, tags, callback) {
		request
			.post("/artist/upload/design/")
			.field('title', title)
			.field('comment', comment)
			.field('tags', tags)
			.field('csrfmiddlewaretoken', window.getCookie('csrftoken'))
			.attach('design', filePath)
			.end(function (err, res) {
				if (res.ok) {
					console.log(res);
					callback(res.body);
					//UserActions.getArtistDesigns(res.body)
				}
				else {
					console.log(err);
				}
			});
	},

	editArtistDesignForm: function (designID, filePath, title, comment, tags, callback) {
		request
			.post("/artist/apis/edit/design/")
			.field('title', title)
			.field('comment', comment)
			.field('tags', tags)
			.field('design_id', designID)
			.field('csrfmiddlewaretoken', window.getCookie('csrftoken'))
			.attach('design', filePath)
			.end(function (err, res) {
				if (res.ok) {
					console.log(res);
					callback(res.body);
				}
				else {
					console.log(err);
				}
			});
	},

	fetchArtistPublicProfile: function (artistID) {
		request
			.post("/artist/apis/get-profile/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'artistID': artistID,
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
			})
			.end(function (err, res) {
				if (res.ok) {
					UserActions.getArtistPublicProfile(res.body)
				}
				else {
					console.log(err);
				}
			});
	},

	uploadUserProfilePic: function (filePath, callback) {
		request
			.post("/user/update/profile-pic/")
			.field('csrfmiddlewaretoken', window.getCookie('csrftoken'))
			.attach('user_photo', filePath)
			.end(function (err, res) {
				if (res.ok) {
					console.log(res);
					callback(res.body);
					//UserActions.getArtistDesigns(res.body)
				}
				else {
					console.log(err);
				}
			});
	},

	fetchUserWallet: function () {
		request
			.post("/user/apis/wallet/")
			.field('csrfmiddlewaretoken', window.getCookie('csrftoken'))
			.end(function (err, res) {
				if (res.ok) {
					console.log(res);
					UserActions.getUserWallet(res.body)
				}
				else {
					console.log(err);
				}
			});
	},

	deliveryPincodeCheck: function (pincode) {
		request
			.post("/ab/apis/check/payment-modes/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'pincode': pincode,
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
			})
			.end(function (err, res) {
				if (res.ok) {
					console.log(res);
					ProductActions.getPincodeStatus(res.body)
				}
				else {
					console.log(err);
				}
			});
	},

	fetchCityStateFromPincode: function (pincode, callback) {
		request
			.post("/ab/apis/check/pincode/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
				'pincode': pincode,
			})
			.end(function (err, res) {
				if (res.ok) {
					console.log(res);
					callback(res.body);
				}
				else {
					console.log(err);
				}
			});
	},

	redeemCoupon: function (code, type, callback) {
		request
			.post("/user/apis/redeem-coupon/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'code': code,
				'type': type,
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
			})
			.end(function (err, res) {
				if (res.ok) {
					if (res.body.hasOwnProperty('txn_id')) {
						setCookie("txn_id", res.body.txn_id, 1);
					}
					if (res.body.hasOwnProperty('txn_id') || (window.location.pathname.indexOf('my-cart') > 0 && !res.body.error)) {
						setCookie('coupon', '', -1)
						location.reload()
					}
					UserActions.getNewRedeemValue(res.body)
					callback(res.body)
				}
			});
	},

	getNotification: function (callback) {
		request
			.post("/apis/notification/")
			.set('Accept', 'application/json')
			.type('form')
			.send({
				'csrfmiddlewaretoken': window.getCookie('csrftoken'),
			})
			.end(function (err, res) {
				if (res.ok) {
					callback(res.body)
				}
			});
	}
}

module.exports = API