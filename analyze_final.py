import re
import os
import glob

POSITIVE_WORDS = ['好', '美', '爱', '喜', '笑', '乐', '幸福', '快乐', '美丽', '喜欢', '高兴', '温柔', '甜蜜', '浪漫', '希望', '温暖']
NEGATIVE_WORDS = ['恨', '哭', '死', '苦', '痛', '悲', '伤', '怨', '孤独', '寂寞', '痛苦', '悲伤', '绝望', '凄凉', '冷', '暗', '黑']

SPACE_WORDS = {
    'indoor': ['家里', '房间', '床上', '浴室', '厨房', '客厅', '卧室', '房里', '楼上', '楼下'],
    'outdoor': ['街上', '弄堂', '公园', '马路', '戏院', '百货公司', '路边', '桥上', '巷子', '胡同'],
    'threshold': ['门口', '楼梯', '电梯', '走廊', '阳台', '窗边', '窗前', '窗下', '门边', '过道']
}

def detect_encoding(file_path):
    for enc in ['gbk', 'utf-8', 'gb18030']:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                f.read()
            return enc
        except:
            continue
    return 'utf-8'

def analyze_text(raw_text, words_list, title):
    # 关键：用换行符 + 标点分句
    sentences = re.split(r'[\n\r。！？；]', raw_text)
    sentences = [s for s in sentences if len(s) > 5]
    avg_len = sum(len(s) for s in sentences) / len(sentences) if sentences else 0
    
    unique_words = len(set(words_list))
    ttr = unique_words / len(words_list) if words_list else 0
    
    text_concat = ''.join(words_list)
    total_k = len(text_concat) / 1000
    counts = {'indoor': 0, 'outdoor': 0, 'threshold': 0}
    for cat, words in SPACE_WORDS.items():
        for w in words:
            counts[cat] += text_concat.count(w)
    indoor = counts['indoor'] / total_k if total_k > 0 else 0
    outdoor = counts['outdoor'] / total_k if total_k > 0 else 0
    threshold = counts['threshold'] / total_k if total_k > 0 else 0
    
    pos_count = sum(words_list.count(w) for w in POSITIVE_WORDS) if words_list else 0
    neg_count = sum(words_list.count(w) for w in NEGATIVE_WORDS) if words_list else 0
    total_sentiment = pos_count + neg_count
    sentiment = pos_count / total_sentiment if total_sentiment > 0 else 0.5
    
    return {
        'title': title,
        'avg_len': avg_len,
        'ttr': ttr,
        'indoor': indoor,
        'outdoor': outdoor,
        'threshold': threshold,
        'sentiment': sentiment,
        'pos': pos_count,
        'neg': neg_count,
        'total_words': len(words_list)
    }

def process_period(period_name, folder_path):
    results = []
    txt_files = glob.glob(f'{folder_path}/*.txt')
    for raw_path in txt_files:
        filename = os.path.basename(raw_path)
        processed_path = f'data/processed/{period_name}/{filename}'
        print(f'  Analyzing: {filename}')
        try:
            enc = detect_encoding(raw_path)
            with open(raw_path, 'r', encoding=enc, errors='ignore') as f:
                raw_text = f.read()
            with open(processed_path, 'r', encoding='utf-8') as f:
                words = f.read().split()
            if not words:
                print(f'    ⚠️ No words found for {filename}, skipping')
                continue
            result = analyze_text(raw_text, words, filename)
            results.append(result)
        except Exception as e:
            print(f'    ⚠️ Error: {e}')
    return results

if __name__ == '__main__':
    print('===== Eileen Chang: Language Style Analysis =====\n')
    all_results = []
    print('Shanghai Period:')
    all_results.extend(process_period('shanghai', 'data/raw/shanghai'))
    print('\nAmerica Period:')
    all_results.extend(process_period('america', 'data/raw/america'))
    
    print('\n' + '=' * 70)
    print('Individual Results')
    print('=' * 70)
    for r in all_results:
        print(f"\n{r['title']}:")
        print(f"  Words: {r['total_words']}")
        print(f"  Avg sentence length: {r['avg_len']:.1f}")
        print(f"  TTR: {r['ttr']:.4f}")
        print(f"  Indoor: {r['indoor']:.2f} | Outdoor: {r['outdoor']:.2f} | Threshold: {r['threshold']:.2f}")
        print(f"  Sentiment: {r['sentiment']:.3f} (pos:{r['pos']} neg:{r['neg']})")
    
    america_titles = ['小团圆']
    sh_works = [r for r in all_results if not any(t in r['title'] for t in america_titles)]
    us_works = [r for r in all_results if any(t in r['title'] for t in america_titles)]
    
    def avg(lst, key):
        vals = [r[key] for r in lst if r[key] is not None]
        return sum(vals) / len(vals) if vals else 0
    
    print('\n' + '=' * 70)
    print('Period Averages')
    print('=' * 70)
    print(f"{'Metric':<25} {'Shanghai Period':<20} {'America Period':<20}")
    print('-' * 65)
    metrics = ['avg_len', 'ttr', 'indoor', 'outdoor', 'threshold', 'sentiment']
    names = {'avg_len': 'Avg Sentence Length', 'ttr': 'TTR', 'indoor': 'Indoor Density', 
             'outdoor': 'Outdoor Density', 'threshold': 'Threshold Density', 'sentiment': 'Sentiment'}
    for m in metrics:
        print(f"{names[m]:<25} {avg(sh_works, m):<20.2f} {avg(us_works, m):<20.2f}")
    
    print('\n' + '=' * 70)
    print('Key Findings')
    print('=' * 70)
    print(f"1. TTR: Shanghai {avg(sh_works, 'ttr'):.3f} → America {avg(us_works, 'ttr'):.3f}")
    print(f"2. Indoor density: Shanghai {avg(sh_works, 'indoor'):.2f} → America {avg(us_works, 'indoor'):.2f}")
    print(f"3. Sentiment: Shanghai {avg(sh_works, 'sentiment'):.2f} → America {avg(us_works, 'sentiment'):.2f}")
    print('\nAnalysis complete!')
