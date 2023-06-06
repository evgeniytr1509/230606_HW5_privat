import aiohttp
import asyncio
import datetime
import sys
import aiofile
import aiopath
import websocket

class CurrencyAPI:
    BASE_URL = 'https://api.privatbank.ua/p24api/exchange_rates'

    async def get_exchange_rates(self, currencies, days):
        today = datetime.date.today()
        start_date = today - datetime.timedelta(days=days)

        async with aiohttp.ClientSession() as session:
            tasks = []
            for date in self._date_range(start_date, today):
                url = f"{self.BASE_URL}?json&date={date.strftime('%d.%m.%Y')}"
                tasks.append(self._fetch(session, url, currencies))

            results = await asyncio.gather(*tasks)
            return results

    async def _fetch(self, session, url, currencies):
        async with session.get(url) as response:
            data = await response.json()
            exchange_rates = data.get('exchangeRate', [])
            rates = []
            for rate in exchange_rates:
                if rate['currency'] in currencies:
                    rates.append({
                        'date': data['date'],
                        'currency': rate['currency'],
                        'rate': rate['saleRate']
                    })
            return rates

    def _date_range(self, start_date, end_date):
        for n in range(int((end_date - start_date).days) + 1):
            yield start_date + datetime.timedelta(n)


class ConsoleApp:
    def __init__(self):
        self.currency_api = CurrencyAPI()

    async def run(self):
        currencies = input("Введите валюты (через запятую, например, EUR,USD): ").upper()
        currencies = currencies.split(',')
        days = input("Введите количество дней (не более 10): ")

        try:
            days = int(days)
            if days > 10:
                raise ValueError("Количество дней должно быть не более 10.")
        except ValueError as e:
            print(f"Ошибка: {e}")
            return

        try:
            results = await self.currency_api.get_exchange_rates(currencies, days)
            self._display_results(results)
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")

    def _display_results(self, results):
        print("Дата\t\tВалюта\tКурс")
        for rates in results:
            for rate in rates:
                print(f"{rate['date']}\t{rate['currency']}\t{rate['rate']}")

# асинхронная запись в файл
async def log_exchange_command(message):
    log_file_path = aiopath.Path('exchange.log')

    async with aiofile.async_open(log_file_path, mode='a') as file:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f'{timestamp}: {message}\n'
        await file.write(log_entry)

async def handle_message(websocket, path):
    # Получаем сообщение от клиента
    message = await websocket.recv()

    # Записываем лог в файл
    await log_exchange_command(message)

    # Остальной код обработки команды exchange
    # ...


if __name__ == "__main__":
    app = ConsoleApp()
    asyncio.run(app.run())
