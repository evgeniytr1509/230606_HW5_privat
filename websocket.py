import asyncio
import websockets

# Функция, которая будет вызываться при получении сообщения от клиента
async def handle_message(websocket, path):
    # Получаем сообщение от клиента
    message = await websocket.recv()
    
    # Выводим полученное сообщение в консоль
    print(f"Получено сообщение от клиента: {message}")
    
    # Отправляем ответное сообщение клиенту
    response = "Сообщение получено!"
    await websocket.send(response)

# Запуск WebSocket-сервера
async def start_server():
    # Создаем сервер и указываем функцию обработки сообщений
    server = await websockets.serve(handle_message, 'localhost', 8000)

    print("Сервер WebSocket запущен и ожидает подключений...")
    
    # Бесконечный цикл событий для обработки подключений и сообщений
    await asyncio.Future()

# Запускаем сервер
asyncio.run(start_server())