"""Consumer"""

import asyncio

import aio_pika
from msfwk.desp.rabbitmq.mq_message import DespMQMessage, ModerationEventStatus, queue_consumer_callback
from msfwk.mqclient import RabbitMQConfig, consume_mq_queue_async, send_error_message, send_mq_message
from msfwk.utils.logging import get_logger

from moderation_handling.utils import delete_message_from_manual_moderation

logger = get_logger(__name__)


class QueueConsumer:
    """Store the consumer"""

    consumer: asyncio.Task = None


@queue_consumer_callback(DespMQMessage)
async def play_callback(mq_message: DespMQMessage, message: aio_pika.IncomingMessage) -> None:
    """Play the callback of the given message
    Will try to convert message body into DespMQMessage in order to play it's callback (reject / accept)

    Args:
        mq_message (DespMQMessage): converted message
        message (aio_pika.IncomingMessage): original message received from mq
    """
    logger.info("Treating received message")
    try:
        status = mq_message.status
        if status == ModerationEventStatus.Accepted:
            await delete_message_from_manual_moderation(mq_message.id)
            logger.info("Apply Accepted Callbacks")
            await mq_message.execute_accept_callbacks()
        elif status == ModerationEventStatus.Rejected:
            await delete_message_from_manual_moderation(mq_message.id)
            logger.info("Apply Rejected Callbacks")
            await mq_message.execute_reject_callbacks()
        elif status == ModerationEventStatus.Manual_Pending:
            await delete_message_from_manual_moderation(mq_message.id)
            logger.info("Send message to manual moderation")
            await send_mq_message(mq_message, RabbitMQConfig.MODERATION_EXCHANGE, RabbitMQConfig.TO_MANUAL_RKEY)
        else:
            logger.warning("Received a message that is in status: %s, which is not handled", status)
        await message.ack()
    except Exception as e:
        err_mess = f"Exception processing message: {e}. Sending to Error queue"
        logger.exception(err_mess, exc_info=e)
        await message.nack(requeue=False)
        await send_error_message(mq_message, err_mess)


async def listen_to_handle(queue_name: str) -> None:
    """Listen to the given queue, an play the callbacks of all received message

    Args:
        queue_name (str): _description_
    """
    logger.info("Listening to queue: %s", queue_name)
    QueueConsumer.consumer = await consume_mq_queue_async(queue_name, play_callback)
    logger.info("Waiting for messages.")


async def stop_listening() -> None:
    """Stops the consumer"""
    logger.info("Stop Listening to Handling queue")
    try:
        if QueueConsumer.consumer is not None:
            QueueConsumer.consumer.cancel()
    except asyncio.CancelledError:
        logger.warning("Consumer task was already cancelled.")
