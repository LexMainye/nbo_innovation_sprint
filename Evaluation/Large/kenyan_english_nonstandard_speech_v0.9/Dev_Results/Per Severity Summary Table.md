### Per Severity Summary Table

| Severity | WER (Mean) | WER (Count) | CER (Mean) | CER(Count) |
| :--- | :--- | :--- | :--- | :--- |
| Mild | 0.15 | 72 | 0.08 | 72 |
| Moderate | 0.20 | 35 | 0.13 | 35 |
| Severe | 0.23 | 64 | 0.14 | 64 |

### Summary

Based on the development set evaluation across 171 samples, there is a clear correlation between the severity of the speech impairment and the model's performance.

- **Performance Trend**: Both Word Error Rate (WER) and Character Error Rate (CER) increase as the severity level rises. The WER goes from **0.15** for `mild` cases to **0.23** for `severe` cases.
- **Sample Distribution**: The `moderate` category has the smallest sample size (35), while the `mild` (72) and `severe` (64) categories are more represented.
- **Overall Performance (Dev Set)**: The weighted average WER for this set is approximately **0.19**, and the weighted average CER is **0.11**. This indicates a notable performance gap when compared to the test set results (WER 0.13, CER 0.08), suggesting the development set may contain more challenging examples.