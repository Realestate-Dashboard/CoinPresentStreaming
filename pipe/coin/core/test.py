import json
from ubkc_market import CoinoneRestAndSocket
from coin.core.coin_socket_interaction import MessageDataPreprocessing

from pathlib import Path

path = Path(__file__).parent.parent


class __MarketAPIFactory:
    """Factory for market APIs."""

    _create = {
        "coinone": CoinoneRestAndSocket,
    }

    @classmethod
    def market_load(cls, conn_type: str, *args, **kwargs):
        """
        거래소 API의 인스턴스를 생성합니다.
        """
        if conn_type not in cls._create:
            raise ValueError(f"잘못된 연결 유형: {conn_type}")

        creator = cls._create[conn_type]
        return creator(*args, **kwargs)


def load_json(conn_type: str):
    """
    Open the file and load market information.

    ExchangeDataTypeHints(Type): dict[str, ExchangeConfig]
    - from coin.core.util._typing import ExchangeDataTypeHints
    """
    with open(
        file=f"{path}/config/_market_{conn_type}.json", mode="r", encoding="utf-8"
    ) as file:
        market_info = json.load(file)

    market_info = {
        market: {**info, "api": __MarketAPIFactory.market_load(market)}
        for market, info in market_info.items()
    }
    return market_info



def get_socket_parameter(self, symbol: str) -> dict[str, str, dict[str, str]]:
    return {
        "request_type": "SUBSCRIBE",
        "channel": "TICKER",
        "topic": {"quote_currency": "KRW", "target_currency": f"{symbol}"},
    }

async def get_present_websocket(self, symbol: str) -> None:
    from coin.core.coin_socket_interaction import WebsocketConnectionManager as WCM

    return await WCM().websocket_to_json(
        uri=self.__coin_websocket,
        subscribe_fmt=self.get_socket_parameter(symbol=symbol),
        symbol=symbol,
    )