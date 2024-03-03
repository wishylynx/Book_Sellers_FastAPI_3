from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError
from typing import List, Optional

__all__ = ["IncomingBook", "ReturnedAllBooks", "ReturnedBook"]


# Базовый класс "Книги", содержащий поля, которые есть во всех классах-наследниках.
class BaseBook(BaseModel):
    title: str
    author: str
    year: int = Field(..., example=2024)
    count_pages: int = Field(default=300, alias="pages")


# Класс для валидации входящих данных. Не содержит id так как его присваивает БД.
class IncomingBook(BaseBook):
    seller_id: int  # Добавляем это поле для связи книги с продавцом

    year: int = Field(default=2024, example=2024)  # Пример присваивания дефолтного значения
    count_pages: int = Field(default=300, alias="pages")  # Пример использования тонкой настройки полей

    @field_validator("year")  # Валидатор, проверяет что дата не слишком древняя
    @staticmethod
    def validate_year(val: int):
        if val < 1900:
            raise PydanticCustomError("Validation error", "Year is wrong!")
        return val


# Класс, валидирующий исходящие данные. Он уже содержит id
class ReturnedBook(BaseBook):
    id: int
    count_pages: int
    seller_id: Optional[int]

# Класс для возврата массива объектов "Книга"
class ReturnedAllBooks(BaseModel):
    books: list[ReturnedBook]
