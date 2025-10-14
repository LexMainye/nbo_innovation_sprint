### Swahili Test Set Results

Here are the results from the evaluation on the Swahili test set, converted from the CSV files.

#### Overall WER & CER Summary

This summary is based on the evaluation of **554 examples**.

| Metric | Overall (Normalized) |
| :--- | :--- |
| **WER** | 0.49 |
| **CER** | 0.18 |

#### Per-Severity Summary

This table breaks down the model's performance on the Swahili test set by the severity of the speech impairment.

| Severity | WER Mean | WER Count | CER Mean | CER Count |
| :--- | :--- | :--- | :--- | :--- |
| Mild | 0.43 | 3 | 0.16 | 3 |
| Moderate | 0.52 | 3 | 0.20 | 3 |
| Severe | 0.63 | 3 | 0.25 | 3 |

**Summary:**

*   **Error Trend:** As expected, the Word Error Rate (WER) and Character Error Rate (CER) increase with the severity of the speech impairment. The `mild` category has the lowest error rates, while the `severe` category has the highest.
*   **High Error Rates:** The overall error rates are very high across all categories, with the best-performing `mild` category still showing a high WER of 43%. This suggests that the `whisper-large-v3` model struggles significantly with non-standard Swahili speech.

#### Per-Speaker Summary

This table provides a detailed breakdown of the model's performance for each speaker in the Swahili test set.

| speaker_id | severity | etiology | wer (mean) | wer (count) | cer (mean) | cer (count) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| KES013 | mild | Cerebral Palsy | 0.53 | 89 | 0.23 | 89 |
| KES021 | mild | Parkinson’s Disease | 0.36 | 109 | 0.08 | 109 |
| KES030 | mild | Neurodevelopmental disorder | 0.41 | 52 | 0.19 | 52 |
| KES012 | moderate | Neurodevelopmental disorder | 0.42 | 91 | 0.12 | 91 |
| KES028 | moderate | Cerebral Palsy | 0.69 | 30 | 0.31 | 30 |
| KES035 | moderate | Multiple Sclerosis (MS) | 0.46 | 79 | 0.18 | 79 |
| KES001 | severe | Cerebral Palsy | 0.61 | 7 | 0.23 | 7 |
| KES002 | severe | Cerebral Palsy | 0.65 | 51 | 0.25 | 51 |
| KES010 | severe | Neurodevelopmental disorder | 0.62 | 46 | 0.25 | 46 |

**Summary:**

*   **Top Performer:** Speaker **`KES021`** (mild, Parkinson's Disease) had the best results with the lowest WER of **36%** and CER of **8%**.
*   **Most Challenging Speaker:** Speaker **`KES028`** (moderate, Cerebral Palsy) was the most challenging, with the highest WER of **69%** and CER of **31%**.
*   **Variability:** Similar to the English results, there is significant performance variation between speakers, even within the same severity category.

#### Per-Etiology Summary

This table breaks down the model's performance on the Swahili test set by the speaker's underlying condition (etiology).

| etiology | wer (mean) | cer (mean) |
| :--- | :--- | :--- |
| Cerebral Palsy | 0.62 | 0.26 |
| Multiple Sclerosis (MS) | 0.46 | 0.18 |
| Neurodevelopmental disorder | 0.48 | 0.18 |
| Parkinson’s Disease | 0.36 | 0.08 |

**Summary:**

*   **Best Performance:** The model performed best on speech from the speaker with **Parkinson's Disease**, achieving the lowest WER of **36%** and CER of **8%**.
*   **Highest Error Rates:** The highest error rates were observed in the **Cerebral Palsy** category, with a WER of **62%**.

### English Test Set Results

Here are the results from the evaluation on the English test set, as you had them in your markdown files.

#### Overall WER & CER Summary

This summary is based on the evaluation of **705 examples**.

| Metric | Overall (Normalized) | Average (Normalized) |
| :--- | :--- | :--- |
| **WER** | 0.131 | 0.127 |
| **CER** | 0.075 | 0.073 |

#### Per-Severity Summary

| Severity | WER Mean | WER Count | CER Mean | CER Count |
| :--- | :--- | :--- | :--- | :--- |
| Mild | 0.11 | 94 | 0.07 | 94 |
| Moderate | 0.17 | 68 | 0.11 | 68 |
| Severe | 0.14 | 73 | 0.07 | 73 |

**Summary:**

*   **Unexpected Result:** The `severe` category (WER 14%) shows better performance than the `moderate` category (WER 17%). This is counter-intuitive but explained by the speaker-level results.

#### Per-Speaker Summary

| speaker_id | severity | etiology | wer (mean) | wer (count) | cer (mean) | cer (count) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| KES013 | mild | Cerebral Palsy | 0.13 | 62 | 0.09 | 62 |
| KES021 | mild | Parkinson's Disease | 0.07 | 125 | 0.03 | 125 |
| KES030 | mild | Neurodevelopmental disorder | 0.12 | 95 | 0.09 | 95 |
| KES012 | moderate | Neurodevelopmental disorder | 0.09 | 111 | 0.05 | 111 |
| KES028 | moderate | Cerebral Palsy | 0.25 | 56 | 0.15 | 56 |
| KES035 | moderate | Multiple Sclerosis (MS) | 0.16 | 38 | 0.12 | 38 |
| KES001 | severe | Cerebral Palsy | 0.12 | 62 | 0.06 | 62 |
| KES002 | severe | Cerebral Palsy | 0.16 | 69 | 0.09 | 69 |
| KES010 | severe | Neurodevelopmental disorder | 0.13 | 87 | 0.07 | 87 |

**Summary:**

*   **Top Performer:** Speaker **`KES021`** (mild, Parkinson's Disease) achieved the best results with a very low WER of **7%**.
*   **Most Challenging Speaker:** Speaker **`KES028`** (moderate, Cerebral Palsy) had the highest WER of **25%**. The poor performance on this speaker is the primary reason the `moderate` category has a higher average WER than the `severe` category.

#### Per-Etiology Summary

| etiology | wer (mean) | cer (mean) |
| :--- | :--- | :--- |
| Cerebral Palsy | 0.17 | 0.10 |
| Multiple Sclerosis (MS) | 0.16 | 0.12 |
| Neurodevelopmental disorder | 0.12 | 0.07 |
| Parkinson's Disease | 0.07 | 0.03 |

### Explanation of Results

**What are WER and CER?**

*   **Word Error Rate (WER):** This is a standard metric for measuring the performance of a speech recognition system. It calculates the number of errors (substitutions, deletions, and insertions) between the predicted text and the ground truth, divided by the total number of words in the ground truth. A lower WER is better.
*   **Character Error Rate (CER):** Similar to WER, but it calculates errors at the character level instead of the word level. This can be a more granular metric, especially for languages with complex morphology.

**Analysis of the `whisper-large-v3` Model's Performance:**

1.  **English vs. Swahili:** The model performs significantly better on the **Kenyan English** non-standard speech dataset (13.1% WER) compared to the **Kenyan Swahili** dataset (49% WER). This is expected, as the base `whisper-large-v3` model was pre-trained on a massive amount of English data, and has had much less exposure to Swahili.

2.  **Impact of Severity:**
    *   In the **Swahili** evaluation, the error rates increase with the severity of the speech impairment, which is the expected behavior.
    *   In the **English** evaluation, the `moderate` severity category has a higher average WER than the `severe` category. The per-speaker results show that this is due to one particularly challenging speaker in the `moderate` group (`KES028`). This highlights that severity labels alone are not always a perfect predictor of ASR performance and that individual speaker characteristics play a huge role.

3.  **Impact of Etiology:** For both languages, the model performed best on the speaker with **Parkinson's Disease** and struggled most with speakers who have **Cerebral Palsy**. This suggests that the acoustic characteristics of speech affected by Parkinson's are easier for the model to transcribe than the characteristics of speech affected by Cerebral Palsy.

**Conclusion:**

The `whisper-large-v3` model provides a strong baseline for transcribing non-standard **Kenyan English**, with an overall WER of 13.1%. However, its performance on non-standard **Kenyan Swahili** is very poor (49% WER), indicating that the model is not suitable for this task without significant fine-tuning on Swahili data. The results also show that performance can vary greatly between individual speakers, even within the same severity category.

### Recommendations

Based on these results, here are my recommendations for improving the models:

**For Swahili:**

The performance on the Swahili dataset is currently very poor (49% WER), so my priority would be to improve the base model's understanding of Swahili.

*   **Swahili-Specific Finetuning:** My most important recommendation is to finetune the `whisper-large-v3` model on a large, diverse dataset of **standard Swahili speech** before even attempting to finetune on the non-standard speech data. The model's high error rate suggests it lacks a fundamental understanding of Swahili phonetics, grammar, and vocabulary. A good starting point would be to use datasets like Common Voice for Swahili.
*   **Data Augmentation:** For the non-standard Swahili data, I would recommend using data augmentation techniques to increase the size of the training dataset. This could include techniques like changing the speed of the audio, adding background noise, or using SpecAugment.
*   **Targeted Finetuning:** Once the model has a better grasp of standard Swahili, I would recommend a second stage of finetuning on the non-standard Swahili dataset. Given the high variability between speakers, it might be beneficial to experiment with speaker-adaptive finetuning if more data per speaker becomes available.

**For English:**

The model is already performing well on the English dataset (13.1% WER), so my focus here would be on reducing the error rate for the more challenging speakers.

*   **Finetuning on Non-Standard Speech:** While the base model is strong, finetuning it on the non-standard English speech dataset will likely improve its performance, especially for speakers with higher error rates like `KES028`.
*   **Focus on Challenging Speakers:** When finetuning, I would recommend oversampling the data from speakers with the highest WER. This will encourage the model to learn the specific speech patterns of these more challenging speakers.
*   **Analyze Errors:** I would recommend a deeper analysis of the errors for the English predictions. Are the errors concentrated on specific words or phonetic patterns? This analysis could inform further data collection or augmentation strategies. For example, if the model is consistently miss-transcribing certain words, I could add more examples of these words to the training data.
