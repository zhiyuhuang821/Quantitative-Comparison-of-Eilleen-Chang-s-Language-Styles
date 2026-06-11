import jieba
import os
import re

# 文本清洗函数
def clean_text(text):
    # 移除英文和数字
    text = re.sub(r'[a-zA-Z0-9]', '', text)
    # 移除多余空格和换行
    text = re.sub(r'\s+', '', text)
    return text.strip()

# 处理单个文件
def process_one_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        raw = f.read()
    
    cleaned = clean_text(raw)
    words = jieba.lcut(cleaned)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(' '.join(words))
    
    print(f"处理完成: {input_path} -> {len(words)} 个词")
    return len(words)

# 批量处理
def process_all():
    periods = ['shanghai', 'america']
    total_stats = {}
    
    for period in periods:
        raw_folder = f'data/raw/{period}/'
        processed_folder = f'data/processed/{period}/'
        
        # 确保输出文件夹存在
        os.makedirs(processed_folder, exist_ok=True)
        
        for filename in os.listdir(raw_folder):
            if filename.endswith('.txt'):
                input_path = os.path.join(raw_folder, filename)
                output_path = os.path.join(processed_folder, filename)
                word_count = process_one_file(input_path, output_path)
                total_stats[filename] = word_count
    
    print("\n===== 处理完成 =====")
    for f, count in total_stats.items():
        print(f"{f}: {count} 词")

# 运行
if __name__ == '__main__':
    process_all()
