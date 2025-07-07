"""Utils"""

import requests
from fastapi import HTTPException
from msfwk.request import HTTP_SUCCESS, HttpClient
from msfwk.utils.logging import get_logger

logger = get_logger(__name__)


async def delete_message_from_manual_moderation(message_id: str) -> None:
    """Delete a message from manual_moderation

    Args:
        message_id (str): _description_

    Raises:
        HTTPException: _description_
        HTTPException: _description_
    """
    try:
        async with (
            HttpClient().get_service_session("moderation") as session,
            session.delete(f"/messages/{message_id}/") as response,
        ):
            if response.status == HTTP_SUCCESS:
                logger.info("Removed all message with id %s in moderation.", message_id)
            else:
                msg = f"Failed to delete messages with id {message_id}: {response.status} - {await response.text()}"
                logger.error(msg)
                raise HTTPException(status_code=response.status, detail=msg)

    except requests.exceptions.RequestException as e:
        # Handle errors related to the request (e.g., network issues)
        msg = f"Error during metadata upload: {e!s}"
        logger.exception(msg, exc_info=e)
        raise HTTPException(status_code=500, detail=msg) from e
