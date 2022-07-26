# coding: utf-8
from .base import ManagerTransaction
from maxipago.requesters.pix import PixRequester


class PixManager(ManagerTransaction):

    def add(self, **kwargs):
        fields = (
            ('referenceNum', {'translated_name': 'referenceNum'}),
            ('processorID', {'translated_name': 'processorID'}),
            ('chargeTotal', {'translated_name': 'payment/chargeTotal'}),
            ('expirationTime', {'translated_name': 'transactionDetail/payType/pix/expirationTime', 'required': False}),
        )
        requester = PixRequester(fields, kwargs)
        return self.send(command='sale', requester=requester)

    def get(self, **kwargs):
        fields = (
            # ('transaction_id', {'translated_name': 'transactionID'}),
            ('order_id', {'translated_name': 'orderID'}),
            # ('referenceNum', {'translated_name': 'referenceNum'}),
        )
        requester = PixRequester(fields, kwargs)
        return self.send(command='authente', requester=requester)