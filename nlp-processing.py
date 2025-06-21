# -*- coding: utf-8 -*-
"""
NLP Processing with BERTopic

This script performs topic modeling on a dataset of review sentences.
It loads the data, trains a BERTopic model to identify topics and sub-topics,
assigns these topics back to the sentences, and saves the result.
Finally, it generates and displays a topic hierarchy.
"""

# =============================================================================
# Крок 1: Імпорт необхідних бібліотек
# =============================================================================
import pandas as pd
from bertopic import BERTopic
import plotly.io as pio

print("="*60)
print("Ініціалізація скрипту NLP-обробки...")
print("="*60)


# =============================================================================
# Крок 2: Завантаження даних та підготовка
# =============================================================================
print("\n--- Крок 2/5: Завантаження даних та підготовка ---")

# Шлях до вашого файлу
file_path = '/Users/user/PycharmProjects/genesis-analytics-game/llm-messages-analysis/df/expanded_df.csv'

try:
    df = pd.read_csv(file_path)
    print(f"✅ Датасет успішно завантажено з '{file_path}'.")
    print(f"   Кількість речень для аналізу: {len(df):,}")
except FileNotFoundError:
    print(f"❌ ПОМИЛКА: Файл не знайдено за шляхом: {file_path}")
    print("Будь ласка, перевірте шлях до файлу та запустіть скрипт знову.")
    exit()

# Переконуємося, що колонка 'sentence' має текстовий тип і не містить пустих значень
df.dropna(subset=['sentence'], inplace=True)
sentences = df['sentence'].astype(str).tolist()

# --- ОПЦІЙНО: Використання меншої вибірки для тестування ---
# Обробка великої кількості речень може зайняти багато часу.
# Розкоментуйте наступні два рядки, щоб протестувати на меншій вибірці (напр., перші 20,000 речень).
#
# print("\n⚠️ УВІМКНЕНО РЕЖИМ ВИБІРКИ! Обробка перших 20,000 речень.")
# sentences_to_process = sentences[:20000]
# df_to_process = df.head(20000).copy()
#
# Закоментуйте наступні два рядки, якщо використовуєте вибірку
df_to_process = df.copy()
sentences_to_process = sentences

print(f"✅ Дані готові для моделювання. Кількість речень для обробки: {len(sentences_to_process):,}")


# =============================================================================
# Крок 3: Навчання моделі BERTopic
# =============================================================================
print("\n--- Крок 3/5: Ініціалізація та навчання моделі BERTopic ---")
print("⏳ Це може зайняти тривалий час, будь ласка, зачекайте...")

# Створюємо модель. `language="english"` - припускаємо, що більшість відгуків англійською.
# `calculate_probabilities=True` дозволить нам бачити ймовірності тем.
# `verbose=True` буде показувати прогрес обробки.
topic_model = BERTopic(language="english", calculate_probabilities=True, verbose=True)

# Навчаємо модель на наших реченнях
topics, probabilities = topic_model.fit_transform(sentences_to_process)

print("✅ Модель успішно навчена!")


# =============================================================================
# Крок 4: Призначення топіків реченням та збереження результатів
# =============================================================================
print("\n--- Крок 4/5: Додавання топіків до датасету та збереження ---")

# `get_topic_info()` дає нам опис кожної теми
topic_info_df = topic_model.get_topic_info()
print(f"✅ Знайдено {len(topic_info_df) - 1} основних топіків (тема -1 - це 'викиди').")

# Створюємо словник для швидкого доступу до назв тем
topic_id_to_name = topic_info_df.set_index('Topic')['Name'].to_dict()

# Додаємо результати в наш DataFrame
df_to_process['topic_id'] = topics
df_to_process['topic_name'] = df_to_process['topic_id'].map(topic_id_to_name)

# Зберігаємо результат у новий CSV файл
output_file_path = '/Users/user/PycharmProjects/genesis-analytics-game/llm-messages-analysis/df/expanded_df_with_topics.csv'
df_to_process.to_csv(output_file_path, index=False)

print(f"✅ Результати успішно збережено у файл: {output_file_path}")
print("\nПриклад даних зі знайденими топіками:")
print(df_to_process[['sentence', 'topic_id', 'topic_name']].head())


# =============================================================================
# Крок 5: Аналіз ієрархії топіків (Топіки та Саб-топіки)
# =============================================================================
print("\n--- Крок 5/5: Побудова та візуалізація ієрархії топіків ---")

# Налаштовуємо рендерер, щоб графік автоматично відкривався у браузері
pio.renderers.default = "browser"

# Створюємо ієрархічні топіки
try:
    hierarchical_topics = topic_model.hierarchical_topics(sentences_to_process)

    # Візуалізуємо ієрархію
    print("⏳ Генеруємо дендрограму... Графік має відкритися у вашому браузері.")
    fig = topic_model.visualize_hierarchy(hierarchical_topics=hierarchical_topics)
    fig.show()
    
    print("\nТекстове представлення ієрархії:")
    print(hierarchical_topics)
    
except Exception as e:
    print(f"❌ Не вдалося згенерувати ієрархію. Помилка: {e}")

print("\n" + "="*60)
print("✅ Скрипт NLP-обробки завершив роботу!")
print("="*60)
