### Per Severity Summary Table (Test Set)

| Severity | WER Mean | WER Count | CER Mean | CER Count |
| :--- | :--- | :--- | :--- | :--- |
| Mild | 0.11 | 94 | 0.07 | 94 |
| Moderate | 0.17 | 68 | 0.11 | 68 |
| Severe | 0.14 | 73 | 0.07 | 73 |

*Note: The `count` values have been rounded to the nearest whole number.*

### Summary

This table breaks down the model's performance on the test set by the severity of the speech impairment.

- **Best Performance**: The model performed best on the `mild` category, achieving the lowest Word Error Rate (WER) of **11%** and a Character Error Rate (CER) of **7%**.
- **Unexpected Result**: Contrary to the trend observed in the development set (where errors increased with severity), the `severe` category (WER 14%, CER 7%) shows better performance than the `moderate` category (WER 17%, CER 11%). The CER for `severe` cases is surprisingly as low as for `mild` cases.
- **Interpretation**: This anomaly suggests that the specific speakers or utterances within the `severe` slice of the test set may have been less challenging for the model than those in the `moderate` slice. For instance, speaker `KES001` (severe) had a low WER of 12%, which is better than some speakers in the moderate category. This highlights the variability within severity labels and the importance of speaker-level analysis.
