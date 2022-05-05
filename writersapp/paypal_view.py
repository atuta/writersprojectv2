from decimal import Decimal

from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.views.generic import TemplateView

from writersapp.models import PaymentTransactions
from writersproject import settings


def process_payment(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(PaymentTransactions, p_id='10')
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '20',
        'item_name': 'Order {}'.format(order.p_id),
        'invoice': str(order.p_id),
        'currency_code': 'USD',
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'paypal_form.html', {'order': order, 'form': form})
