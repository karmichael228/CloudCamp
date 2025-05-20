import json
import os
import socket
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, Tuple, Optional
from datetime import datetime


logging_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=logging_format)
logger = logging.getLogger('echo_service')


def fetch_system_info() -> Dict[str, Any]:
    """
    Получает информацию о системе для возвращения в ответах.

    Функция собирает имя хоста, IP-адрес и имя автора из переменных окружения.
    Также, на всякий, добавил метку времени для целей отладки.
    """
    hostname = socket.gethostname()
    
    try:
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(("8.8.8.8", 80)) 
        ip_address = temp_socket.getsockname()[0]
        temp_socket.close()
    except Exception:
        ip_address = socket.gethostbyname(hostname)
    
    author = os.environ.get('AUTHOR', 'Unknown')
    
    system_data = {
        "hostname": hostname,
        "ip_address": ip_address,
        "author": author,
        "timestamp": datetime.now().isoformat(),
    }
    
    return system_data


class EchoResponder(BaseHTTPRequestHandler):
    """
    Обработчик HTTP-запросов, возвращающий информацию о системе.

    Решил не использовать фреймворк, чтобы минимизировать зависимости, но оставил модульность.
    """
    
    def _set_json_headers(self) -> None:
        """Устанавливает заголовки ответа для JSON-контента"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
    
    def _build_response(self) -> bytes:
        """
        Формирует JSON-ответ с информацией о системе.
        Возвращает байты, готовые для записи в выходной поток.
        """
        info = fetch_system_info()
        logger.info(f"Serving request from {info['hostname']} ({info['ip_address']})")
        return json.dumps(info, indent=2).encode('utf-8')
    
    def do_GET(self) -> None:
        """Обрабатывает все GET-запросы независимо от пути"""
        self._set_json_headers()
        self.wfile.write(self._build_response())
    
    def log_message(self, format: str, *args: Any) -> None:
        """Переопределяет стандартное логирование для использования нашего логгера"""
        logger.info(f"{self.client_address[0]} - {format % args}")


def launch_server(port: int = 8000, bind_addr: str = '0.0.0.0') -> None:
    """
    Запускает HTTP-сервер на указанном порту.

    Args:
        port: TCP-порт для прослушивания (по умолчанию: 8000)
        bind_addr: Адрес для привязки (по умолчанию: все интерфейсы)
    """
    server_address = (bind_addr, port)
    httpd = HTTPServer(server_address, EchoResponder)
    
    logger.info(f"🚀 Echo server starting on http://{bind_addr}:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, shutting down...")
    finally:
        httpd.server_close()
        logger.info("Server stopped.")


if __name__ == "__main__":
    launch_server() 