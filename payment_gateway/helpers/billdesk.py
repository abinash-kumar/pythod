def get_request_url(production=False):
    if production:
        return u'https://pgi.billdesk.com/pgidsk/PGIMerchantPayment'
    return u'https://pgi.billdesk.com/pgidsk/PGIMerchantPayment'


def required_config_keys():
    return [
        'MERCHANT_ID',
        'SECURITY_ID',
        'CHECKSUM_KEY'
    ]


def required_request_keys():
    return [
        'transaction',
        'reference_id',
        'amount',
        'email',
        'phone'
    ]


# Only one key that contains actual data
def required_response_keys():
    return [
        'msg'
    ]


def request_keys():
    return [
        'MerchantID',
        'CustomerID',
        'NA',
        'TxnAmount',
        'NA',
        'NA',
        'NA',
        'CurrencyType',
        'NA',
        'TypeField1',
        'SecurityID',
        'NA',
        'NA',
        'TypeField2',
        'AdditionalInfo1',
        'AdditionalInfo2',
        'AdditionalInfo3',
        'AdditionalInfo4',
        'AdditionalInfo5',
        'AdditionalInfo6',
        'AdditionalInfo7',
        'RU',
        'CheckSum'
    ]


def response_keys():
    return [
        'MerchantID',
        'CustomerID',
        'TxnReferenceNo',
        'BankReferenceNo',
        'TxnAmount',
        'BankID',
        'BankMerchantID',
        'TxnType',
        'CurrencyName',
        'ItemCode',
        'SecurityType',
        'SecurityID',
        'SecurityPassword',
        'TxnDate',
        'AuthStatus',
        'SettlementType',
        'AdditionalInfo1',
        'AdditionalInfo2',
        'AdditionalInfo3',
        'AdditionalInfo4',
        'AdditionalInfo5',
        'AdditionalInfo6',
        'AdditionalInfo7',
        'ErrorStatus',
        'ErrorDescription',
        'CheckSum'
    ]


def response_data_keys():
    return {
        'TxnReferenceNo': 'payment_id',
        'TxnAmount': 'payment_amount',
        'TxnDate': 'payment_date',
        'AuthStatus': 'status',
        'CustomerID': 'transaction_id',
        'AdditionalInfo1': 'reference_id',
        'ErrorStatus': 'status_txt',
        'ErrorDescription': 'status_desc'
    }


def response_status():
    return {
        '0300': {
            'payment_status': 'Success',
            'transaction_status': 'Successful Transaction'},
        '0399': {
            'payment_status': 'Invalid Authentication at Bank',
            'transaction_status': 'Failed Transaction'},
        'NA': {
            'payment_status': 'Invalid Input in the Request Message',
            'transaction_status': 'Cancel Transaction'},
        '0002': {
            'payment_status': 'Unable to ascertain the status of the txn.',
            'transaction_status': 'Pending Transaction'},
        '0001': {
            'payment_status': 'Error at BillDesk',
            'transaction_status': 'Cancel Transaction'},
        '0000': {
            'payment_status': 'Invalid Request',
            'transaction_status': 'Invalid Transaction'
        }
    }
