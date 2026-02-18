# Comparison of Development vs. Test Set Results

This report compares the evaluation results of the `smainye/whisper-small-kenyan-english-nonstandard` model on the **Development** and **Test** splits of the `cdli/kenyan_english_nonstandard_speech_v0.9` dataset.

## Executive Summary

The model performs significantly better on the **Test set** across almost all metrics and categories compared to the Development set.
*   **Overall WER** improved from **14.9%** (Dev) to **9.8%** (Test).
*   **Overall CER** improved from **8.0%** (Dev) to **5.0%** (Test).

This suggests that the model generalizes well to the test data, or potentially that the test set contains slightly easier examples (e.g., clearer recordings or less severe impairments on average) than the development set.

## 1. Overall Performance Comparison

| Metric | Dev Set | Test Set | Absolute Change | Relative Improvement |
| :--- | :--- | :--- | :--- | :--- |
| **Overall WER** | 14.9% | 9.8% | -5.1% | ~34% |
| **Overall CER** | 8.0% | 5.0% | -3.0% | ~37% |
| **Avg Utterance WER** | 16.4% | 10.6% | -5.8% | ~35% |
| **Avg Utterance CER** | 9.3% | 5.4% | -3.9% | ~42% |

## 2. Analysis by Severity

The model consistently performs better on the Test set across all severity levels.

| Severity | Dev WER | Test WER | Dev CER | Test CER | Trend |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Mild** | 0.13 | 0.08 | 0.06 | 0.04 | ✅ Improved |
| **Moderate** | 0.23 | 0.15 | 0.14 | 0.09 | ✅ Improved |
| **Severe** | 0.16 | 0.11 | 0.09 | 0.06 | ✅ Improved |

*   **Observation:** The relative hierarchy remains similar: "Mild" is essentially the easiest, followed by "Severe", with "Moderate" actually showing the highest error rates in both sets (possibly due to specific speaker characteristics in the "Moderate" bucket).

## 3. Analysis by Etiology

Performance varies significantly by etiology, likely due to small sample sizes (some etiologies have only 1-2 speakers).

| Etiology | Dev WER | Test WER | Change |
| :--- | :--- | :--- | :--- |
| **Cerebral Palsy** | 0.17 | 0.12 | ✅ Improved |
| **Neuro. Disorder** | 0.17 | 0.10 | ✅ Improved |
| **Parkinson’s** | 0.26 | 0.07 | ✅ **Major Improvement** |
| **Multiple Sclerosis**| 0.10 | 0.17 | ❌ Regressed |

*   **Parkinson's Disease:** Shows the most dramatic improvement (26% WER -> 7% WER). This could be due to speaker-specific differences; the speaker in the test set might have milder symptoms or clearer articulation than the one in the dev set.
*   **Multiple Sclerosis:** This is the only category where performance degraded (10% WER -> 17% WER). However, with very low speaker counts (often N=1), this is likely a speaker-specific variation rather than a general trend for the etiology.

## Conclusion

The evaluation results on the Test set are highly encouraging, showing a roughly **35% relative reduction in error rates** compared to the Development set. The model demonstrates robust performance, particularly on "Mild" and "Severe" impairments, though high variance in specific etiologies (like Parkinson's vs. MS) highlights the impact of individual speaker characteristics in small-data regimes.
