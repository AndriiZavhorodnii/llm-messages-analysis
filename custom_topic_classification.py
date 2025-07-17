# -*- coding: utf-8 -*-
"""
Custom Topic & Sub-Topic Classification using Zero-Shot Learning (Optimized & Fast Model)

This script classifies review sentences into a predefined hierarchy. This version
uses a LIGHTWEIGHT and FAST model ('Moritz/distilbert-base-uncased-mnli') for
significantly faster processing time.
"""

# =============================================================================
# Крок 1: Імпорт бібліотек та визначення ієрархії топіків
# =============================================================================
import pandas as pd
from transformers import pipeline
import torch
from tqdm import tqdm

print("="*60)
print("Ініціалізація ШВИДКОГО скрипту класифікації...")
print("="*60)

# Визначаємо вашу ієрархію топіків, взяту з зображення
TOPIC_HIERARCHY = {
    "App Functionality & User Experience (UX/UI)": [
        "App Performance", "User Interface", "General Usability"
    ],
    "Content Quality & Variety": [
        "Content Relevance", "Summaries Quality", "Book Selection"
    ],
    "Pricing, Subscription & Billing Issues": [
        "Subscription Complaints", "Billing Problems", "Cancellation & Refund Issues", "Misleading Advertising"
    ],
    "Customer Support Experience": [
        "Responsiveness", "Helpfulness", "Overall Negative Experience"
    ],
    "Personal Growth & Learning Experience": [
        "Knowledge Gain", "Habit Formation", "Alternative to Social Media"
    ],
    "Audio Features & Narration": [
        "Audio Quality", "Narration Style", "Human vs. AI Voice"
    ],
    "Language & Localization": [
        "Language Options", "Localization Issues"
    ]
}

# Створюємо список основних топіків для першого етапу класифікації
MAIN_TOPICS = list(TOPIC_HIERARCHY.keys())
print("✅ Ієрархію топіків успішно завантажено.")

# =============================================================================
# Крок 2: Завантаження даних та ШВИДКОЇ моделі
# =============================================================================
print("\n--- Крок 2/4: Завантаження даних та Zero-Shot моделі ---")

# Завантажуємо датасет
file_path = '/Users/user/PycharmProjects/genesis-analytics-game/llm-messages-analysis/df/expanded_df.csv'
try:
    df = pd.read_csv(file_path)
    df.dropna(subset=['sentence'], inplace=True)
    df['sentence'] = df['sentence'].astype(str)
    print(f"✅ Датасет успішно завантажено. Кількість речень: {len(df):,}")
except FileNotFoundError:
    print(f"❌ ПОМИЛКА: Файл не знайдено: {file_path}")
    exit()

# --- ОПЦІЙНО: Використання вибірки для швидкого тестування ---
# df = df.head(1000).copy()
# print(f"⚠️ УВІМКНЕНО РЕЖИМ ВИБІРКИ! Обробка перших {len(df)} речень.")

# Перевірка наявності та вибір пристрою (GPU/CPU)
device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"
print(f"⚡️ Обрано пристрій для обчислень: {device.upper()}")

# --- ВИКОРИСТАННЯ ШВИДКОЇ МОДЕЛІ ---
model_name = "valhalla/distilbart-mnli-12-3"
print(f"⏳ Завантаження ШВИДКОЇ моделі '{model_name}'... Це займе менше часу.")
classifier = pipeline(
    "zero-shot-classification",
    model=model_name,
    device=device
)
print("✅ Модель успішно завантажена.")


# =============================================================================
# Крок 3: Пакетна класифікація (Оптимізована логіка з tqdm)
# =============================================================================
print("\n--- Крок 3/4: Виконання ієрархічної класифікації в пакетному режимі ---")

sentences_to_classify = df['sentence'].tolist()
BATCH_SIZE = 32 # Можна збільшити батч для меншої моделі

# --- Етап 1: Пакетна класифікація за ОСНОВНИМ топіком з прогрес-баром ---
print(f"⏳ Етап 1: Класифікація за основними топіками... (батчі по {BATCH_SIZE})")
main_topic_results_list = []

# Ручна ітерація по батчах з tqdm для візуалізації прогресу
for i in tqdm(range(0, len(sentences_to_classify), BATCH_SIZE), desc="Основні топіки"):
    batch = sentences_to_classify[i:i + BATCH_SIZE]
    if not batch: # Пропускаємо пустий батч в кінці, якщо є
        continue
    results = classifier(
        batch,
        candidate_labels=MAIN_TOPICS,
        multi_label=False
    )
    # classifier повертає список результатів для батча, тому розширюємо список
    main_topic_results_list.extend(results)

df['Main Topic'] = [res['labels'][0] for res in main_topic_results_list]
print("✅ Етап 1: Основні топіки класифіковано.")


# --- Етап 2: Пакетна класифікація за САБ-топіками з прогрес-баром ---
print("\n⏳ Етап 2: Класифікація за саб-топіками...")
df['Sub-Topic'] = "N/A" # Створюємо колонку зі значенням за замовчуванням

# Групуємо речення за знайденим основним топіком
grouped_topics = df.groupby('Main Topic')
# Використовуємо tqdm для візуалізації прогресу по групах
for main_topic, group_df in tqdm(grouped_topics, total=len(grouped_topics), desc="Обробка груп саб-топіків"):
    sub_topic_candidates = TOPIC_HIERARCHY.get(main_topic)

    # Перевіряємо, чи є для цієї групи саб-топіки та речення
    if not sub_topic_candidates or group_df.empty:
        continue

    print(f"  -> Обробка групи '{main_topic}' ({len(group_df)} речень)...")
    
    group_sentences = group_df['sentence'].tolist()
    
    # Класифікуємо тільки речення поточної групи
    sub_topic_results = classifier(
        group_sentences,
        candidate_labels=sub_topic_candidates,
        batch_size=BATCH_SIZE,
        multi_label=False
    )
    
    # Оновлюємо значення 'Sub-Topic' тільки для цієї групи
    predicted_sub_topics = [res['labels'][0] for res in sub_topic_results]
    df.loc[group_df.index, 'Sub-Topic'] = predicted_sub_topics

print("\n✅ Класифікацію успішно завершено!")


# =============================================================================
# Крок 4: Збереження та перегляд результатів
# =============================================================================
print("\n--- Крок 4/4: Збереження та перегляд результатів ---")

# Зберігаємо результат у новий CSV файл
output_file_path = '/Users/user/PycharmProjects/genesis-analytics-game/llm-messages-analysis/df/expanded_df_with_custom_topics_fast_model.csv'
df.to_csv(output_file_path, index=False)

print(f"✅ Результати збережено у файл: {output_file_path}")

print("\nПриклад даних з кастомними топіками:")
print(df[['sentence', 'Main Topic', 'Sub-Topic']].head(10))

print("\nРозподіл за основними топіками:")
print(df['Main Topic'].value_counts())

print("\n" + "="*60)
print("✅ Скрипт завершив роботу!")
print("="*60) 