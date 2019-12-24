import hashlib
import hmac
import json
import logging

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from drchrono.forms.webhook import get_form_class_for_event

logger = logging.getLogger()


@method_decorator(csrf_exempt, name='dispatch')
class WebhookView(View):
    def get(self, request, *args, **kwargs):
        secret_token = hmac.new(
            settings.WEBHOOK_SECRET_TOKEN, request.GET['msg'], hashlib.sha256
        ).hexdigest()
        return JsonResponse({'secret_token': secret_token})

    def post(self, request, *args, **kwargs):
        secret_token = request.META.get('HTTP_X_DRCHRONO_SIGNATURE', '')
        event = request.META.get('HTTP_X_DRCHRONO_EVENT')
        if secret_token != settings.WEBHOOK_SECRET_TOKEN:
            logger.error('webook secret is wrong')
            return HttpResponse(status=403)
        try:
            data = json.loads(request.body)
        except ValueError:
            logger.error('webook payload is not a valid json')
            return HttpResponse(status=400)

        form_class = get_form_class_for_event(event)
        if form_class is None:
            logger.info('webhook event `{}` is not handled'.format(event))
            return HttpResponse(status=200)

        form = form_class(data['object'])
        if not form.is_valid():
            logger.error('paylod data is not valid')
            return HttpResponse(status=400)

        form.save()
        return HttpResponse()
