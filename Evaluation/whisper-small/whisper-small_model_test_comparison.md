### Swahili Test Set Results (whisper-small)

Here are the results from the evaluation on the Swahili test set using the `whisper-small` model for the kenyan_swahili_nonstandard_speech_v0.9 dataset.

### Swahili Test Set Results (whisper-small)

#### Overall WER & CER Summary

The `whisper-small` model has almost completely failed on the Swahili test set, with a Word Error Rate (WER) approaching 100% and a Character Error Rate (CER) of around 76.4%.

This summary is based on the evaluation of **554 examples**.

| Metric | Overall (Normalized) | Average (Normalized) |
| :--- | :--- | :--- |
| **WER** | 100.0% | 83.7% |
| **CER** | 76.4% | 32.8% |

#### Per-Severity Summary

| Severity | WER (mean) | CER (mean) |
| :--- | :---: | :---: |
| Mild | 99% | 80% |
| Moderate | 100% | 80% |
| Severe | 100% | 80% |

**Summary:**

*   The model fails across all severity levels.

#### Per-Speaker Summary

| Speaker ID | Severity | Etiology | WER | CER |
| :--- | :--- | :--- | :---: | :---: |
| KES013 | mild | Cerebral Palsy | 100% | 80% |
| KES021 | mild | Parkinson’s Disease | 98% | 80% |
| KES030 | mild | Neurodevelopmental disorder | 100% | 80% |
| KES012 | moderate | Neurodevelopmental disorder | 100% | 80% |
| KES028 | moderate | Cerebral Palsy | 100% | 80% |
| KES035 | moderate | Multiple Sclerosis (MS) | 100% | 80% |
| KES001 | severe | Cerebral Palsy | 100% | 80% |
| KES002 | severe | Cerebral Palsy | 100% | 80% |
| KES010 | severe | Neurodevelopmental disorder | 100% | 80% |

**Summary:**

*   The model fails for all speakers.

### English Test Set Results (whisper-small)

Here are the results from the evaluation on the kenyan_english_nonstandard_speech_v0.9 dataset test set using the `whisper-small` model.

#### Overall WER & CER Summary

This summary is based on the evaluation of **705 examples**.

| Metric | Overall (Normalized) |
| :--- | :--- |
| **WER** | 17.8% |
| **CER** | 10.1% |

#### Per-Severity Summary

| Severity | WER (Mean) | CER (Mean) |
| :--- | :--- | :--- |
| Mild | 0.16 | 0.08 |
| Moderate | 0.23 | 0.13 |
| Severe | 0.18 | 0.10 |

#### Per-Speaker Summary

| speaker_id | severity | etiology | wer (mean) | cer (mean) |
| :--- | :--- | :--- | :--- | :--- |
| KES013 | mild | Cerebral Palsy | 0.19 | 0.11 |
| KES021 | mild | Parkinson’s Disease | 0.10 | 0.04 |
| KES030 | mild | Neurodevelopmental disorder | 0.18 | 0.10 |
| KES012 | moderate | Neurodevelopmental disorder | 0.15 | 0.07 |
| KES028 | moderate | Cerebral Palsy | 0.35 | 0.21 |
| KES035 | moderate | Multiple Sclerosis (MS) | 0.19 | 0.12 |
| KES001 | severe | Cerebral Palsy | 0.18 | 0.09 |
| KES002 | severe | Cerebral Palsy | 0.20 | 0.12 |
| KES010 | severe | Neurodevelopmental disorder | 0.17 | 0.09 |

#### Per-Etiology Summary

| etiology | wer (mean) | cer (mean) |
| :--- | :--- | :--- |
| Cerebral Palsy | 0.23 | 0.13 |
| Multiple Sclerosis (MS) | 0.19 | 0.12 |
| Neurodevelopmental disorder | 0.17 | 0.09 |
| Parkinson’s Disease | 0.10 | 0.04 |

### Explanation of Results

The test set results for the `whisper-small` model confirm the findings from the development set:

*   **Swahili:** The model is completely unable to transcribe the Swahili test set, with a WER of nearly 100%. This confirms that the model is not suitable for Swahili without significant adaptation.
*   **English:** The model performs much better on the English test set, with an overall WER of 17.8%. This is a reasonable baseline, but there is still significant room for improvement. The error rates are highest for the `moderate` severity category, and speaker `KES028` is a clear outlier with a very high WER of 35%.
