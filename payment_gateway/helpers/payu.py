def get_request_url(production=False):
    if production:
        return u'https://secure.payu.in/_payment'
    return u'https://test.payu.in/_payment'


def required_config_keys():
    return [
        'MERCHANT_ID',
        'SALT'
    ]


def required_request_keys():
    return [
        'key',
        'txnid',
        'amount',
        'productinfo',
        'firstname',
        'email',
        'phone',
        'surl',
        'furl',
        'hash'
    ]


def required_response_keys():
    return ['mihpayid', 'status']


def request_keys():
    return [
        'key',
        'txnid',
        'amount',
        'productinfo',
        'firstname',
        'email',
        'phone',
        'lastname',
        'address1',
        'address2',
        'city',
        'state',
        'country',
        'zipcode',
        'udf1',
        'udf2',
        'udf3',
        'udf4',
        'udf5',
        'surl',
        'furl',
        'curl'
        'hash',
        'pg',
        'codurl',
        'drop_category',
        'enforce_paymethod',
        'custom_note',
        'note_category',
        'api_version',
        'shipping_firstname',
        'shipping_lastname',
        'shipping_address1',
        'shipping_address2',
        'shipping_city',
        'shipping_state',
        'shipping_country',
        'shipping_zipcode',
        'shipping_phone',
        'offer_key'
    ]


def response_keys():
    return [
        'mihpayid',
        'mode',
        'status',
        'key',
        'txnid',
        'amount',
        'discount',
        'offer',
        'productinfo',
        'firstname',
        'lastname',
        'address1',
        'address2',
        'city',
        'state',
        'country',
        'zipcode',
        'email',
        'phone',
        'udf1',
        'udf2',
        'udf3',
        'udf4',
        'udf5',
        'hash',
        'error',
        'bankcode',
        'pg_type',
        'bank_ref_num',
        'shipping_firstname',
        'shipping_lastname',
        'shipping_address1',
        'shipping_address2',
        'shipping_city',
        'shipping_state',
        'shipping_country',
        'shipping_zipcode',
        'shipping_phone',
        'unmappedstatus'
    ]


def keys_required_for_hash():
    return [
        'key',
        'txnid',
        'amount',
        'productinfo',
        'firstname',
        'email',
        'udf1',
        'udf2',
        'udf3',
        'udf4',
        'udf5'
    ]
