###  Summary of WER and CER by Speaker

| Speaker ID | Severity | Etiology                  | WER Mean | WER Count | CER Mean | CER Count |
| :---       | :---     | :------------------------ | :---     | :---      | :---     | :---      |
| KES006     | mild     | Cerebral Palsy            | 0.19     | 50        | 0.09     | 50        |
| KES018     | mild     | Multiple Sclerosis (MS)   | 0.11     | 94        | 0.06     | 94        |
| KES005     | moderate | Neurological disorder     | 0.17     | 10        | 0.12     | 10        |
| KES020     | moderate | Parkinson’s Disease       | 0.22     | 60        | 0.15     | 60        |
| KES004     | severe   | Neurological disorder     | 0.21     | 54        | 0.13     | 54        |
| KES007     | severe   | Cerebral Palsy            | 0.26     | 74        | 0.14     | 74        |


### Summary of Findings (Development Set)

This table breaks down the model's performance on the development set for individual speakers.

- **Performance vs. Severity**: There is a clear trend where error rates increase with the severity of the speech impairment. The average WER for `mild` speakers is approximately 0.14, rising to 0.21 for `moderate` and 0.24 for `severe` speakers. This aligns with the overall severity summary.
- **Individual Variation**: Performance varies significantly even within the same severity level. For instance, among `mild` speakers, KES018 (MS) has a much lower WER (0.11) than KES006 (Cerebral Palsy) at 0.19.
- **Highest Error Rates**: The highest error rates are observed in the `severe` category, with speaker KES007 (Cerebral Palsy) showing the highest WER of 0.26. Speaker KES020 (moderate, Parkinson's Disease) also shows a high WER of 0.22.
- **Best Performance**: The best performance in this set is from speaker KES018 (mild, Multiple Sclerosis), with a WER of 0.11 and a CER of 0.06 over 94 samples.
