### Swahili Dev Set Results (whisper-small)

Here are the results from the evaluation on the Swahili dev set using the `whisper-small` model for the kenyan_swahili_nonstandard_speech_v0.9 dataset.

#### Overall WER & CER Summary

This summary is based on the evaluation of **272 examples**

The evaluation of the `whisper-small` model on the Swahili development set shows a near-complete failure to transcribe the audio correctly. The Word Error Rate (WER) is close to 100%, and the Character Error Rate (CER) is around 80%.

| Metric | Overall (Normalized) |
| :--- | :--- |
| **WER** | ~99% |
| **CER** | ~80% |

#### Per-Severity Summary

| Severity | WER (mean) | CER (mean) |
| :--- | :---: | :---: |
| Mild | 98% | 80% |
| Moderate | 99% | 80% |
| Severe | 100% | 80% |

**Summary:**

*   The model fails across all severity levels.

#### Per-Speaker Summary

| Speaker ID | Severity | Etiology | WER | CER |
| :--- | :--- | :--- | :---: | :---: |
| KES004 | severe | Neurological disorder | 100% | 80% |
| KES005 | moderate | Neurological disorder | 99% | 80% |
| KES006 | mild | Cerebral Palsy | 100% | 80% |
| KES007 | severe | Cerebral Palsy | 100% | 80% |
| KES018 | mild | Multiple Sclerosis (MS) | 96% | 80% |
| KES020 | moderate | Parkinson’s Disease | 99% | 80% |

**Summary:**

*   The model fails for all speakers.

### English Dev Set Results (whisper-small)

Here are the results from the evaluation on the English development set using the `whisper-small` model for the kenyan_English_nonstandard_speech_v0.9 dataset.

#### Overall WER & CER Summary

This summary is based on the evaluation of **342 examples**.

| Metric | Overall (Normalized) |
| :--- | :--- |
| **WER** | 30.3% |
| **CER** | 21.7% |

#### Per-Severity Summary

| Severity | WER (Mean) | CER (Mean) |
| :--- | :--- | :--- |
| Mild | 0.24 | 0.13 |
| Moderate | 0.30 | 0.19 |
| Severe | 0.30 | 0.18 |

#### Per-Speaker Summary

| Speaker ID | Severity | Etiology | WER Mean | CER Mean |
| :--- | :--- | :--- | :--- | :--- |
| KES006 | mild | Cerebral Palsy | 0.29 | 0.16 |
| KES018 | mild | Multiple Sclerosis (MS) | 0.18 | 0.09 |
| KES005 | moderate | Neurological disorder | 0.27 | 0.20 |
| KES020 | moderate | Parkinson’s Disease | 0.32 | 0.18 |
| KES004 | severe | Neurological disorder | 0.28 | 0.17 |
| KES007 | severe | Cerebral Palsy | 0.32 | 0.18 |

#### Per-Etiology Summary

| Etiology | WER Mean | CER Mean |
| :--- | :--- | :--- |
| Cerebral Palsy | 0.30 | 0.17 |
| Multiple Sclerosis (MS) | 0.18 | 0.09 |
| Neurological disorder | 0.28 | 0.18 |
| Parkinson’s Disease | 0.32 | 0.18 |

### Explanation of Results

The `whisper-small` model shows a dramatic difference in performance between the two languages.

*   **Swahili:** The model has completely failed on the Swahili development set. A WER of ~99% means that it is not transcribing the language correctly at all. This is likely due to the lack of Swahili data in the model's pre-training.
*   **English:** The performance on the English development set is much better, with a WER of around 30%. While this is still a high error rate, it shows that the model has a foundational understanding of English. The error rates increase with severity, and there is significant variability between speakers.

