# coding: utf-8
from io import BytesIO
from maxipago.utils import etree
from maxipago.resources.base import Resource
from maxipago.exceptions import PaymentException


class PixResource(Resource):

    def process(self):
        self.approved = False
        self.emv = None
        self.imagem_base64 = None
    
        tree = etree.parse(BytesIO(self.data))

        error_code = tree.find('errorCode')
        if error_code is not None and error_code.text != '0':
            error_message = tree.find('errorMsg').text
            raise PaymentException(message=error_message)

        fields = [
            ('transactionID', 'transaction_id'),
            ('authCode', 'auth_code'),
            ('orderID', 'order_id'),
            ('referenceNum', 'reference_num'),
            ('transactionTimestamp', 'transaction_timestamp'),
            ('responseCode', 'response_code'),
            ('responseMessage', 'response_message'),
            ('avsResponseCode', 'avs_response_code'),
            ('processorCode', 'processor_code'),
            ('processorMessage', 'processor_message'),
            ('processorName', 'processor_name'),
            ('errorMessage', 'error_message'),
            ('processorTransactionID', 'processor_transaction_id'),
            ('processorReferenceNumber', 'processor_reference_number'),
            ('onlineDebitURL', 'online_debit_url'),
            ('emv', 'emv'),
            ('imagem_base64', 'imagem_base64'),
        ]

        for f_name, f_translated in fields:
            field = tree.find(f_name)
            if field is not None:
                setattr(self, f_translated, field.text)

        if self.processor_code and self.processor_code.lower() == 'a':
            if self.emv or self.imagem_base64:
                self.approved = True