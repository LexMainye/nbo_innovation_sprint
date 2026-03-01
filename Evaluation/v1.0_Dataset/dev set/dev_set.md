# Evaluation Output Report for smainye/whisper-small-kenyan-english-nonstandard on Validation Set

This report summarizes the evaluation results of the `smainye/whisper-small-kenyan-english-nonstandard` model on the **validation split** of the `cdli/kenyan_english_nonstandard_speech_v1.0` dataset. The key metrics used for evaluation are Word Error Rate (WER) and Character Error Rate (CER).

* **Word Error Rate (WER):** A metric for measuring the performance of an automatic speech recognition system. It is the number of errors (substitutions, deletions, and insertions) divided by the number of words in the reference transcript. A lower WER indicates better performance.
* **Character Error Rate (CER):** Similar to WER, but operates at the character level. It is the number of character-level errors divided by the number of characters in the reference transcript. A lower CER indicates better performance.

## Overall Results

* **Overall WER (corpus-level):** 29.7%
* **Overall CER (corpus-level):** 18.7%
* **Average Utterance-level WER:** 22.8%
* **Average Utterance-level CER:** 14.0%

**Explanation:**
The overall corpus-level WER is 29.7%, which is the standard way of measuring performance on a dataset. The average utterance-level WER is lower at 22.8%; this metric is calculated by averaging the WER of each individual utterance and caps the maximum error rate per utterance at 1.0.

## Per-Severity Results

The following table shows the model's performance aggregated by the severity of the speaker's speech impairment.

| severity | wer_mean | cer_mean |
| --- | --- | --- |
| mild | 0.18 | 0.10 |
| moderate | 0.28 | 0.19 |
| severe | 0.25 | 0.16 |

**Explanation:**
The table shows the mean WER and CER for each severity category. From these results, the model performs best on speakers with "mild" speech impairment. In this specific validation set, performance on "severe" impairment (25% WER) is slightly better than on "moderate" impairment (28% WER), likely driven by the specific characteristics or conditions of the speakers in the moderate category.

## Per-Speaker Results

This table breaks down the performance by individual speaker, showing the mean WER and CER for each.

| speaker_id | severity | etiology | wer_mean | cer_mean |
| --- | --- | --- | --- | --- |
| KES018 | mild | Multiple Sclerosis (MS) | 0.13 | 0.07 |
| KES005 | moderate | Neurodevelopmental disorder | 0.21 | 0.14 |
| KES006 | mild | Cerebral Palsy | 0.22 | 0.12 |
| KES007 | severe | Cerebral Palsy | 0.23 | 0.13 |
| KES004 | severe | Neurodevelopmental disorder | 0.28 | 0.19 |
| KES020 | moderate | Parkinson’s Disease | 0.36 | 0.24 |

**Explanation:**
This table provides a more granular view of the model's performance. It shows the WER and CER for each speaker, along with their impairment severity and etiology. This allows for a detailed analysis of which speakers the model performs well or poorly on. For example, speaker `KES020` (Parkinson's Disease) has the highest error rates, while `KES018` (Multiple Sclerosis) has the lowest.

## Per-Etiology Results

The following table shows the model's performance aggregated by the etiology (the cause of the speech impairment).

| etiology | wer_mean | cer_mean |
| --- | --- | --- |
| Multiple Sclerosis (MS) | 0.13 | 0.07 |
| Cerebral Palsy | 0.23 | 0.13 |
| Neurodevelopmental disorder | 0.25 | 0.16 |
| Parkinson’s Disease | 0.36 | 0.24 |

**Explanation:**
This table aggregates the results based on the cause of the speech impairment. The model appears to perform best for speech related to Multiple Sclerosis (MS) and struggles most with speech affected by Parkinson's Disease in this validation set.