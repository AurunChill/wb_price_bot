import asyncio
import aiohttp
from datetime import datetime
from typing import Optional, Dict, List


class AsyncWildberriesParser:
    def __init__(self):
        self.session = None
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "ru-RU,ru;q=0.9",
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def _fetch(self, url: str) -> Optional[Dict]:
        """Асинхронный GET-запрос"""
        try:
            async with self.session.get(
                url, headers=self.headers, timeout=3
            ) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            print(f"Request error: {str(e)}")
            return None

    async def _get_vol_part_nm(self, article: str):
        nm = int(article)
        vol = nm // 100000
        part = nm // 1000

        return vol, part, nm

    async def _get_price_history(self, article: str) -> List[Dict]:
        """Параллельный перебор корзин для истории цен"""
        vol, part, nm = await self._get_vol_part_nm(article)

        async def fetch_basket(basket: int):
            url = f"https://basket-{basket:02d}.wbbasket.ru/vol{vol}/part{part}/{nm}/info/price-history.json"
            try:
                async with self.session.get(url, timeout=1) as response:
                    if response.status == 200:
                        data = await response.json()
                        return [
                            {
                                "date": datetime.fromtimestamp(item["dt"]).strftime(
                                    "%d-%m-%Y"
                                ),
                                "price": round(item["price"]["RUB"] / 100, 2),
                            }
                            for item in data
                        ]
            except Exception:
                return None

        tasks = [fetch_basket(b) for b in range(1, 100)]
        for result in await asyncio.gather(*tasks):
            if result:
                return result

        return []

    async def _find_valid_image_url(self, article: str) -> str:
        """Параллельный поиск изображения с приоритетом big"""
        vol, part, nm = await self._get_vol_part_nm(article)

        async def check_image(basket: int, size: str):
            url = f"https://basket-{basket:02d}.wbbasket.ru/vol{vol}/part{part}/{nm}/images/{size}/1.webp"
            try:
                async with self.session.head(url) as response:
                    return url if response.status == 200 else None
            except Exception:
                return None

        # Если не нашли big, проверяем другие размеры
        for size in ["big", "c246x328", "tm"]:
            tasks = [check_image(b, size) for b in range(1, 100)]
            for result in await asyncio.gather(*tasks):
                if result:
                    return result

        return ""

    async def get_product_info(self, article: str) -> Optional[Dict]:
        """Основной асинхронный метод"""
        main_url = f"https://www.wildberries.ru/catalog/{article}/detail.aspx"
        data_url = f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-5856842&spp=30&ab_testing=false&lang=ru&nm={article}"

        product_data = await self._fetch(data_url)
        if not product_data or not product_data.get("data", {}).get("products"):
            return None

        product = product_data["data"]["products"][0]
        sizes = product.get("sizes", [{}])
        stocks = sizes[0].get("stocks", [{}]) if sizes else [{}]

        try:
            current_price = round(sizes[0]["price"]["product"] / 100, 2)
        except KeyError:
            current_price = 0.0

        price_history = await self._get_price_history(article)
        image_url = await self._find_valid_image_url(article)

        current_price_entry = {
            "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "price": current_price,
        }

        full_history = price_history + [current_price_entry]
        min_entry = min(full_history, key=lambda x: x["price"]) if full_history else {}
        max_entry = max(full_history, key=lambda x: x["price"]) if full_history else {}

        prev_price_entry = price_history[-2] if len(price_history) >= 2 else None

        return {
            "link": main_url,
            "name": product.get("name", ""),
            "article": article,
            "current_price": current_price,
            "prev_price": prev_price_entry["price"] if prev_price_entry else None,
            "prev_price_date": prev_price_entry["date"] if prev_price_entry else "N/A",
            "stock": sum(stock.get("qty", 0) for stock in stocks),
            "image_url": image_url,
            "min_price": min_entry.get("price", 0.0),
            "min_price_date": min_entry.get("date", "N/A"),
            "max_price": max_entry.get("price", 0.0),
            "max_price_date": max_entry.get("date", "N/A"),
            "updated": datetime.now().strftime("%d-%m-%Y %H:%M"),
        }


async def main():
    async with AsyncWildberriesParser() as parser:
        test_articles = ["319796142"]
        for article in test_articles:
            result = await parser.get_product_info(article)
            if result:
                print("\nУспешно получены данные:")
                print(f"Ссылка: {result['link']}")
                print(f"Название: {result['name']}")
                print(f"Остаток: {result['stock']} шт.")
                print(f"Изображение: {result['image_url']}")
                print(f"Артикул: {result['article']}")
                print(f"Цена: {result['current_price']} руб.")
                print(f"Изменение: {result['prev_price']} → {result['current_price']}")
            else:
                print(f"\nНе удалось получить данные для артикула {article}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
