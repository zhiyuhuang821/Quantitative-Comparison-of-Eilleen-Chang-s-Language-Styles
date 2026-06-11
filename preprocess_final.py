import jieba
import re
import os

def clean_text(text):
    """Keep only Chinese characters"""
    return re.sub(r'[^\u4e00-\u9fa5]', '', text)

def process_file(input_path, output_path):
    """Process single file: read -> clean -> tokenize -> save"""
    with open(input_path, 'r', encoding='gbk', errors='ignore') as f:
        text = f.read()
    
    cleaned = clean_text(text)
    words = jieba.lcut(cleaned)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(' '.join(words))
    
    print(f'✓ {os.path.basename(input_path)}: {len(words)} words')
    return len(words)

if __name__ == '__main__':
    print('Starting preprocessing...\n')
    
    process_file('data/raw/shanghai/金锁记.txt', 'data/processed/shanghai/金锁记.txt')
    process_file('data/raw/america/小团圆.txt', 'data/processed/america/小团圆.txt')
    
    print('\nPreprocessing completed!')
