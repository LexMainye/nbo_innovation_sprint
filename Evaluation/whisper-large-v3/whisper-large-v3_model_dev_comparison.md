### Swahili Dev Set Results

Here are the results from the evaluation on the Swahili development set for the kenyan_swahili_nonstandard_speech_v0.9 dataset

#### Overall WER & CER Summary

This summary is based on the evaluation of **272 examples**


| Metric | Overall (Normalized) |
| :--- | :--- |
| **WER** | 72.1% |
| **CER** | 30.6% |

#### Per-Severity Summary

This table breaks down the model's performance on the Swahili development set by the severity of the speech impairment.

| Severity | WER (mean) | CER (mean) |
| :--- | :---: | :---: |
| Mild | 56.0% | 19.0% |
| Moderate | 64.0% | 31.0% |
| Severe | 75.0% | 34.0% |

**Summary:**

*   **Error Trend:** As expected, the Word Error Rate (WER) and Character Error Rate (CER) increase with the severity of the speech impairment.

#### Per-Speaker Summary

This table provides a detailed breakdown of the model's performance for each speaker in the Swahili development set.

| Speaker ID | Severity | Etiology | WER | CER |
| :--- | :--- | :--- | :---: | :---: |
| KES004 | severe | Neurological disorder | 71.7% | 41.1% |
| KES005 | moderate | Neurological disorder | 54.1% | 32.1% |
| KES006 | mild | Cerebral Palsy | 72.1% | 28.2% |
| KES007 | severe | Cerebral Palsy | 79.2% | 26.0% |
| KES018 | mild | Multiple Sclerosis (MS) | 39.7% | 10.2% |
| KES020 | moderate | Parkinson’s Disease | 74.7% | 29.9% |

**Summary:**

*   **Top Performer:** Speaker **`KES018`** (mild, Multiple Sclerosis) had the best results with the lowest WER of **39.7%**.
*   **Most Challenging Speaker:** Speaker **`KES007`** (severe, Cerebral Palsy) was the most challenging, with the highest WER of **79.2%**.

#### Per-Etiology Summary

| Etiology | Average WER | Average CER |
| :--- | :---: | :---: |
| Multiple Sclerosis (MS) | 40.0% | 10.0% |
| Neurological disorder | 63.0% | 37.0% |
| Cerebral Palsy | 76.0% | 27.0% |
| Parkinson’s Disease | 75.0% | 30.0% |

### English Dev Set Results

Here are the results from the evaluation on the English development set for the kenyan_english_nonstandard_speech_v0.9 dataset

#### Overall WER & CER Summary

This summary is based on the evaluation of **342 examples**.

| Metric | Overall (Normalized) | Average (Normalized) |
| :--- | :--- | :--- |
| **WER** | 0.194 | 0.19 |
| **CER** | 0.106 | 0.111 |

#### Per-Severity Summary

| Severity | WER (Mean) | CER (Mean) |
| :--- | :--- | :--- |
| Mild | 0.15 | 0.08 |
| Moderate | 0.20 | 0.13 |
| Severe | 0.23 | 0.14 |

**Summary:**

*   **Performance Trend**: Both Word Error Rate (WER) and Character Error Rate (CER) increase as the severity level rises.

#### Per-Speaker Summary

| Speaker ID | Severity | Etiology | WER Mean | CER Mean |
| :--- | :--- | :--- | :--- | :--- |
| KES006 | mild | Cerebral Palsy | 0.19 | 0.09 |
| KES018 | mild | Multiple Sclerosis (MS) | 0.11 | 0.06 |
| KES005 | moderate | Neurological disorder | 0.17 | 0.12 |
| KES020 | moderate | Parkinson’s Disease | 0.22 | 0.15 |
| KES004 | severe | Neurological disorder | 0.21 | 0.13 |
| KES007 | severe | Cerebral Palsy | 0.26 | 0.14 |

**Summary:**

*   **Best Performance**: The best performance in this set is from speaker KES018 (mild, Multiple Sclerosis), with a WER of 0.11.
*   **Highest Error Rates**: The highest error rates are observed in the `severe` category, with speaker KES007 (Cerebral Palsy) showing the highest WER of 0.26.

#### Per-Etiology Summary

| Etiology | WER Mean | CER Mean |
| :--- | :--- | :--- |
| Cerebral Palsy | 0.22 | 0.12 |
| Multiple Sclerosis (MS) | 0.11 | 0.06 |
| Neurological disorder | 0.19 | 0.13 |
| Parkinson’s Disease | 0.22 | 0.15 |

### Explanation of Results

The development set results show a clearer trend than the test set. For both English and Swahili, the error rates (WER and CER) consistently increase with the severity of the speech impairment. This is the expected behavior and indicates that the development set is well-balanced in terms of difficulty.

*   **English vs. Swahili:** Similar to the test set, the model performs much better on English than on Swahili. The WER for English is around 19.4%, while for Swahili it's a very high 72.1%.
*   **Best and Worst Performance:** For both languages, the speaker with Multiple Sclerosis (`KES018`) has the lowest error rates, and speakers with Cerebral Palsy and Parkinson's Disease have the highest.
