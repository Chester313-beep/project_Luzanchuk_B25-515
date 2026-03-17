class NewsProcessor:

    def process(self, items):
        processed = []
        for item in items:
            # Пропускаем записи с пустым содержимым (content)
            if not item.content or not item.content.strip():
                continue   # такие записи не попадут в результат

            # Нормализация: удаляем лишние пробелы, приводим к нижнему регистру
            cleaned = ' '.join(item.content.split()).lower()
            item.content = cleaned

            # Вычисляем количество слов
            word_count = len(cleaned.split())
            item.metadata['word_count'] = word_count

            processed.append(item)

        return processed