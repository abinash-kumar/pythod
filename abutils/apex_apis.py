import requests
from django.conf import settings
import json


class APEXApiIntegration():
    """docstring for APEXApiIntegration"""

    ROUTE = {
        'PINCODE_CHECK': 'account/getapi/pincodecheck',
        'CREATE_ADDRESS': 'account/getapi/createaddress',
        'ADDRESS_STATUS': 'account/getapi/addressstatus',
        'ADDRESS_STATUS_FOR': 'account/getapi/addressavailable',
        'PACKAGE_AVAILBILITY': 'account/getapi/packages',
        'SERVICE_AVAILBILITY': 'account/getapi/partners',
        'CREATE_ORDER': 'account/getapi/ordercreate',
        'TRACK_ORDER': 'account/getapi/tracking',
        'BILLING': 'account/getbillingapi/billingdetails',
        'BILL_TOTAL': 'account/getbillingapi/billingnumberdetails',
        'COD_STATUS': 'account/getbillingapi/aipexcod',
        'BILL_COD_STATUS': 'account/getbillingapi/billingcod',
    }

    CHECK_ADDRESS_STATUS_FOR = {
        'NOT_APPROVED': 0,
        'APPROVED': 1,
        'ALL': 2
    }

    ORDER_DATA_KEYS = [
        'from_address_id',
        'to_pincode',
        'to_address',
        'to_address2',
        'to_address3',
        'customer_firstname',
        'customer_lastname',
        'customer_email',
        'customer_contact_no',
        'ship_date',
        'company_name',
        'insurance',
        'no_of_packages',
        'package_type',
        'package_id',
        'total_invoice_value',
        'shipping_method',
        'shipping_type',
        'payment_mode',
        'package_name',
        'partner_id',
        'package_weight1',
        'package_height1',
        'package_length1',
        'package_width1',
        'aipex_ref_number'
    ]

    def create_order_dict(self, order_list):
        order_dict = {}
        for i in range(len(order_list)):
            order_dict.update({self.ORDER_DATA_KEYS[i]: order_list[i]})
        return order_dict

    def get_uri(self, route):
        if settings.DEBUG:
            uri = settings.APEX_PRODUCTION_URL + '?route=' + self.ROUTE[route]
        else:
            uri = settings.APEX_PRODUCTION_URL + '?route=' + self.ROUTE[route]
        return uri

    def get_response_from_api_request(self, data, route):
        uri = self.get_uri(route)
        post_data = requests.post(uri, data=data)
        return json.loads(post_data.content), post_data.request.__dict__

    def pincode_check(self, pincode):
        data = {
            'pincode': pincode,
        }
        response_data, post_data = self.get_response_from_api_request(data, 'PINCODE_CHECK')
        return response_data

    def create_address(self, first_name, last_name, address_1, address_2, pincode, mobile):
        data = {
            'username': settings.APEX_USERNAME,
            'pass': settings.APEX_PASSWORD,
            'token': settings.APEX_TOKEN,
            'firstname': first_name,
            'lastname': last_name,
            'address_1': address_1,
            'address_2': address_2,
            'postcode': pincode,
            'telephone': mobile,
        }
        response_data, post_data = self.get_response_from_api_request(data, 'CREATE_ADDRESS')
        return response_data, post_data

    def get_all_address_status(self):
        data = {
            'username': settings.APEX_USERNAME,
            'pass': settings.APEX_PASSWORD,
            'token': settings.APEX_TOKEN,
        }
        response_data, post_data = self.get_response_from_api_request(data, 'ADDRESS_STATUS')
        return response_data, post_data

    def get_address_status(self, status):
        status = self.CHECK_ADDRESS_STATUS_FOR[status]
        data = {
            'username': settings.APEX_USERNAME,
            'pass': settings.APEX_PASSWORD,
            'token': settings.APEX_TOKEN,
            'status': status,
        }
        response_data, post_data = self.get_response_from_api_request(data, 'ADDRESS_STATUS_FOR')
        return response_data, post_data

    def get_package_availability(self, status):
        response_data, post_data = self.get_response_from_api_request({}, 'PACKAGE_AVAILBILITY')
        return response_data, post_data

    def is_service_available(self,
                             pickup_pincode,
                             delivery_pincode,
                             payment_mode,
                             weight,
                             servicetype,
                             shipping_type,
                             shipping_method,
                             length,
                             width,
                             height,
                             no_of_packages):
        data = {
            'username': settings.APEX_USERNAME,
            'pass': settings.APEX_PASSWORD,
            'token': settings.APEX_TOKEN,
            'pickup_pincode': pickup_pincode,
            'delivery_pincode': delivery_pincode,
            'payment_mode': payment_mode,
            'weight': weight,
            'servicetype': servicetype,
            'shipping_type': shipping_type,
            'shipping_method': shipping_method,
            'length': length,
            'width': width,
            'height': height,
            'no_of_packages': no_of_packages,
        }
        response_data, post_data = self.get_response_from_api_request(data, 'SERVICE_AVAILBILITY')
        return response_data, post_data

    def create_order(self, order_data):
        data = {
            'username': settings.APEX_USERNAME,
            'pass': settings.APEX_PASSWORD,
            'token': settings.APEX_TOKEN,
        }
        data.update({self.ORDER_DATA_KEYS[i]: order_data[i] for i in range(len(self.ORDER_DATA_KEYS))})
        print data
        response_data, post_data = self.get_response_from_api_request(data, 'CREATE_ORDER')
        return response_data, post_data

    def track_order(self, aipexnumber):
        data = {
            'aipexnumber': aipexnumber,
        }
        response_data, post_data = self.get_response_from_api_request(data, 'TRACK_ORDER')
        return response_data, post_data

    # Billing APIS

    def shipping_cost(self, aipexnumber):
        data = {
            'aipexnumber': aipexnumber,
        }
        response_data, post_data = self.get_response_from_api_request(data, 'BILLING')
        return response_data, post_data

    def total_bill(self, billingnumber):
        data = {
            'billingnumber': billingnumber,
        }
        response_data, post_data = self.get_response_from_api_request(data, 'BILL_TOTAL')
        return response_data, post_data

    def COD_status(self, aipexnumber):
        data = {
            'aipexnumber': aipexnumber,
        }
        response_data, post_data = self.get_response_from_api_request(data, 'COD_STATUS')
        return response_data, post_data

    def bill_COD_status(self, billingnumber):
        data = {
            'billingnumber': billingnumber,
        }
        response_data, post_data = self.get_response_from_api_request(data, 'BILL_COD_STATUS')
        return response_data, post_data
