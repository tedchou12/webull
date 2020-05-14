import pytest
import requests_mock

from unittest.mock import MagicMock
from webull.webull import webull, endpoints

'''

[HOW TO RUN TESTS]

pip install pytest requests_mocks
python -m pytest -v

'''

# FIXTURES

urls = endpoints.urls()

@pytest.fixture
def reqmock():
    with requests_mock.Mocker() as m:
        yield m

@pytest.fixture
def wb():
    return webull()



# TESTS

@pytest.mark.skip(reason="TODO")
def test_alerts_add():
	pass


@pytest.mark.skip(reason="TODO")
def test_alerts_list():
	pass

@pytest.mark.skip(reason="TODO")
def test_alerts_remove():
	pass

@pytest.mark.skip(reason="TODO")
def test_build_req_headers():
	pass

@pytest.mark.skip(reason="TODO")
def test_cancel_order():
	pass

@pytest.mark.skip(reason="TODO")
def test_cancel_otoco_order():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_account():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_account_id():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_active_gainer_loser():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_analysis():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_bars():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_calendar():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_current_orders():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_detail():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_dividends():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_financials():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_history_orders():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_news():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_option_quote():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_options():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_options_by_strike_and_expire_date():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_options_expiration_dates():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_portfolio():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_positions():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_quote():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_ticker():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_tradable():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_trade_token():
	pass

@pytest.mark.skip(reason="TODO")
def test_login(reqmock, wb):
    # [case 1] login fails, bad mobile username credentials
    reqmock.post(urls.login(), text='''
        {
          "success": false,
          "code": "phone.illegal"
        }
    ''')

    bad_mobile_username = '1112224444'
    resp = wb.login(username=bad_mobile_username, password='xxxxxxxx')
    assert resp['success'] == False
    assert resp['code'] == 'phone.illegal'

    # [case 2] mobile login succeeds
    # actual API response includes more data, but for brevity,
    # this mock response only returns the fields which we are expecting
    reqmock.post(urls.login(), text='''
        {
            "success":true,
            "code":"200",
            "data":{
                "accessToken":"xxxxxxxxxx",
                "uuid":"yyyyyyyyyy",
                "refreshToken":"zzzzzzzzzz",
                "tokenExpireTime":"2020-07 13T00:25:34.235+0000"
            }
        }
    ''')
    # mocking this to cover webull.login internal call to webull.get_account_id
    wb.get_account_id = MagicMock(return_value='11111111')

    resp = wb.login(username='1+1112223333', password='xxxxxxxx')
    assert resp['success'] == True
    assert wb._access_token == 'xxxxxxxxxx'
    assert wb._refresh_token == 'zzzzzzzzzz'
    assert wb._token_expire == '2020-07 13T00:25:34.235+0000'
    assert wb._uuid == 'yyyyyyyyyy'
    assert wb._account_id == '11111111'

    # if username or password is not passed, should raise ValueError
    with pytest.raises(ValueError):
        wb.login()

def test_login_prompt():
	pass

@pytest.mark.skip(reason="TODO")
def test_logout(wb, reqmock):
    # successful logout returns a 200 response
    reqmock.get(urls.logout(), status_code=200)
    resp = wb.logout()
    assert resp == 200

def test_modify_order():
	pass

@pytest.mark.skip(reason="TODO")
def test_place_option_order():
	pass

@pytest.mark.skip(reason="TODO")
def test_place_order():
	pass

@pytest.mark.skip(reason="TODO")
def test_place_otoco_order():
	pass

@pytest.mark.skip(reason="TODO")
def test_refresh_login():
	pass

@pytest.mark.skip(reason="TODO")
def test_replace_option_order():
	pass

@pytest.mark.skip(reason="TODO")
def test_run_screener():
	pass
