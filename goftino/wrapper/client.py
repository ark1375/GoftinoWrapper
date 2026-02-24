import urllib.parse
from urllib.parse import urlencode
import requests
import os
import logging
from typing import Optional, Dict, Any, Union

from .data_types import Error, Response

logger = logging.getLogger("goftino_client")


class Goftino:
    """Goftino API client for chat management."""

    BASE_URL = "https://api.goftino.com/v1/"

    def __init__(
        self, 
        api_key: Optional[str] = None,
        session: Optional[requests.Session] = None  # NEW: Optional parameter
    ):
        """
        Initialize Goftino client.

        Args:
            api_key: API key for authentication. If not provided, reads from GOFTINO_KEY environment variable.
            session: Optional requests.Session for connection pooling. If None, creates a new session.

        Raises:
            ValueError: If no API key is provided and GOFTINO_KEY is not set.
        """
        if api_key:
            self._api_key = api_key
        else:
            if "GOFTINO_KEY" not in os.environ:
                logger.error("ApiKey Not Found.")
                raise ValueError("API key must be provided or set in GOFTINO_KEY environment variable")
            self._api_key = os.getenv("GOFTINO_KEY")

        self._headers = {
            "Content-Type": "application/json",
            "goftino-key": self._api_key
        }

        # NEW: Use provided session or create new one
        self._session = session if session is not None else requests.Session()
        self._owns_session = session is None  # Track if we created the session

    def close(self):
        """Close the session if we own it. Call this when done using the client."""
        if self._owns_session and self._session:
            self._session.close()

    def __enter__(self):
        """Context manager support."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup."""
        self.close()

    def _build_url(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> str:
        """Build complete URL with query parameters."""
        url = urllib.parse.urljoin(self.BASE_URL, endpoint)
        if params:
            filtered_params = {k: v for k, v in params.items() if v is not None}
            if filtered_params:
                query_string = urlencode(filtered_params)
                url = f"{url}?{query_string}"
        return url

    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        model_type: Optional[str] = None
    ) -> Union[Response, Error]:
        """
        Make HTTP request and handle response.

        Args:
            method: HTTP method ('GET' or 'POST')
            endpoint: API endpoint
            params: URL query parameters
            json_data: JSON payload for POST requests
            model_type: Model type to inject into response data

        Returns:
            Response or Error object
        """
        url = self._build_url(endpoint, params if method == 'GET' else None)

        try:
            # CHANGED: Use self._session instead of requests directly
            if method == 'GET':
                resp = self._session.get(url=url, headers=self._headers)
            else:  # POST
                filtered_json = {k: v for k, v in json_data.items() if v is not None} if json_data else {}
                resp = self._session.post(url=url, headers=self._headers, json=filtered_json)

            output = resp.json()

            if resp.status_code == 200:
                if model_type:
                    if 'data' not in output:
                        output['data'] = {}
                    output['data']['model'] = model_type
                return Response(**output)
            else:
                return Error(**output)

        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

    def get_all_chats(
        self,
        limit: int = 10,
        page: int = 0,
        operator_id: Optional[str] = None,
        status: Optional[str] = None,
        has_owner: Optional[bool] = None
    ) -> Response:
        """Retrieve all chats with optional filtering."""
        params = {
            'limit': limit,
            'page': page,
            'operator_id': operator_id,
            'status': status,
            'has_owner': has_owner
        }
        return self._make_request('GET', 'chats', params=params, model_type='chats')

    def get_chat(
        self,
        chat_id: Optional[str] = None,
        user_id: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        limit: int = 50,
        page: Optional[int] = None
    ) -> Response:
        """Retrieve chat data by chat_id or user_id."""
        if not (chat_id is None) ^ (user_id is None):
            raise ValueError("Either chat_id or user_id must be set, but not both.")

        params = {
            'chat_id': chat_id,
            'user_id': user_id,
            'from_date': from_date,
            'to_date': to_date,
            'limit': limit,
            'page': page
        }
        return self._make_request('GET', 'chat_data', params=params, model_type='chat')

    def user_unread_messages(
        self,
        chat_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Response:
        """Get unread messages for a user."""
        if not (chat_id or user_id):
            raise ValueError('Either the user_id or chat_id parameter should be provided!')

        params = {'chat_id': chat_id, 'user_id': user_id}
        return self._make_request('GET', 'user_unread_messages', params=params, model_type='chat')

    def user_data(
        self,
        chat_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Response:
        """Retrieve user data."""
        if not (chat_id or user_id):
            logger.error("Either the user_id or chat_id parameter should be provided!")
            raise ValueError("Either the user_id or chat_id parameter should be provided!")

        params = {'chat_id': chat_id, 'user_id': user_id}
        return self._make_request('GET', 'user_data', params=params, model_type='user_data')

    def get_all_operators(self) -> Response:
        """Retrieve all operators."""
        return self._make_request('GET', 'operators', model_type='operators')

    def get_operator_data(
        self,
        email: Optional[str] = None,
        operator_id: Optional[str] = None
    ) -> Response:
        """Retrieve operator data by email or operator_id."""
        if not (email or operator_id):
            logger.error('Either the email or operator_id parameter should be provided!')
            raise ValueError('Either the email or operator_id parameter should be provided!')

        params = {'email': email, 'operator_id': operator_id}
        return self._make_request('GET', 'operator_data', params=params, model_type='operator')

    def send_message(
        self,
        chat_id: str,
        operator_id: str,
        message: str,
        reply_id: Optional[str] = None
    ) -> Response:
        """Send a message as an operator."""
        json_data = {
            'chat_id': chat_id,
            'operator_id': operator_id,
            'message': message,
            'reply_id': reply_id
        }
        return self._make_request('POST', 'send_message', json_data=json_data, model_type='send_message')

    def send_from_user(
        self,
        chat_id: str,
        message: str,
        reply_id: Optional[str] = None
    ) -> Response:
        """Send a message as a user."""
        json_data = {'chat_id': chat_id, 'message': message, 'reply_id': reply_id}
        return self._make_request('POST', 'send_message_from_user', json_data=json_data, model_type='general')

    def send_operator_typing(
        self,
        chat_id: str,
        operator_id: str,
        typing_status: bool = True
    ) -> Response:
        """Send operator typing status."""
        json_data = {
            'chat_id': chat_id,
            'operator_id': operator_id,
            'typing_status': 'true' if typing_status else 'false'
        }
        return self._make_request('POST', 'operator_typing', json_data=json_data, model_type='general')

    def close_chat(self, chat_id: str, operator_id: str) -> Response:
        """Close a chat."""
        json_data = {'chat_id': chat_id, 'operator_id': operator_id}
        return self._make_request('POST', 'close_chat', json_data=json_data, model_type='general')

    def assign_chat(
        self,
        chat_id: str,
        from_operator: str,
        to_operator: str
    ) -> Response:
        """Assign chat from one operator to another."""
        json_data = {
            'chat_id': chat_id,
            'from_operator': from_operator,
            'to_operator': to_operator
        }
        return self._make_request('POST', 'assign_chat', json_data=json_data, model_type='general')

    def unassign_chat(self, chat_id: str, from_operator: str) -> Response:
        """Unassign chat from an operator."""
        json_data = {'chat_id': chat_id, 'from_operator': from_operator}
        return self._make_request('POST', 'unassign_chat', json_data=json_data, model_type='general')

    def send_poll(self, chat_id: str) -> Response:
        """Send a poll to chat."""
        json_data = {'chat_id': chat_id}
        return self._make_request('POST', 'send_poll', json_data=json_data, model_type='general')

    def send_file(
        self,
        chat_id: str,
        operator_id: str,
        file_url: str,
        file_name: str,
        file_size: Optional[str] = None,
        file_duration: Optional[str] = None
    ) -> Response:
        """Send a file."""
        json_data = {
            'chat_id': chat_id,
            'operator_id': operator_id,
            'file_url': file_url,
            'file_name': file_name,
            'file_size': file_size,
            'file_duration': file_duration
        }
        return self._make_request('POST', 'send_file', json_data=json_data, model_type='general')

    def edit_message(self, message: str, message_id: str) -> Response:
        """Edit an existing message."""
        json_data = {'message': message, 'message_id': message_id}
        return self._make_request('POST', 'edit_message', json_data=json_data, model_type='general')

    def create_chat(
        self,
        user_message: str,
        operator_message: Optional[str] = None,
        operator_id: Optional[str] = None
    ) -> Response:
        """Create a new chat."""
        if not ((operator_id is None) ^ (operator_message is None)):
            if (operator_id is not None) or (operator_message is not None):
                raise ValueError("operator_message and operator_id must be set together or not at all.")

        json_data = {
            'user_message': user_message,
            'operator_message': operator_message,
            'operator_id': operator_id
        }
        return self._make_request('POST', 'create_chat', json_data=json_data, model_type='create_chat')

    def remove_chat(self, chat_id: str) -> Response:
        """Remove a chat."""
        json_data = {'chat_id': chat_id}
        return self._make_request('POST', 'remove_chat', json_data=json_data, model_type='general')

    def widget(
        self,
        state: bool,
        chat_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Response:
        """Open or close widget."""
        if not ((chat_id is not None) ^ (user_id is not None)):
            raise ValueError("Either chat_id or user_id must be passed, but not both.")

        action = "open" if state else "close"
        json_data = {'chat_id': chat_id, 'user_id': user_id, 'action': action}
        return self._make_request('POST', 'widget', json_data=json_data, model_type='general')

    def dispatch_js_event(
        self,
        event: str,
        chat_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Response:
        """Dispatch a JavaScript event."""
        if not ((chat_id is not None) ^ (user_id is not None)):
            raise ValueError("Either chat_id or user_id must be passed, but not both.")

        json_data = {'chat_id': chat_id, 'user_id': user_id, 'event': event}
        return self._make_request('POST', 'dispatch_js_event', json_data=json_data, model_type='general')


if __name__ == '__main__':
    client = Goftino()
