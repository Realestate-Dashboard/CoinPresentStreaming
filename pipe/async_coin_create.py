"""
실시간 테스트 
"""

import asyncio

from coin.core.coin_interaction import CoinPresentPriceMarketPlace
from coin.core.config.properties import BTC_TOPIC_NAME, ETH_TOPIC_NAME
from coin.core.data_mq.data_admin import new_topic_initalization


async def btc_present_start() -> None:
    """
    bitcoin kafak stream
    """
    await CoinPresentPriceMarketPlace.total_full_request("BTC", BTC_TOPIC_NAME)


async def eth_present_start() -> None:
    """
    ethereum kafak stream
    """
    await CoinPresentPriceMarketPlace.total_full_request("ETC", ETH_TOPIC_NAME)


async def be_present_gether() -> None:
    """
    kafka async steam
    """
    tasks = [
        asyncio.create_task(btc_present_start()),
        asyncio.create_task(eth_present_start()),
    ]
    await asyncio.gather(*tasks, return_exceptions=True)


async def start() -> None:
    """
    Topic create
    """
    topic = [BTC_TOPIC_NAME, ETH_TOPIC_NAME]
    partition = [2, 2]
    replication = [2, 2]

    new_topic_initalization(
        topic=topic, partition=partition, replication_factor=replication
    )

    asyncio.sleep(1)
    await be_present_gether()


asyncio.run(start())
