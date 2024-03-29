# Домашнее задание #01 (введение, тестирование)

### 1. Функция оценки сообщения
Реализовать функцию predict_message_mood, которая приниамает на вход строку, экземпляр модели SomeModel и пороги хорошести.
Функция возвращает:
- "неуд", если предсказание модели меньше bad_threshold
- "отл", если предсказание модели больше good_threshold
- "норм" в остальных случаях

```py
class SomeModel:
    def predict(self, message: str) -> float:
        # реализация не важна


def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    ...


assert predict_message_mood("Чапаев и пустота", model) == "отл"
assert predict_message_mood("Вулкан", model) == "неуд"
```

### 2. Генератор для чтения и фильтрации файла
Есть текстовый файл, который может не помещаться в память.
В каждой строке файла фраза или предложение: набор слов, разделенных пробелами (знаков препинания нет).

Генератор должен принимать на вход имя файла или файловый объект и список слов для поиска.
Генератор перебирает строки файла и возвращает только те из них (строку целиком), где встретилось хотя бы одно из слов для поиска.
Поиск должен выполняться по полному совпадению слова без учета регистра.

Например, для строки из файла "а Роза упала на лапу Азора" слово поиска "роза" должно найтись, а "роз" или "розан" - уже нет.

### 3. Тесты в отдельном модуле для каждого пункта

### 4. Перед отправкой на проверку код должен быть прогнан через flake8 и pylint, по желанию еще black

### 5. Покрытие тестов через coverage, отчет в репу

#### Покрытие тестов для первого задания с моделью
<image src="coverage_report_tsk1.png">

#### Покрытие тестов для второго задания с генератором
<image src="coverage_report_tsk2.png">