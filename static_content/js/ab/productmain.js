var value = getCookie('cart') == "" ? 0 : parseInt(getCookie('cart'));

// function UserProfileViewModel() {
//     var self = this;
//     self.profilePhoto = ko.observable(profilePhoto);
// }
// if (document.getElementById('user-profile') != null) {
// ko.applyBindings(new UserProfileViewModel(),document.getElementById('user-profile'));
// }
function ProductViewModel() {
    var self = this;
    if (typeof prod_price != 'undefined') {
        var price_before_discount = prod_price;
        var discount = dis_value;
        var discount_t = dis_type;
        self.mainImage = ko.observable(prod_first_url);
        self.varient = ko.observable();
        self.valueInputSize = ko.observable();
        self.discount_type = ko.computed(function () {
            return (discount_t.toLowerCase() == "percentage" ? parseInt(discount) + "%" : parseInt(discount))
        });
        self.price = ko.computed(function () {
            if (discount_t.toLowerCase() === "percentage") {
                return self.price = "₹ " + Math.round(parseInt(price_before_discount) * (1 - discount / 100));
            }
            else {
                return self.price = "₹ " + Math.round(parseInt(price_before_discount) - discount);
            }
        });
        self.discount = ko.observable();
        self.images = ko.observableArray(prod_image_url)
        self.changeImg = function (value) {
            console.log(value);
            console.log(self.mainImage());
            self.mainImage(value);
            mainImageUrl = value;
            jQuery(document).ready(function ($) {
                $('#image1').addimagezoom({ // single image zoom
                    zoomrange: [2, 2],
                    magnifiersize: [300, 400],
                    magnifierpos: 'right',
                    cursorshade: true,
                    magvertcenter: true,
                    speed: 500,
                    largeimage: getUpdatedUrl() //<-- No comma after last option!
                })

            })
        };
    }
    // ***********************************
    self.cartValue = ko.observable(value);
    self.addThisProduct = function (productId) {
        $.ajax({
            type: "POST",
            url: "/product/add-cart/",
            data: {
                'csrfmiddlewaretoken': csrf_token,
                'varient': self.varient(),
                'productId': productId,
                'update_in': 'CART',
                'cookie': document.cookie
            },
            success: function (data) {
                if (data.success) {
                    // animation for add to cart
                    // $('.fa-shopping-cart').parent().on('click', function () {
                    //     var cart = $('.cart');
                    //     var imgtodrag = $('#image1');
                    //     if (imgtodrag) {

                    //         var imgclone = imgtodrag.clone()
                    //             .offset({
                    //             top: imgtodrag.offset().top,
                    //             left: imgtodrag.offset().left
                    //         })
                    //             .css({
                    //             'opacity': '0.5',
                    //                 'position': 'absolute',
                    //                 'height': '150px',
                    //                 'width': '150px',
                    //                 'z-index': '100'
                    //         })
                    //             .appendTo($('body'))
                    //             .animate({
                    //             'top': cart.offset().top + 10,
                    //             'left': cart.offset().left + 10,
                    //             'width': 75,
                    //             'height': 75
                    //         });

                    //         setTimeout(function () {
                    //             cart.effect("shake", {
                    //                 times: 2
                    //             }, 200);
                    //         }, 1500);

                    //         imgclone.animate({
                    //             'width': 0,
                    //                 'height': 0
                    //         }, function () {
                    //             $(this).detach()
                    //         });
                    //     }
                    // });

                    // end for animation  
                    console.log("added succesfully");
                    if (getCookie('token') == "")
                        setCookie('token', data.token, 30);
                    value = getCookie('cart') == "" ? 0 : parseInt(getCookie('cart'));
                    setCookie('cart', value + 1, 30);
                    self.cartValue(value + 1);
                }
                else {
                    console.log("some error");
                }
            },
            async: false
        });
    }
}

ko.applyBindings(new ProductViewModel(), document.getElementById('block-main'));


function deletethisItem(cartId) {
    $.ajax({
        type: "POST",
        url: "/product/delete-cart/",
        data: {
            'csrfmiddlewaretoken': csrf_token,
            'cart_id': cartId,
        },
        success: function (data) {
            if (data.success) {
                console.log("deleted succesfully");
                location.reload();
            }
            else {
                console.log("unable to delete cart");
            }
        },
        async: false
    });
}

function updateSpreadSheet(name, mobile, email, message) {
    $.ajax({
        type: "POST",
        url: "/update_sheet/",
        data: {
            'csrfmiddlewaretoken': csrf_token,
            'name': name,
            'mobile': mobile,
            'email': email,
            'message': message,
        },
        success: function (data) {
            if (data.success) {
                console.log("succesfully");
            }
            else {
                console.log("unable to update");
            }
        },
        async: true
    });
}


function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + "; " + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function removeTokenValue() {
    setCookie('token', '', -1)
    setCookie('cart', '', -1)
}


function convertToINR(value) {
    if (value != null) {
        return value.toLocaleString('en-IN', {
            maximumFractionDigits: 2,
            style: 'currency',
            currency: 'INR'
        });;
    }
    else return null
}

function getValueOfParam(value) {
    var url_string = window.location.href
    var url = new URL(url_string);
    var c = url.searchParams.get(value);
    return c;
}

function findPos(obj) {
    var curtop = 0;
    if (obj.offsetParent) {
        do {
            curtop += obj.offsetTop;
        } while (obj = obj.offsetParent);
        return [curtop];
    }
}

function objectValues(obj) {
    var res = [];
    for (var i in obj) {
        if (obj.hasOwnProperty(i)) {
            res.push(obj[i]);
        }
    }
    return res;
}
function objectKeys(obj) {
    var res = [];
    for (var i in obj) {
        if (obj.hasOwnProperty(i)) {
            res.push(i);
        }
    }
    return res;
}


function sticky_relocate() {
    var window_top = $(window).scrollTop();
    var div_top = $('#sticky-anchor').offset().top;
    if (window_top > div_top) {
        $('.sticky').addClass('stick');
        $('#sticky-anchor').height($('.sticky').outerHeight());
    } else {
        $('.sticky').removeClass('stick');
        $('#sticky-anchor').height(0);
    }
}


function sticky_relocate_filter() {
    var window_top = $(window).scrollTop();
    var div_top = $('#sticky-anchor').offset().top;
    if (window_top > div_top) {
        $('.sticky-filter').addClass('stick-filter');
        isScrolledIntoView($('#main-footer'));
    } else {
        $('.sticky-filter').removeClass('stick-filter');
    }
}

$(function () {
    $(window).scroll(function () {
        sticky_relocate_filter();
        sticky_relocate();
    });
});

function isScrolledIntoView(elem) {
    var $elem = $(elem);
    var $window = $(window);
    var docViewTop = $window.scrollTop();
    var docViewBottom = docViewTop + $window.height();
    var elemTop = $elem.offset().top;
    var elemBottom = elemTop + $elem.height();
    if (elemTop <= docViewBottom) {
        $('#filter-product-listing').height(window.innerHeight - (docViewBottom - elemTop + 120))
    }
    else {
        $('#filter-product-listing').height((window.innerHeight * 85) / 100);
    }
}

var dir = 1;
var MIN_TOP = 200;
var MAX_TOP = 350;

function autoscroll() {
    var window_top = $(window).scrollTop() + dir;
    if (window_top >= MAX_TOP) {
        window_top = MAX_TOP;
        dir = -1;
    } else if (window_top <= MIN_TOP) {
        window_top = MIN_TOP;
        dir = 1;
    }
    $(window).scrollTop(window_top);
    window.setTimeout(autoscroll, 100);
}

function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email.toLowerCase());
}
