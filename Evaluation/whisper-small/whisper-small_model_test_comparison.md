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

### Recommendations

Based on these test set results, here are my recommendations for the `whisper-small` model:

**For Swahili:**

My recommendation remains the same as for the dev set: the `whisper-small` model is not a viable starting point for Swahili.

*   **Switch to a Larger, Multilingual Model:** I must switch to a larger, multilingual model like `whisper-large-v3`. The `small` model does not have the necessary linguistic knowledge to handle Swahili.
*   **Focus on Pre-training:** If I were to build a new model from scratch, I would need to ensure that it is pre-trained on a massive amount of Swahili data.

**For English:**

The English test set results are promising and show that the `whisper-small` model can be a viable option with further work.

*   **Finetune on the Non-Standard Data:** My immediate next step should be to finetune the `whisper-small` model on the English non-standard speech dataset. This will help the model to adapt to the specific speech patterns of the speakers.
*   **Address the Outlier Speaker:** Speaker `KES028` has a very high WER. I should investigate the reasons for this. Is it a data quality issue, or is this speaker's speech particularly challenging? I may need to collect more data for this speaker or use targeted data augmentation.
*   **Compare with `whisper-large-v3`:** While the `whisper-small` model is a good starting point, the results from the `large` model show that a larger model can achieve a lower error rate out-of-the-box. I should weigh the trade-offs between model size, inference speed, and accuracy. If accuracy is the primary concern, `whisper-large-v3` is the better choice.
