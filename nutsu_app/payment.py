from sslcommerz_lib import SSLCOMMERZ
from decouple import config
import requests


def create_get_session(tran_id,service,username,amount,name,email,phone):

    settings = { 'store_id': config('LIVE_STORE_ID'), 'store_pass': config('LIVE_STORE_PASS'), 'issandbox': False }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = tran_id
    post_body['success_url'] = config("SUCCESS_URL")+f"?service={service}&username={username}&amount={amount}&tran_id={tran_id}"
    post_body['fail_url'] = config("FAIL_URL")+f"?service={service}&username={username}&amount={amount}&tran_id={tran_id}"
    post_body['cancel_url'] = config("CANCEL_URL")+f"?service={service}&username={username}&amount={amount}&tran_id={tran_id}"
    post_body['emi_option'] = 0
    post_body['cus_name'] = name
    post_body['cus_email'] = email
    post_body['cus_phone'] = phone
    post_body['cus_add1'] = "Bangladesh"
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Prescribemate"
    post_body['product_category'] = "Software Subscription"
    post_body['product_profile'] = "Doctors"


    response = sslcz.createSession(post_body)
    
    return response['GatewayPageURL'],response["sessionkey"]
    # Need to redirect user to response['GatewayPageURL']

def validate_with_ipn():

    settings = { 'store_id': 'test_testemi', 'store_pass': 'test_testemi@ssl', 'issandbox': True } 

    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['tran_id'] = '5E121A0D01F92'
    post_body['val_id'] = '200105225826116qFnATY9sHIwo'
    post_body['amount'] = "10.00"
    post_body['card_type'] = "VISA-Dutch Bangla"
    post_body['store_amount'] = "9.75"
    post_body['card_no'] = "418117XXXXXX6675"
    post_body['bank_tran_id'] = "200105225825DBgSoRGLvczhFjj"
    post_body['status'] = "VALID"
    post_body['tran_date'] = "2020-01-05 22:58:21"
    post_body['currency'] = "BDT"
    post_body['card_issuer'] = "TRUST BANK, LTD."
    post_body['card_brand'] = "VISA"
    post_body['card_issuer_country'] = "Bangladesh"
    post_body['card_issuer_country_code'] = "BD"
    post_body['store_id'] = "test_testemi"
    post_body['verify_sign'] = "d42fab70ae0bcbda5280e7baffef60b0"
    post_body['verify_key'] = "amount,bank_tran_id,base_fair,card_brand,card_issuer,card_issuer_country,card_issuer_country_code,card_no,card_type,currency,currency_amount,currency_rate,currency_type,risk_level,risk_title,status,store_amount,store_id,tran_date,tran_id,val_id,value_a,value_b,value_c,value_d"
    post_body['verify_sign_sha2'] = "02c0417ff467c109006382d56eedccecd68382e47245266e7b47abbb3d43976e"
    post_body['currency_type'] = "BDT"
    post_body['currency_amount'] = "10.00"
    post_body['currency_rate'] = "1.0000"
    post_body['base_fair'] = "0.00"
    post_body['value_a'] = ""
    post_body['value_b'] = ""
    post_body['value_c'] = ""
    post_body['value_d'] = ""
    post_body['risk_level'] = "0"
    post_body['risk_title'] = "Safe"
    if sslcz.hash_validate_ipn(post_body):
        response = sslcz.validationTransactionOrder(post_body['val_id'])
        print(response)
    else:
        print("Hash validation failed")