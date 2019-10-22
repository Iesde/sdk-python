# coding: utf-8
from maxipago.managers.base import ManagerTransaction, ManagerApi
from maxipago.requesters.payment import PaymentRecurringRequester
from maxipago.resources.payment import PaymentResource
from maxipago.resources.recurring import CancelResource, EditResource

class PaymentRecurringManager(ManagerTransaction):

    def add(self, **kwargs):
        fields = (
            ('processor_id', {'translated_name': 'processorID'}),
            ('reference_num', {'translated_name': 'referenceNum'}),
            ('ip_address', {'translated_name': 'ipAddress', 'required': False}),

            ('card_number', {'translated_name': 'transactionDetail/payType/creditCard/number'}),
            ('card_expiration_month', {'translated_name': 'transactionDetail/payType/creditCard/expMonth'}),
            ('card_expiration_year', {'translated_name': 'transactionDetail/payType/creditCard/expYear'}),
            ('card_cvv', {'translated_name': 'transactionDetail/payType/creditCard/cvvNumber', 'required': False}),

            ('charge_total', {'translated_name': 'payment/chargeTotal'}),
            ('currency_code', {'translated_name': 'payment/currencyCode', 'required': True}),

            ('recurring_action', {'translated_name': 'recurring/action', 'default': 'new'}),
            ('recurring_start', {'translated_name': 'recurring/startDate', 'required': False}),
            ('recurring_last', {'translated_name': 'recurring/lastDate', 'required': False}),
            ('recurring_frequency', {'translated_name': 'recurring/frequency'}),
            ('recurring_period', {'translated_name': 'recurring/period'}),
            ('recurring_first_amount', {'translated_name': 'recurring/firstAmount', 'required': False}),
            ('recurring_last_amount', {'translated_name': 'recurring/lastAmount', 'required': False}),
            ('recurring_installments', {'translated_name': 'recurring/installments'}),
            ('recurring_failure_threshold', {'translated_name': 'recurring/failureThreshold', 'required': False}),
        )
        
        requester = PaymentRecurringRequester(fields, kwargs)       
        return self.send(command='recurringPayment', requester=requester, resource=PaymentResource)


    def delete(self, **kwargs):
        fields = (
            ('order_id', {'translated_name': 'orderID'}),
        )

        requester = PaymentRecurringRequester(fields, kwargs)
        
        manager = ManagerApi(maxid=self.maxid, api_key=self.api_key, api_version=self.api_version, sandbox=self.sandbox)
        return manager.send(command='cancel-recurring', requester=requester, resource=CancelResource)


class PaymentRecurringManagerApi(ManagerApi):

    def edit(self, **kwargs):
        
        fields = (
            ('order_id', {'translated_name': 'orderID'}),

            ('card_number', {'translated_name': 'paymentInfo/cardInfo/creditCardNumber', 'required': False}),
            ('card_expiration_month', {'translated_name': 'paymentInfo/cardInfo/expirationMonth', 'required': False}),
            ('card_expiration_year', {'translated_name': 'paymentInfo/cardInfo/expirationYear', 'required': False}),
            ('card_soft_description', {'translated_name': 'paymentInfo/cardInfo/softDescriptor', 'required': False}),

            ('charge_total', {'translated_name': 'paymentInfo/chargeTotal'}),

            ('processor_id', {'translated_name': 'recurring/processorID', 'Required': False}),
            ('recurring_action', {'translated_name': 'recurring/action', 'default': 'enabled', 'required': True}),
            ('recurring_installments', {'translated_name': 'recurring/installments'}),
            ('recurring_next_date', {'translated_name': 'recurring/nextFireDate', 'required': False}),
            ('recurring_day', {'translated_name': 'recurring/fireDay', 'required': False}),
            ('recurring_period', {'translated_name': 'recurring/period', 'required': False}),
            ('recurring_last_date', {'translated_name': 'recurring/lastDate', 'required': False}),
            ('recurring_last_amount', {'translated_name': 'recurring/lastAmount', 'required': False}),
            
            ('billing_name', {'translated_name': 'billingInfo/name', 'required': False}),
            ('billing_address', {'translated_name': 'billingInfo/address1', 'required': False}),
            ('billing_address2', {'translated_name': 'billingInfo/address2', 'required': False}),
            ('billing_city', {'translated_name': 'billingInfo/city', 'required': False}),
            ('billing_postalcode', {'translated_name': 'billingInfo/zip', 'required': False}),
            ('billing_country', {'translated_name': 'billingInfo/country', 'required': False}),
            ('billing_email', {'translated_name': 'billingInfo/email', 'required': False}),
            ('billing_phone', {'translated_name': 'billingInfo/phone', 'required': False}),

            ('shipping_name', {'translated_name': 'shippingInfo/name', 'required': False}),
            ('shipping_address', {'translated_name': 'shippingInfo/address1', 'required': False}),
            ('shipping_address2', {'translated_name': 'shippingInfo/address2', 'required': False}),
            ('shipping_city', {'translated_name': 'shippingInfo/city', 'required': False}),
            ('shipping_postalcode', {'translated_name': 'shippingInfo/zip', 'required': False}),
            ('shipping_country', {'translated_name': 'shippingInfo/country', 'required': False}),
            ('shipping_email', {'translated_name': 'shippingInfo/email', 'required': False}),
            ('shipping_phone', {'translated_name': 'shippingInfo/phone', 'required': False}),
        )
        
        requester = PaymentRecurringRequester(fields, kwargs)
        return self.send(command='modify-recurring', requester=requester, resource=EditResource)
