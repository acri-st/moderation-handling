"""Main"""

from msfwk.application import app
from msfwk.context import current_config, register_destroy, register_init
from msfwk.mqclient import RabbitMQConfig, load_default_rabbitmq_config
from msfwk.utils.logging import get_logger

from moderation_handling.consumer import listen_to_handle, stop_listening

logger = get_logger("application")


app_handling = app


async def init(config: dict) -> bool:
    """Init"""
    logger.info("Start Initialisation ...")
    load_succeded = load_default_rabbitmq_config()
    current_config.set(config)
    if load_succeded:
        await listen_to_handle(RabbitMQConfig.HANDLING_MODERATION_QUEUE)
    else:
        logger.error("Failed to load rabbitmq config")
    return load_succeded


async def destroy(_: dict) -> bool:
    """Destroy"""
    logger.info("Start Destroying ...")
    await stop_listening()


register_init(init)
register_destroy(destroy)
