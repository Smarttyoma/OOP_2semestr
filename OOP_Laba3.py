import re
import socket
import sys
from abc import ABC, abstractmethod
from typing import List


class LogFilterProtocol(ABC):
    @abstractmethod
    def match(self, text: str) -> bool:
        pass


class SimpleLogFilter(LogFilterProtocol):
    def __init__(self, pattern: str):
        self.pattern = pattern.lower()

    def match(self, text: str) -> bool:
        return self.pattern in text.lower()


class ReLogFilter(LogFilterProtocol):
    def __init__(self, regex_pattern: str):
        self.regex = re.compile(regex_pattern)

    def match(self, text: str) -> bool:
        return bool(self.regex.search(text))


class LogHandlerProtocol(ABC):
    @abstractmethod
    def handle(self, text: str) -> None:
        pass


class FileHandler(LogHandlerProtocol):
    def __init__(self, filename: str):
        self.filename = filename

    def handle(self, text: str) -> None:
        with open(self.filename, 'a') as f:
            f.write(text + '\n')


class SocketHandler(LogHandlerProtocol):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def handle(self, text: str) -> None:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.sendall((text + '\n').encode('utf-8'))
        except Exception as e:
            print(f"Socket error: {e}", file=sys.stderr)


class ConsoleHandler(LogHandlerProtocol):
    def handle(self, text: str) -> None:
        print(text)


class SyslogHandler(LogHandlerProtocol):
    def handle(self, text: str) -> None:
        print(f"[SYSLOG] {text}")


class Logger:
    def __init__(self,
                 filters: List[LogFilterProtocol] = None,
                 handlers: List[LogHandlerProtocol] = None):
        self.filters = filters or []
        self.handlers = handlers or []

    def log(self, text: str) -> None:
        for filter in self.filters:
            if not filter.match(text):
                return

        for handler in self.handlers:
            handler.handle(text)


if __name__ == "__main__":
    error_filter = SimpleLogFilter("error")
    warning_filter = SimpleLogFilter("warning")
    http_filter = ReLogFilter(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    console_handler = ConsoleHandler()
    file_handler = FileHandler("app.log")
    syslog_handler = SyslogHandler()

    error_logger = Logger(
        filters=[error_filter],
        handlers=[console_handler, file_handler, syslog_handler]
    )

    warning_logger = Logger(
        filters=[warning_filter],
        handlers=[console_handler, file_handler]
    )

    http_logger = Logger(
        filters=[http_filter],
        handlers=[file_handler]
    )

    print("=== Тестирование системы логирования ===")

    error_logger.log("This is an error message")
    error_logger.log("This is a warning message")  # Не должно быть обработано
    warning_logger.log("This is a warning message")
    warning_logger.log("This is an info message")  # Не должно быть обработано
    http_logger.log("Visit our site at https://example.com")
    http_logger.log("This message has no URL")  # Не должно быть обработано

    print("\nСодержимое файла app.log:")
    with open("app.log", 'r') as f:
        print(f.read())