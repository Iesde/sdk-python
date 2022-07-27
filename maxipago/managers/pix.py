# coding: utf-8
from .base import ManagerTransaction
from maxipago.requesters.pix import PixRequester
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
        return self.send(command='sale', requester=requester)

    def xml_to_dict(self, content):
        xmlDict = {}
        tree = etree.fromstring(content)
        for child in tree.iter('*'):
            childrens = child.getchildren()
            for chil in childrens:
                xmlDict[chil.tag] = chil.text

        return xmlDict