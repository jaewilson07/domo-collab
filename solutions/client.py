from dataclasses import dataclass
from typing import Union
import requests


class DomoAPIRequest_Error(Exception):
    """a customized Exception class for handing Domo errors"""

    def __init__(self, function_name, message):
        super().__init__(f"{function_name} | {message} ")


@dataclass
class ResponseClass:
    status: int  # API response status code
    is_success: bool
    response: dict

    @classmethod
    def from_request_response(
        cls, res: requests.models.Response, response: Union[list, dict] = None
    ):

        is_success = res.ok

        response = (
            response or res.json() if res.headers.get("Content-Length") != "0" else None
        )

        # if there's an API errror, the Response class stores the error in the 'message' field of the response object
        if not is_success:
            response = response["message"]

        return cls(
            status=res.status_code,
            is_success=is_success,
            response=response,
        )
