from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_json_api.views import ReadOnlyModelViewSet
from wallet_api.apicore.models import Wallet, Transaction
from wallet_api.apicore.serializers import WalletSerializer, TransactionSerializer

def ping(HttpRequest):
    return HttpResponse(content='200 OK!', status=200)


class WalletViewSet(ReadOnlyModelViewSet):
    http_method_names = ['get']
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    ordering_fields = ('id',)


class TransactionViewSet(ReadOnlyModelViewSet):
    http_method_names = ['get']
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    ordering_fields = ('id',)
    filterset_fields = {
        'wallet_id': ['exact'],
        'amount': ['gt', 'gte', 'lt', 'lte'],
    }

    @action(detail=False, url_path='by-txid/(?P<txid>\w+)', url_name='by-trxid')
    def by_trxid(self, request, txid):
        trx = Transaction.objects.get(txid=txid)
        serializer = self.get_serializer(trx)
        return Response(serializer.data)
