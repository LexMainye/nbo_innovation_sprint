### Per-Etiology & Speaker Summary (Test Set)


| speaker_id | severity | etiology | wer (mean) | wer (count) | cer (mean) | cer (count) |
|------------|----------|----------|------------|-------------|------------|-------------|
| KES013 | mild | Cerebral Palsy | 0.13 | 62 | 0.09 | 62 |
| KES021 | mild | Parkinson's Disease | 0.07 | 125 | 0.03 | 125 |
| KES030 | mild | Neurodevelopmental disorder | 0.12 | 95 | 0.09 | 95 |
| KES012 | moderate | Neurodevelopmental disorder | 0.09 | 111 | 0.05 | 111 |
| KES028 | moderate | Cerebral Palsy | 0.25 | 56 | 0.15 | 56 |
| KES035 | moderate | Multiple Sclerosis (MS) | 0.16 | 38 | 0.12 | 38 |
| KES001 | severe | Cerebral Palsy | 0.12 | 62 | 0.06 | 62 |
| KES002 | severe | Cerebral Palsy | 0.16 | 69 | 0.09 | 69 |
| KES010 | severe | Neurodevelopmental disorder | 0.13 | 87 | 0.07 | 87 |

## Summary

This table provides a detailed breakdown of the model's performance for each speaker in the test set.

- **Top Performer**: Speaker **`KES021`** (mild, Parkinson's Disease) achieved the best results with an exceptionally low Word Error Rate (WER) of **7%** and a Character Error Rate (CER) of **3%**.
- **Most Challenging Speaker**: Speaker **`KES028`** (moderate, Cerebral Palsy) proved to be the most challenging, with the highest WER of **25%** and CER of **15%**.
- **Performance Inconsistencies**: The results reveal significant performance variations that are not always aligned with the assigned severity level.
  - Speaker **`KES012`** (moderate) had a WER of only **9%**, outperforming two of the three speakers in the `mild` category.
  - Speaker **`KES001`** (severe) had a WER of **12%**, which was better than one speaker in the `mild` category and two in the `moderate` category.
- **Explaining Aggregate Results**: This speaker-level detail helps explain the unexpected finding in the aggregate severity results, where the `moderate` category had a higher average WER (17%) than the `severe` category (14%). The poor performance on speaker `KES028` significantly increased the average error rate for the `moderate` group.