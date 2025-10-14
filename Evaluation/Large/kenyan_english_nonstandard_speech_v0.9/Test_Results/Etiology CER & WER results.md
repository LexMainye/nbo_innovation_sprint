## Etiology Analysis

| etiology | wer (mean) | wer (mean count) | wer (count mean) | wer (count count) | cer (mean) | cer (mean count) | cer (count mean) | cer (count count) |
|----------|------------|------------------|------------------|-------------------|------------|------------------|------------------|-------------------|
| Cerebral Palsy | 0.17 | 4 | 62.25 | 4 | 0.10 | 4 | 62.25 | 4 |
| Multiple Sclerosis (MS) | 0.16 | 1 | 38.00 | 1 | 0.12 | 1 | 38.00 | 1 |
| Neurodevelopmental disorder | 0.12 | 3 | 97.67 | 3 | 0.07 | 3 | 97.67 | 3 |
| Parkinson's Disease | 0.07 | 1 | 125.00 | 1 | 0.03 | 1 | 125.00 | 1 |

*Note: This table breaks down the model's performance on the test set by the speaker's underlying condition (etiology).*

## Summary
- **Best Performance**: The model performed exceptionally well on speech from the speaker with **Parkinson's Disease**, achieving the lowest Word Error Rate (WER) of **7%** and Character Error Rate (CER) of **3%**. This was the largest group by sample count (125 utterances).
- **Strong Performance**: The **Neurodevelopmental disorder** category also showed strong results, with a WER of **12%** and a CER of **7%** across three speakers.
- **Highest Error Rates**: The highest WER was observed in the **Cerebral Palsy** category at **17%**, averaged across four speakers.
- **Data Imbalance**: It's important to note the imbalance in the number of speakers per category. Parkinson's Disease and Multiple Sclerosis are each represented by only a single speaker, while Cerebral Palsy is represented by four. This may influence the aggregated metrics.