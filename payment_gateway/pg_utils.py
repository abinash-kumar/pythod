from motor_product import prod_utils as mpu
from health_product import prod_utils as hpu

HEALTH_INSURER_SLUG =  {
    'the-oriental-insurance-company-ltd': 'oriental'
}

def resolve_utils(transaction):
    if transaction.product_type == 'motor':
        return mpu
    elif transaction.product_type == 'health':
        return hpu
    else:
        return None


def process_payment_response(request, response, transaction):
    if transaction.product_type == 'motor':
        return mpu.process_payment_response(
            request,
            mpu.VEHICLE_TYPE_SLUG[transaction.vehicle_type],
            get_insurer_slug(transaction),
            response,
            transaction.transaction_id
        )
    elif transaction.product_type == 'health':
        return hpu.process_payment_response(
            transaction.slab.health_product.insurer.id,
            response,
            transaction
        )
    else:
        return None


def get_insurer_slug(transaction):
    if transaction.product_type == 'motor':
        return transaction.insurer.slug
    elif transaction.product_type == 'health':
        return HEALTH_INSURER_SLUG[transaction.slab.health_product.insurer.slug]
    else:
        return None


def get_error_url(transaction):
    if transaction.product_type == 'motor':
        vehicle_type = mpu.VEHICLE_TYPE_SLUG[transaction.vehicle_type]
        return '/motor/' + vehicle_type + '/product/failure/'
    elif transaction.product_type == 'health':
        return '/health-plan/payment/transaction/%s/failure/' % transaction.transaction_id
    else:
        return None

def todict(obj, classkey=None):
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = todict(v, classkey)
        return data
    elif hasattr(obj, "_ast"):
        return todict(obj._ast())
    elif hasattr(obj, "__iter__"):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, todict(value, classkey))
                    for key, value in obj.__dict__.iteritems()
                    if not callable(value) and not key.startswith('_')])
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj
