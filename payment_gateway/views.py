"""Payment-gateway controllers"""
from __future__ import absolute_import
import json
import traceback
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from payment_gateway import gateways
from utils import payment_logger
from payment_gateway import pg_utils
from payment_gateway.models import Payment


GATEWAY = {
    'billdesk': gateways.billdesk.Billdesk,
    'payu': gateways.payu.Payu
}


@never_cache
def response(request, gateway):
    request_data = request.POST.dict() or request.GET.dict()
    payment_logger.info(json.dumps({
        'type': 'response',
        'gateway': gateway,
        'medium': 'browser',
        'data': request_data
    }))
    # try:
    #     pg = PaymentGateway.objects.get(slug=gateway)
    # except PaymentGateway.DoesNotExist:
    #     payment_logger.info(json.dumps({
    #         'type': 'response',
    #         'gateway': gateway,
    #         'medium': 'browser',
    #         'data': request_data,
    #         'message': 'INVALID GATEWAY'
    #     }))
    if gateway in GATEWAY:
        pg = GATEWAY[gateway]
        if gateway == 'billdesk':
            payment_id = pg.parse_response(request_data)['CustomerID']
        elif gateway == 'payu':
            payment_id = request_data['txnid']
        payment = Payment.objects.get(payment_id=payment_id)
        transaction = payment.transaction
        payment.response_set.create(data=request_data)
        insurer_slug = pg_utils.get_insurer_slug(transaction)
        config = pg.get_config(insurer_slug)
        pg_obj = pg(request_data, config)

        if pg_obj.validate_checksum():
            if payment.raw.get('s2s_status'):
                is_payment_success = payment.raw['s2s_status']['is_payment_success']
            else:
                # billdesk.get_s2s_query_response()
                if gateway == 'billdesk':
                    response = pg_obj.get_response_data()
                elif gateway == 'payu':
                    response = request_data
                try:
                    is_payment_success, transaction = pg_utils.process_payment_response(
                        request, response, transaction)
                except:
                    stacktrace = traceback.format_exc()
                    payment_logger.info(stacktrace)
                    return HttpResponseRedirect(pg_utils.get_error_url(transaction))

            return HttpResponseRedirect(
                transaction.payment_url(is_payment_success=is_payment_success)
            )

        else:
            payment_logger.info(json.dumps({
                'type': 'response',
                'gateway': gateway,
                'medium': 'browser',
                'transaction': transaction.transaction_id,
                'data': request_data,
                'message': 'INVALID CHECKSUM'
            }))
            return HttpResponseRedirect(pg_utils.get_error_url(transaction))
    payment_logger.info(json.dumps({
        'type': 'response',
        'gateway': gateway,
        'medium': 'browser',
        'data': request_data,
        'message': 'INVALID GATEWAY'
    }))
    return HttpResponse(json.dumps({'success': False, 'message': 'INVALID_GATEWAY'}), status=400)


@never_cache
def s2s_response(request, gateway):
    request_data = request.POST.dict() or request.GET.dict()
    payment_logger.info(json.dumps({
        'type': 'response',
        'gateway': gateway,
        'medium': 'server-to-server',
        'data': request_data,
        'body': request.body
    }))

    if gateway in GATEWAY:
        pg = GATEWAY[gateway]
        if gateway == 'billdesk':
            try:
                request_data['msg'] = request_data['msg'].rstrip('\n')
                payment_id = pg.parse_response(request_data)['CustomerID']
            except KeyError:
                return HttpResponse(json.dumps({'success': False, 'message': 'INVALID_DATA'}), status=400)
        elif gateway == 'payu':
            payment_id = request_data['txnid']
        payment = Payment.objects.get(payment_id=payment_id)
        transaction = payment.transaction
        payment.response_set.create(data=request_data, type='S2S')
        insurer_slug = pg_utils.get_insurer_slug(transaction)
        config = pg.get_config(insurer_slug)
        pg_obj = pg(request_data, config)
        if pg_obj.validate_checksum():
            if gateway == 'billdesk':
                response = pg_obj.get_response_data()
            elif gateway == 'payu':
                response = request_data
            if transaction.status == 'COMPLETED':
                return HttpResponse(status=208)
            try:
                is_payment_success, transaction = pg_utils.process_payment_response(
                    request, response, transaction
                )
                payment.raw['s2s_status'] = {'is_payment_success': is_payment_success}
                payment.save(update_fields=['raw'])
            except:
                stacktrace = traceback.format_exc()
                payment_logger.error(stacktrace)
            finally:
                return HttpResponse(status=200)
        else:
            payment_logger.info(json.dumps({
                'type': 'response',
                'gateway': gateway,
                'medium': 'server-to-server',
                'transaction': transaction.transaction_id,
                'data': request_data,
                'message': 'INVALID CHECKSUM'
            }))
            return HttpResponse(status=401)
