# coding: utf-8
from maxipago.managers.base import ManagerTransaction
from maxipago.requesters.pix import PixRequester
from maxipago.resources.pix import PixResource
from maxipago.utils import etree

class PixManager(ManagerTransaction):

    def add(self, **kwargs):
        fields = (
            ('referenceNum', {'translated_name': 'referenceNum'}),
            ('processorID', {'translated_name': 'processorID'}),
            ('chargeTotal', {'translated_name': 'payment/chargeTotal'}),
            ('expirationTime', {'translated_name': 'transactionDetail/payType/pix/expirationTime', 'required': False}),
        )
        requester = PixRequester(fields, kwargs)
        return self.send(command='sale', requester=requester, resource=PixResource)