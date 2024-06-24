# coding: utf-8
import os
import unittest
from datetime import date
from maxipago import Maxipago, exceptions
from maxipago.utils import payment_processors, etree
from random import randint
from time import sleep


MAXIPAGO_ID = os.getenv('MAXIPAGO_ID')
MAXIPAGO_API_KEY = os.getenv('MAXIPAGO_API_KEY')

class MaxipagoTestCase(unittest.TestCase):

    def setUp(self):
        self.maxipago = Maxipago(MAXIPAGO_ID, MAXIPAGO_API_KEY, sandbox=True)

    def test_add_customer(self):
        CUSTOMER_ID = randint(1, 100000)

        response = self.maxipago.customer.add(
            customer_id=CUSTOMER_ID,
            first_name='Fulano',
            last_name='de Tal',
        )

        self.assertTrue(getattr(response, 'id', False))

    def test_delete_customer(self):
        CUSTOMER_ID = randint(1, 100000)

        # creating customer with random id.
        response = self.maxipago.customer.add(
            customer_id=CUSTOMER_ID,
            first_name='Fulano',
            last_name='de Tal',
        )

        self.assertTrue(hasattr(response, 'id'))

        maxipago_customer_id = response.id

        response = self.maxipago.customer.delete(
            id=maxipago_customer_id,
        )

    def test_update_customer(self):
        CUSTOMER_ID = randint(1, 100000)

        # creating customer with random id.
        response = self.maxipago.customer.add(
            customer_id=CUSTOMER_ID,
            first_name=u'Fulano',
            last_name=u'de Tal',
        )

        self.assertTrue(hasattr(response, 'id'))

        maxipago_customer_id = response.id

        response = self.maxipago.customer.update(
            id=maxipago_customer_id,
            customer_id=CUSTOMER_ID,
            first_name=u'Antonio',
        )

    def test_add_card(self):
        CUSTOMER_ID = randint(1, 100000)

        response = self.maxipago.customer.add(
            customer_id=CUSTOMER_ID,
            first_name=u'Fulano',
            last_name=u'de Tal',
        )

        self.assertTrue(hasattr(response, 'id'))

        maxipago_customer_id = response.id

        response = self.maxipago.card.add(
            customer_id=maxipago_customer_id,
            number=u'4111111111111111',
            expiration_month=u'02',
            expiration_year=date.today().year + 3,
            billing_name=u'Fulano de Tal',
            billing_address1=u'Rua das Alamedas, 123',
            billing_city=u'Rio de Janeiro',
            billing_state=u'RJ',
            billing_zip=u'20123456',
            billing_country=u'BR',
            billing_phone=u'552140634666',
            billing_email=u'fulano@detal.com',
        )

        self.assertTrue(getattr(response, 'token', False))

    def test_delete_card(self):
        CUSTOMER_ID = randint(1, 100000)

        customer_response = self.maxipago.customer.add(
            customer_id=CUSTOMER_ID,
            first_name=u'Fulano',
            last_name=u'de Tal',
        )

        self.assertTrue(hasattr(customer_response, 'id'))

        maxipago_customer_id = customer_response.id

        card_response = self.maxipago.card.add(
            customer_id=maxipago_customer_id,
            number=u'4111111111111111',
            expiration_month=u'02',
            expiration_year=date.today().year + 3,
            billing_name=u'Fulano de Tal',
            billing_address1=u'Rua das Alamedas, 123',
            billing_city=u'Rio de Janeiro',
            billing_state=u'RJ',
            billing_zip=u'20345678',
            billing_country=u'RJ',
            billing_phone=u'552140634666',
            billing_email=u'fulano@detal.com',
        )

        self.assertTrue(getattr(card_response, 'token', False))

        token = card_response.token

        response = self.maxipago.card.delete(
            customer_id=maxipago_customer_id,
            token=token,
        )

        self.assertTrue(getattr(response, 'success', False))

    def test_payment_authorize(self):
        REFERENCE = randint(1, 100000)

        response = self.maxipago.payment.authorize(
            processor_id=payment_processors.TEST,
            reference_num=REFERENCE,

            billing_name=u'Fulano de Tal',
            billing_address1=u'Rua das Alamedas, 123',
            billing_city=u'Rio de Janeiro',
            billing_state=u'RJ',
            billing_zip=u'20345678',
            billing_country=u'RJ',
            billing_phone=u'552140634666',
            billing_email=u'fulano@detal.com',

            card_number='4111111111111111',
            card_expiration_month=u'02',
            card_expiration_year=date.today().year + 3,
            card_cvv='123',

            charge_total='100.00',
        )

        self.assertTrue(response.authorized)
        self.assertFalse(response.captured)

    def test_payment_direct(self):
        REFERENCE = randint(1, 100000)

        response = self.maxipago.payment.direct(
            processor_id=payment_processors.TEST,
            reference_num=REFERENCE,

            billing_name=u'Fulano de Tal',
            billing_address1=u'Rua das Alamedas, 123',
            billing_city=u'Rio de Janeiro',
            billing_state=u'RJ',
            billing_zip=u'20345678',
            billing_country=u'RJ',
            billing_phone=u'552140634666',
            billing_email=u'fulano@detal.com',

            card_number='4111111111111111',
            card_expiration_month=u'02',
            card_expiration_year=date.today().year + 3,
            card_cvv='123',

            charge_total='100.00',
        )

        self.assertTrue(response.authorized)
        self.assertTrue(response.captured)

    def test_payment_direct_declined(self):
        REFERENCE = randint(1, 100000)

        response = self.maxipago.payment.direct(
            processor_id=payment_processors.TEST,
            reference_num=REFERENCE,

            billing_name=u'Fulano de Tal',
            billing_address1=u'Rua das Alamedas, 123',
            billing_city=u'Rio de Janeiro',
            billing_state=u'RJ',
            billing_zip=u'20345678',
            billing_country=u'RJ',
            billing_phone=u'552140634666',
            billing_email=u'fulano@detal.com',

            card_number='4111111111111111',
            card_expiration_month=u'02',
            card_expiration_year=date.today().year + 3,
            card_cvv='123',

            charge_total='100.01',
        )

        self.assertFalse(response.authorized)
        self.assertFalse(response.captured)

    def test_payment_direct_with_token(self):
        CUSTOMER_ID = randint(1, 100000)

        response = self.maxipago.customer.add(
            customer_id=CUSTOMER_ID,
            first_name=u'Fulano',
            last_name=u'de Tal',
        )

        self.assertTrue(hasattr(response, 'id'))

        maxipago_customer_id = response.id

        response = self.maxipago.card.add(
            customer_id=maxipago_customer_id,
            number=u'4111111111111111',
            expiration_month=u'02',
            expiration_year=date.today().year + 3,
            billing_name=u'Fulano de Tal',
            billing_address1=u'Rua das Alamedas, 123',
            billing_city=u'Rio de Janeiro',
            billing_state=u'RJ',
            billing_zip=u'20123456',
            billing_country=u'BR',
            billing_phone=u'552140634666',
            billing_email=u'fulano@detal.com',
        )

        self.assertTrue(getattr(response, 'token', False))
        REFERENCE = randint(1, 100000)

        response = self.maxipago.payment.direct(
            processor_id=payment_processors.TEST,
            reference_num=REFERENCE,

            customer_id=maxipago_customer_id,
            token=response.token,

            charge_total='100.00',
        )

        self.assertTrue(response.authorized)
        self.assertTrue(response.captured)

    def test_payment_direct_with_token_decline(self):
        CUSTOMER_ID = randint(1, 100000)

        response = self.maxipago.customer.add(
            customer_id=CUSTOMER_ID,
            first_name=u'Fulano',
            last_name=u'de Tal',
        )

        self.assertTrue(hasattr(response, 'id'))

        maxipago_customer_id = response.id

        response = self.maxipago.card.add(
            customer_id=maxipago_customer_id,
            number=u'4111111111111111',
            expiration_month=u'02',
            expiration_year=date.today().year + 3,
            billing_name=u'Fulano de Tal',
            billing_address1=u'Rua das Alamedas, 123',
            billing_city=u'Rio de Janeiro',
            billing_state=u'RJ',
            billing_zip=u'20123456',
            billing_country=u'BR',
            billing_phone=u'552140634666',
            billing_email=u'fulano@detal.com',
        )

        self.assertTrue(getattr(response, 'token', False))
        REFERENCE = randint(1, 100000)

        response = self.maxipago.payment.direct(
            processor_id=payment_processors.TEST,
            reference_num=REFERENCE,

            customer_id=maxipago_customer_id,
            token=response.token,

            charge_total='100.01',
        )

        self.assertFalse(response.authorized)
        self.assertFalse(response.captured)

    def test_pix_create(self):
        response = self.maxipago.pix.add(
            referenceNum=randint(1, 100000),
            processorID=payment_processors.TEST,
            chargeTotal=10,
            expirationTime=300
        )

        self.assertTrue(response.approved)
        self.assertIsNotNone(response.emv) # código pix copia e cola
        self.assertIsNotNone(response.imagem_base64) # qr code
        self.assertEqual(response.response_code, '0')
        self.assertEqual(response.processor_message, 'APPROVED')
        self.assertIsNotNone(response.order_id)
        self.assertIsNotNone(response.processor_transaction_id)
        self.assertIsNotNone(response.processor_reference_number)

    def test_pix_create_exception(self):
        with self.assertRaises(exceptions.PaymentException):
            # Requisição sem `expirationTime`
            self.maxipago.pix.add(
                referenceNum=randint(1, 100000),
                processorID=payment_processors.TEST,
                chargeTotal=10,
            )

    def test_get_transaction_pix(self):
        # Create pix
        ref = randint(1, 100000)
        response = self.maxipago.pix.add(
            referenceNum=ref,
            processorID=payment_processors.TEST,
            chargeTotal=10,
            expirationTime=300
        )
        tid = response.transaction_id

        response = self.maxipago.transaction.get(transaction_id=tid)
        r_json = self.maxipago.transaction.to_json(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(r_json.get("transactionId"))
        self.assertIsNotNone(r_json.get("emv"))
        self.assertIsNotNone(r_json.get("imagem_base64"))
        self.assertEqual(r_json.get("referenceNumber"), str(ref))
        self.assertEqual(r_json.get("transactionAmount"), "10.00")

    def test_http_exception(self):
        CUSTOMER_ID = randint(1, 100000)
        customer_manager = self.maxipago.customer
        customer_manager.uri_api = 'https://testapi.maxipago.net/UniversalAPI/WrongUri'
        with self.assertRaises(exceptions.HttpErrorException):
            customer_manager.add(
                customer_id=CUSTOMER_ID,
                first_name='Fulano',
                last_name='de Tal',
            )


if __name__ == '__main__':
    unittest.main()
