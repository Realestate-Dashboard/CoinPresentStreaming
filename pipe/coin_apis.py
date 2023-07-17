from typing import Any
from abc import ABC, abstractmethod
from data_format import CoinSymbol
from properties import get_symbol_collect_url, header_to_json


class CoinFullRequest(ABC):
    """
    Subject:
        - 공통 목록 추상클래스 [개발 순서 및 혼동 방지]
        - 가독성 측면 [유지보수성 관리] \n
    Args:
        - market : 거래소 이름
        - symbol_collect : 코인 심볼 뽑아낼때 쓰는 URL
    """

    def __init__(self, market: str, coin_name: (str | None) = None) -> None:
        self.market = market
        self.coin_name = coin_name
        self.url: str = get_symbol_collect_url(self.market)

    @abstractmethod
    def coinsymbol_extraction(self) -> list[str]:
        """
        Subject:
            - 코인 심볼 추출 \n
        Input:
            - market API 형식 \n
        Returns:
            - list[str]: ["BTC", "ETH" ....]
        """
        pass

    @abstractmethod
    def __getitem__(self, index: Any) -> Any:
        """
        Subject:
            - 코인 인덱스 가격 정보 \n
        Input:
            - market API 형식 \n
        Returns:
            - market 형식
        """
        pass

    def __upperletter__(self) -> str:
        return self.coin_name.upper()

    def __lowletter__(self) -> str:
        return self.coin_name.lower()


class UpBitCoinFullRequest(CoinFullRequest):
    def __init__(self) -> None:
        super().__init__(market="upbit", coin_name="BTC")
        self.upbit_coin_list: list[dict[str, str]] = header_to_json(
            url=f"{self.url}/market/all?isDetails=true"
        )
        self.upbit_coin_present_price = header_to_json(
            url=f"{self.url}/ticker?markets=KRW-{self.__upperletter__()}"
        )

    def coinsymbol_extraction(self) -> list[str]:
        """
        Subject:
            - 코인 심볼 추출 \n
        Input:
            - {
                'market_warning': 'NONE',
                'market': 'KRW-BLUR',
                'korean_name': '블러',
                'english_name': 'Blur'
            } \n
        Returns:
            - list[str]: ["BTC", "ETH" ....]
        """
        return [
            CoinSymbol(coin_symbol=symbol["market"].split("-")[-1]).coin_symbol
            for symbol in self.upbit_coin_list
            if symbol["market"].startswith("KRW-")
        ]

    def __getitem__(self, index: Any) -> Any:
        """
        Args:
            index (Any): List Index 번호 \n
        Returns:
            -  {
                'market': 'KRW-BTC',
                'trade_date': '20230717',
                'trade_time': '090305',
                'trade_date_kst': '20230717',
                'trade_time_kst': '180305',
                'trade_timestamp': 1689584585843,
                'opening_price': 38946000.0,
                'high_price': 39022000.0,
                'low_price': 38832000.0,
                }
        """
        return self.upbit_coin_present_price[index]


class BithumbCoinFullRequest(CoinFullRequest):
    def __init__(self) -> None:
        super().__init__(market="bithum", coin_name=None)
        self.bithum_coin_list: dict[str, Any] = header_to_json(
            url=f"{self.url}/ticker/ALL_KRW"
        )
        self.bithum_present_price = header_to_json(
            url=f"{self.url}/ticker/{self.__upperletter__()}_KRW"
        )

    def coinsymbol_extraction(self) -> list[str]:
        """
        Subject:
            - 코인 심볼 추출 \n
        Input:
            - {
                "status": "0000",
                "data": {
                    "BTC": {
                        "opening_price": "54353000",
                        "closing_price": "53768000",
                        "min_price": "53000000"
                        ...
                    }
                }
            } \n
        Returns:
            - list[str]: ["BTC", "ETH" ....]
        """
        return [
            CoinSymbol(coin_symbol=symbol).coin_symbol
            for symbol in self.bithum_coin_list["data"]
        ][:-1]


class KorbitCoinFullRequest(CoinFullRequest):
    def __init__(self) -> None:
        super().__init__(market="korbit", coin_name=None)
        self.korbit_coin_list: dict[str, dict[str, Any]] = header_to_json(
            url=f"{self.url}/ticker/detailed/all"
        )
        self.korbit_present_price = header_to_json(
            f"{self.url}/ticker/detailed?currency_pair={self.__lowletter__()}_krw"
        )

    def coinsymbol_extraction(self) -> list[str]:
        """
        Subject:
            - 코인 심볼 추출 \n
        Input:
           - {
                "bch_krw": {
                    "timestamp": 1559285555322,
                    "last": "513000",
                    "open": "523900",
                    ...
                }
            } \n
        Returns:
            - list[str]: ["BTC", "ETH" ....]
        """
        return [
            CoinSymbol(coin_symbol=symbol.split("_")[0].upper()).coin_symbol
            for symbol in self.korbit_coin_list
        ]
