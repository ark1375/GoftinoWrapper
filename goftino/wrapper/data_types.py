from typing import Annotated, Literal, Union, Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator


class StrictModel(BaseModel):
    """Base model with strict validation."""

    model_config = ConfigDict(
        extra='forbid',  # reject unknown fields
        validate_by_alias=True,  # allow aliases like "from_"
        validate_by_name=True
    )


class Operator(StrictModel):
    """Operator model."""
    avatar: str
    name: str
    email: str
    is_online: bool
    operator_id: str
    model: Literal['operator'] = Field(default='operator')


class Sender(StrictModel):
    """Message sender model."""
    from_: str = Field(..., alias="from")  # Using "from_" because "from" is a reserved keyword
    id_: str = Field(..., alias='id')


class Fields(StrictModel):
    """Custom fields model."""
    label: str
    value: str


class Message(StrictModel):
    """Chat message model."""
    message_id: str
    sender: Sender
    date: str
    content: str
    type: str
    is_seen: Optional[bool] = Field(default=False)
    reply_to: Optional[str] = Field(default=None)
    file_name: Optional[str] = Field(default=None)
    file_size: Optional[str] = Field(default=None)
    file_duration: Optional[str] = Field(default=None)
    fields: Optional[List[Fields]] = Field(default=None)


class Chats(StrictModel):
    """Chats collection model."""

    class ChatsContent(StrictModel):
        """Individual chat content."""
        chat_id: str
        chat_status: str
        unread_messages: int
        last_message: Message
        all_operators: List[Any] = Field(default_factory=list)
        current_owner: List[Any] = Field(default_factory=list)
        user_id: str
        user_name: str

    chats: List['Chats.ChatsContent']
    page: int
    model: Literal['chats']


class Chat(StrictModel):
    """Single chat model."""
    messages_count: int
    messages: List[Message]
    chat_status: str
    user_id: str
    chat_id: Optional[str] = Field(default=None)
    current_owner: List[Any] = Field(default_factory=list)
    all_operators: List[Any] = Field(default_factory=list)
    model: Literal['chat']


class UserData(StrictModel):
    """User data model."""
    chat_id: str
    user_id: str
    avatar: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    tags: List[Any] = Field(default_factory=list)
    metadata: Union[Dict[str, Any], List[Any]] = Field(default_factory=dict)
    ip: Optional[str] = Field(default=None)
    location: Optional[str] = Field(default=None)
    browser: Optional[str] = Field(default=None)
    os: Optional[str] = Field(default=None)
    is_banned: Optional[bool] = Field(default=None)
    last_url: Optional[str] = Field(default=None)
    last_visit: Optional[str] = Field(default=None)
    first_visit: Optional[str] = Field(default=None)
    page_view: Optional[str] = Field(default=None)
    model: Literal['user_data']


class Operators(StrictModel):
    """Operators collection model."""
    operators: List[Operator]
    model: Literal['operators']


class SendMessage(StrictModel):
    """Send message response model."""
    message_id: str
    model: Literal['send_message']


class CreateChat(StrictModel):
    """Create chat response model."""
    chat_id: str
    user_id: str
    model: Literal['create_chat']


class Error(StrictModel):
    """Error response model."""
    status: str
    code: str
    detail: Optional[str] = None

    @model_validator(mode="after")
    def set_detail(self) -> 'Error':
        """Set error detail based on error code."""
        error_code_dict = {
            "1": "Wrong API key given.",
            "2": "Wrong input parameters for the requested endpoint.",
            "3": "Unauthorized access. You don't have the permission to perform this action.",
            "4": "Server Error. Server encountered some problems. Try again later please.",
            "5": "Wrong model. Try a valid one."
        }
        self.detail = error_code_dict.get(self.code, "Unknown error")
        return self


DataUnion = Annotated[
    Union[Chats, Chat, Operator, Operators, UserData, SendMessage, CreateChat],
    Field(discriminator='model')
]


class Response(StrictModel):
    """API response model."""
    status: str
    code: str = "200"
    data: Union[DataUnion, Dict[str, Any]] = Field(default_factory=dict)

    @field_validator('data', mode='before')
    @classmethod
    def ensure_model_discriminator(cls, v: Any) -> Any:
        """
        If the backend didn't include 'model', infer it from signature keys.
        Only inject when confident; otherwise raise so the caller handles it.
        """
        if not isinstance(v, dict):
            return v

        if v.get('model') == 'general':
            return dict()

        if 'model' in v:
            return v

        return v
