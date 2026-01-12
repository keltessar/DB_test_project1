from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import time


class BaseDBManager:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.engine = None
        self.SessionLocal = None
        self._init_engine_with_retry()

    def _init_engine_with_retry(self, max_retries=3, delay=2):
        """Пытаемся подключиться с повторными попытками"""
        for attempt in range(max_retries):
            try:
                self._init_engine()
                print(f"✅ Подключение к SQL Server успешно установлено (попытка {attempt + 1})")
                return
            except Exception as e:
                print(f"❌ Попытка {attempt + 1} не удалась: {e}")
                if attempt < max_retries - 1:
                    print(f"⏳ Ждем {delay} секунд перед следующей попыткой...")
                    time.sleep(delay)
                else:
                    raise

    def _init_engine(self):
        """Инициализация движка для SQL Server"""
        self.engine = create_engine(
            self.connection_string,
            echo=False,  # видим SQL запросы в консоли
            pool_pre_ping=True,
            connect_args={
                'timeout': 30,
                'autocommit': True
            }
        )
        self.SessionLocal = sessionmaker(bind=self.engine)

    # def create_tables(self):
    #     """Создание всех таблиц"""
    #     Base.metadata.create_all(self.engine)
    #     print("✅ Таблицы созданы успешно")

    @contextmanager
    def get_session(self):
        """Контекстный менеджер для сессии"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def dispose(self):
        """Очистка ресурсов"""
        if self.engine:
            self.engine.dispose()