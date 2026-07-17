# Quantitative-Comparison-of-Eilleen-Chang-s-Language-Styles

A quantitative analysis of Eileen Chang's language style evolution from her Shanghai period (1940s) to her American period (1970s). This project applies computational methods from Digital Humanities to Chinese literature.

## Research Question

How did Eileen Chang's language style change between her early works in Shanghai and her later works in the United States?

## Data

| Period | Works | Year |
|--------|-------|------|
| Shanghai | The Golden Cangue (金锁记), The First Incense (第一炉香) | 1943 |
| America | The Rice Sprout Song (怨女), Little Reunion (小团圆) | 1970s |

## Methods

- **Segmentation**: jieba Chinese tokenizer
- **Lexical Diversity**: Type-Token Ratio (TTR)
- **Spatial Density**: Custom keyword counts (indoor/outdoor/threshold spaces)
- **Sentiment Analysis**: Positive/negative word ratio using custom lexicon

## Key Findings

| Metric | Shanghai Period | America Period | Change |
|--------|----------------|----------------|--------|
| Lexical Diversity (TTR) | 0.277 | 0.301 | ↑ +8.7% |
| Indoor Word Density | 1.87 | 1.25 | ↓ -33% |
| Sentiment (Positive Ratio) | 0.75 | 0.73 | ↓ -2.7% |

**Interpretation:**

1. **Vocabulary became more diverse** — TTR increased from 0.277 to 0.301, suggesting greater lexical variation in her later works.
2. **Spatial imagery shifted** — Indoor word density dropped by 33%, indicating less interior-focused narration in the American period.
3. **Emotional tone remained stable** — Sentiment showed minimal change, suggesting consistent emotional intensity across periods.

However, note that *The Rice Sprout Song* (怨女) is a notable outlier — with the lowest TTR (0.213), lowest indoor density (0.38), and lowest sentiment score (0.625) among all works.

## Files

| File | Description |
|------|-------------|
| `preprocess_final.py` | Text cleaning and tokenization |
| `analyze_final.py` | Main analysis script |
| `analyze_simple.py` | Simplified version for debugging |
| `data/raw/` | Original texts (UTF-8/GBK) |
| `data/processed/` | Tokenized texts |

## Requirements

```bash
pip install jieba
