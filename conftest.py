import uuid

import pytest
import sys
import requests

pytest.my_log = None

pytest.ws_connect = None
pytest.last_message_id = None
pytest.env = 'my_mac'

response = requests.request("GET", "https://autofaq.ai/awsbotkate", headers={}, data={}).text
position = response.find("data-widget-service-id=")
pytest.service_id = response[position:position+60].split('="')[1]

pytest.session_id = str(uuid.uuid4())
pytest.ws_session_id = str(uuid.uuid4())


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="my_mac")
    parser.addoption("--my_log", action="store_true")


if "--my_log" in sys.argv:
    pytest.my_log = True

for addoption in sys.argv:
    if "--env" in addoption:
        pytest.env = addoption.split('=')[1]

print("\nОткружение: " + pytest.env)


def pytest_sessionfinish(session, exitstatus):
    report_dir = session.config.option.allure_report_dir  # Gets the --alluredir directory path

    if report_dir:
        file = open(report_dir + "/environment.properties", "w")
        file.write("env=" + pytest.env)
        file.write("\nwidget=https://autofaq.ai/awsbotkate")
        file.write("\napi=https://chat.autofaq.ai/api/webhooks/widget")
        file.close()
