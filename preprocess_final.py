import jieba
import re
import os

def detect_encoding(file_path):
    """Try common encodings"""
    encodings = ['utf-8', 'gbk', 'gb18030', 'utf-16']
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                f.read()
            return enc
        except:
            continue
    return 'gbk'  # fallback

def clean_text(text):
    """Keep only Chinese characters"""
    return re.sub(r'[^\u4e00-\u9fa5]', '', text)

def process_file(input_path, output_path):
    """Process single file: read -> clean -> tokenize -> save"""
    # Auto-detect encoding
    encoding = detect_encoding(input_path)
    print(f'  Reading {os.path.basename(input_path)} with {encoding} encoding')
    
    with open(input_path, 'r', encoding=encoding, errors='ignore') as f:
        text = f.read()
    
    cleaned = clean_text(text)
    words = jieba.lcut(cleaned)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(' '.join(words))
    
    print(f'  ✓ {os.path.basename(input_path)}: {len(words)} words')
    return len(words)

if __name__ == '__main__':
    print('Starting preprocessing...\n')
    
    # Process all files in shanghai folder
    for filename in os.listdir('data/raw/shanghai/'):
        if filename.endswith('.txt'):
            process_file(
                f'data/raw/shanghai/{filename}',
                f'data/processed/shanghai/{filename}'
            )
    
    # Process all files in america folder
    for filename in os.listdir('data/raw/america/'):
        if filename.endswith('.txt'):
            process_file(
                f'data/raw/america/{filename}',
                f'data/processed/america/{filename}'
            )
    
    print('\nPreprocessing completed!')
