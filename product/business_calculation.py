from orders.models import Order, ShippingCharge
from product.models import Discount
from django.conf import settings
import logging


logging.basicConfig(filename=settings.LOG_DIR + "", level=logging.DEBUG)


class ProductOrderCalculation():
    """docstring for ProductOrderCalculation"""

    def __init__(self, arg):
        super(ProductOrderCalculation, self).__init__()
        self.arg = arg

    @staticmethod
    def calculate_price(product, quantity, coupon_discount=0):
        discount_obj = Discount.objects.get(product=product)
        if discount_obj.discount_type.lower() == "flat":
            price_after_discount = product.price - discount_obj.discount
        elif discount_obj.discount_type.lower() == "percentage":
            price_after_discount = product.price - \
                product.price * (discount_obj.discount / 100)
        else:
            price_after_discount = product.price
        price_after_coupon_discount = (
            price_after_discount * quantity) - coupon_discount
        return price_after_coupon_discount

    @staticmethod
    def calculate_individual_shipping_charge(order_list):
        seller_wise_products_cost = {}
        seller_wise_products_count = {}
        seller_id_list = []
        for order in order_list:
            seller_id = order['seller_id']
            if seller_id in seller_id_list:
                seller_wise_products_cost[seller_id] = seller_wise_products_cost[
                    seller_id] + order['price_without_shipping_charge']
                seller_wise_products_count[seller_id] = seller_wise_products_count[seller_id] + 1
                logging.info('seller id exist')
                logging.info("seller_wise_products_cost --> " +
                             str(seller_wise_products_cost))
                logging.info("seller_wise_products_count --> " +
                             str(seller_wise_products_count))
            else:
                seller_wise_products_cost[seller_id] = order['price_without_shipping_charge']
                seller_wise_products_count[seller_id] = 1
                logging.info("seller_wise_products_cost --> " +
                             str(seller_wise_products_cost))
                logging.info("seller_wise_products_count --> " +
                             str(seller_wise_products_count))
                seller_id_list.append(seller_id)

            shipping_charge_obj = ShippingCharge.objects.get(seller=seller_id)
            logging.info("=====condition here====")
            logging.info(seller_wise_products_cost[seller_id])
            logging.info(shipping_charge_obj.free_shipping_minimum_amount)
            logging.info(seller_wise_products_cost[
                         seller_id] > shipping_charge_obj.free_shipping_minimum_amount)

        for order in order_list:
            seller_id = order['seller_id']
            if seller_id in seller_id_list:
                shipping_charge_obj = ShippingCharge.objects.get(seller=seller_id)
                if seller_wise_products_cost[seller_id] > shipping_charge_obj.free_shipping_minimum_amount:
                    order['shipping_charge'] = 0
                else:
                    order['shipping_charge'] = shipping_charge_obj.shipping_charge
                seller_id_list.remove(seller_id)
            else:
                order['shipping_charge'] = 0
            order['price'] = int(order['price_without_shipping_charge'] + order['shipping_charge'])
            order_id = order.get('order_id', None)
            if order_id:
                order_obj = Order.objects.get(id=order_id)
                order_obj.shipping_charge = order['shipping_charge']
                order_obj.save()
        return order_list

    @staticmethod
    def calculate_unit_price(product):
        discount_obj = Discount.objects.get(product=product)
        if discount_obj.discount_type.lower() == "flat":
            price_after_discount = product.price - discount_obj.discount
        elif discount_obj.discount_type.lower() == "percentage":
            price_after_discount = product.price - \
                product.price * (discount_obj.discount / 100)
        else:
            price_after_discount = product.price
        return int(price_after_discount)

    @staticmethod
    def calculate_tax(price):
        service_tax = 0
        return price * service_tax / 100

    @staticmethod
    def calculate_shipping_charge(order_list, total):
        SHIPPING_CHARGE = 0
        MINIMUM_AMOUNT_FOR_NO_SHIPPING_CHARGE = 500
        if total < 500:
            return SHIPPING_CHARGE
        else:
            return 0

    @staticmethod
    def calculate_coupon_discount(order_list, coupon_code=None):
        return 0

    @staticmethod
    def calculate_tax_in_transaction(order_list):
        total = 0
        for order in orderlist:
            each_order_amount = ((order.price - order.discount)
                                 * order.quantity) - coupon_discount + shipping_charge
            total = total + each_order_amount

        total_with_shipping = total + \
            self.calculate_shipping_charge(order_list, total)
        final_amount = total_with_shipping - \
            self.calculate_coupon_discount(order_list, coupon_code)
        return self.calculate_tax(final_amount)

    @staticmethod
    def calculate_order_subtotal(orderlist):
        total = 0
        total_shipping_charge = 0
        for order in orderlist:
            each_order_amount = order['price_without_shipping_charge'] - order['coupon_discount']
            total_shipping_charge = total_shipping_charge + order['shipping_charge']
            total = total + each_order_amount
        return total, total_shipping_charge
        # total_with_shipping = total + self.calculate_shipping_charge(order_list,total)
        # final_amount = total_with_shipping - self.calculate_coupon_discount(order_list,coupon_code)
        # final_transaction_amount = final_amount + self.calculate_tax(final_amount)
        # return final_transaction_amount

    @staticmethod
    def calculate_cod_charges(orderlist):
        COD_MINIMUM_AMMOUNT = 10000
        COD_CHARGE = 80
        total = 0
        sellers_ammount = {}
        all_sellers = []
        for o in orderlist:
            all_sellers.append(o.product_varient.sellers.all())
        common_seller = list(set(all_sellers[0]).intersection(*all_sellers))
        if len(common_seller) > 0:
            sellers_ammount.update({common_seller[0].id: 0})
        for order in orderlist:
            product_sellers = order.product_varient.sellers.all()
            for product_seller in product_sellers:
                if product_seller.id in sellers_ammount.keys():
                    break

            temp_amt = sellers_ammount.get(product_seller.id, 0)
            sellers_ammount.update(
                {product_seller.id: temp_amt + order.product_id.price})
        for k in sellers_ammount.keys():
            if sellers_ammount.get(k, 0) < COD_MINIMUM_AMMOUNT:
                total = total + COD_CHARGE
        return total
