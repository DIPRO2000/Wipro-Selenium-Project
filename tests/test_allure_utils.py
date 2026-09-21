import unittest
from unittest.mock import Mock, patch

from framework.allure_utils import attach_http_exchange


class AllureUtilsTests(unittest.TestCase):
    def test_attach_http_exchange_redacts_request_and_response_data(self) -> None:
        response = Mock()
        response.status_code = 200
        response.headers = {"Content-Type": "application/json", "Authorization": "secret"}
        response.json.return_value = {
            "responseCode": 200,
            "message": "User exists!",
            "token": "response-secret",
        }

        request = {
            "method": "POST",
            "url": "https://automationexercise.com/api/verifyLogin",
            "data": {"email": "test@example.com", "password": "secret123"},
            "headers": {"Authorization": "request-secret"},
        }

        with patch("framework.allure_utils.allure.attach") as attach:
            attach_http_exchange(request, response)

        self.assertEqual(attach.call_count, 2)
        attached_text = "\n".join(call.args[0] for call in attach.call_args_list)
        self.assertNotIn("secret123", attached_text)
        self.assertNotIn("request-secret", attached_text)
        self.assertNotIn("response-secret", attached_text)
        self.assertIn("***REDACTED***", attached_text)

    def test_attach_http_exchange_tolerates_invalid_json_response(self) -> None:
        response = Mock()
        response.status_code = 500
        response.headers = {}
        response.json.side_effect = ValueError("not JSON")
        response.text = "plain response"

        with patch("framework.allure_utils.allure.attach") as attach:
            attach_http_exchange({"method": "GET", "url": "https://example.test"}, response)

        self.assertEqual(attach.call_count, 2)
        self.assertIn("plain response", attach.call_args_list[1].args[0])


if __name__ == "__main__":
    unittest.main()
