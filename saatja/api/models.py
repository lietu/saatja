from datetime import datetime
from typing import Optional, List, Any

from pydantic import BaseModel, Field, AnyHttpUrl


class CreateTask(BaseModel):
    url: AnyHttpUrl = Field(..., description="Webhook destination URL")
    when: datetime = Field(
        ...,
        description="Approximate RFC 3339 datetime after which it is ok to send webhook",
    )
    payload: Any = Field(None, description="Webhook payload")


class CreateTaskResponse(BaseModel):
    id: str = Field(..., description="Task ID")


# TODO: Implement in the future
class GetTaskResponse(BaseModel):
    url: AnyHttpUrl = Field(..., description="Webhook destination URL")
    when: datetime = Field(
        ...,
        description="Approximate RFC 3339 datetime after which it is ok to send webhook",
    )
    delivered: Optional[datetime] = Field(
        ..., description="RFC 3339 datetime on which the webhook was delivered"
    )
    errors: List[str] = Field(
        ..., description="List of the last timestamps of failed deliveries"
    )


# TODO: Implement in the future
class GetTaskErrorResponse(BaseModel):
    code: int = Field(..., description="Response HTTP status code")
    response: str = Field(..., description="The response body")
