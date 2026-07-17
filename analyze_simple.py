import re
import os
import glob

def analyze_single_file(filename, period):
    raw_path = f'data/raw/{period}/{filename}'
    processed_path = f'data/processed/{period}/{filename}'
    
    with open(raw_path, 'r', encoding='gbk', errors='ignore') as f:
        raw_text = f.read()
    
    with open(processed_path, 'r', encoding='utf-8') as f:
        words = f.read().split()
    
    sentences = re.split(r'[\r\n。！？；]', raw_text)
    sentences = [s for s in sentences if len(s) > 5]
    avg_len = sum(len(s) for s in sentences) / len(sentences) if sentences else 0
    
    unique_words = len(set(words))
    ttr = unique_words / len(words) if words else 0
    
    print(f'{filename}:')
    print(f'  平均句长: {avg_len:.1f}')
    print(f'  TTR: {ttr:.4f}')
    print(f'  词数: {len(words)}')
    print()

if __name__ == '__main__':
    print('===== 简化版分析 =====\n')
    for f in os.listdir('data/raw/shanghai/'):
        if f.endswith('.txt'):
            analyze_single_file(f, 'shanghai')
    for f in os.listdir('data/raw/america/'):
        if f.endswith('.txt'):
            analyze_single_file(f, 'america')
