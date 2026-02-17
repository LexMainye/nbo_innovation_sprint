# Comparison of Development vs. Test Set Results

This analysis compares the performance of the `smainye/whisper-small-kenyan-english-nonstandard` model on the development set (`dev_output.md`) versus the test set (`test_output.md`). While the model shows strong performance on both, there are notable differences in the results when broken down by speaker characteristics.

## Summary of Key Differences

### 1. Overall Performance

The model performs significantly **better on the test set** than on the development set across all aggregated severity levels.

| Severity | Test Set WER (mean) | Dev Set WER (mean) | Difference |
| :--- | :---: | :---: | :---: |
| Mild | 8% | 13% | **-5%** |
| Moderate | 15% | 23% | **-8%** |
| Severe | 11% | 16% | **-5%** |

The overall WER on the development set was **14.9%**, while the per-severity results from the test set suggest its overall WER is likely lower, indicating better generalization to the unseen test data.

### 2. Performance Trend by Severity

A key anomaly is present in **both sets**: performance on speakers with "severe" impairment is better than on those with "moderate" impairment.

*   **Dev Set:** `mild` (13%) < `severe` (16%) < `moderate` (23%)
*   **Test Set:** `mild` (8%) < `severe` (11%) < `moderate` (15%)

This consistent pattern suggests that the "severity" label may not perfectly correlate with the difficulty of speech transcription for this model, or that there is high variance in speaker clarity within these categories.

### 3. Performance Inversion by Etiology

The most striking difference is the **complete inversion of performance** for certain etiologies between the two datasets.

| Etiology | Test Set WER (mean) | Dev Set WER (mean) | Performance Rank (Test) | Performance Rank (Dev) |
|:---|:---:|:---:|:---|:---|
| **Parkinson’s Disease** | **7%** | **26%** | **Best** | **Worst** |
| **Multiple Sclerosis (MS)** | **17%** | **10%** | **Worst** | **Best** |
| Cerebral Palsy | 12% | 17% | Mid-tier | Mid-tier |
| Neurological/Neurodev. | 10% | 17% | Good | Mid-tier |

**Explanation:**
This dramatic shift highlights that the model's performance is highly sensitive to the individual speaker, not just the general etiology. For example, the speaker with Parkinson's in the test set (`KES021`, 7% WER) was transcribed much more accurately than the speaker with the same condition in the dev set (`KES020`, 26% WER). The opposite is true for Multiple Sclerosis. This indicates that with a small number of speakers, aggregating by etiology can be misleading and performance is more speaker-dependent.

## Conclusion

While the model generalizes well to the test set, achieving even lower error rates than on the dev set, the evaluation reveals significant performance variance based on the specific speaker. The consistent "severe better than moderate" trend and the inversion of performance for Parkinson's and MS highlight the need for a more extensive and diverse set of speakers for a more stable and reliable evaluation of model performance across different speech impairment conditions.