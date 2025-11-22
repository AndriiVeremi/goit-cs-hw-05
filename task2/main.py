import requests
import re
from collections import defaultdict, Counter 
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor

def get_text(url):
    """Завантажує текст з URL-адреси."""
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.text
    except requests.RequestException as e:
        print(f"Помилка під час завантаження URL {url}: {e}")
        return None

def clean_and_split_text(text):
    """Очищує текст від пунктуації та розбиває на слова."""
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)
    return words

# Map функція 
def map_function(words_chunk):
    """Мапує слова"""
    return [(word, 1) for word in words_chunk]

# Shuffle функція 
def shuffle_function(mapped_values):
    """Групує значення за ключем."""
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items() 

# Reduce функція 
def reduce_function(shuffled_values):
    """Зменшує згруповані значення."""
    reduced = {}
    for key, values in shuffled_values:
        reduced[key] = sum(values)
    return reduced

def map_reduce_orchestrator(text, num_threads=4):
    """
    MapReduce для підрахунку частоти слів.
    """
    all_words = clean_and_split_text(text)
    
    chunk_size = len(all_words) // num_threads if len(all_words) >= num_threads else 1
    chunks = [all_words[i:i + chunk_size] for i in range(0, len(all_words), chunk_size)]
    
    all_mapped_values = []
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = executor.map(map_function, chunks)
        for mapped_chunk_result in results:
            all_mapped_values.extend(mapped_chunk_result) 

    shuffled_results = shuffle_function(all_mapped_values)
    final_reduced_result = reduce_function(shuffled_results)
    return Counter(final_reduced_result)

def visualize_top_words(word_counts, top_n=10):
    """Візуалізує топ найчастіше вживаних слів."""
    if not word_counts:
        print("Немає даних для візуалізації.")
        return

    top_words = word_counts.most_common(top_n)
    words, counts = zip(*top_words)

    plt.figure(figsize=(10, 6))
    plt.barh(words, counts, color='skyblue')
    plt.xlabel('Частота')
    plt.ylabel('Слова')
    plt.title(f'Топ-{top_n} найчастіше вживаних слів')
    plt.gca().invert_yaxis()  
    plt.tight_layout()
    plt.savefig('word_frequency.png')
    print("Графік збережено у файл 'word_frequency.png'")


if __name__ == "__main__":
    # URL для прикладу 
    URL = "https://www.gutenberg.org/files/66933/66933-0.txt"

    text_content = get_text(URL)

    if text_content:
        word_counts = map_reduce_orchestrator(text_content)
        visualize_top_words(word_counts, top_n=15)