# Evaluation Output Report for smainye/whisper-small-kenyan-english-nonstandard on Development Set

This report summarizes the evaluation results of the `smainye/whisper-small-kenyan-english-nonstandard` model on the **development split** of the `cdli/kenyan_english_nonstandard_speech_v0.9` dataset. The key metrics used for evaluation are Word Error Rate (WER) and Character Error Rate (CER).

*   **Word Error Rate (WER):** A metric for measuring the performance of an automatic speech recognition system. It is the number of errors (substitutions, deletions, and insertions) divided by the number of words in the reference transcript. A lower WER indicates better performance.
*   **Character Error Rate (CER):** Similar to WER, but operates at the character level. It is the number of character-level errors divided by the number of characters in the reference transcript. A lower CER indicates better performance.

## Overall Results

*   **Overall WER (corpus-level):** 14.9%
*   **Overall CER (corpus-level):** 8.0%
*   **Average Utterance-level WER:** 16.4%
*   **Average Utterance-level CER:** 9.3%

**Explanation:**
The overall corpus-level WER is 14.9%, which is the standard way of measuring performance on a dataset. The average utterance-level WER is slightly higher at 16.4%; this metric is calculated by averaging the WER of each individual utterance and can be more sensitive to high error rates on short utterances.

## Per-Severity Results

The following table shows the model's performance aggregated by the severity of the speaker's speech impairment. The results are averaged across speakers for each severity level.

| severity | wer_mean | wer_count | cer_mean | cer_count |
| :--- | :--- | :--- | :--- | :--- |
| mild | 0.13 | 2 | 0.06 | 2 |
| moderate | 0.23 | 2 | 0.14 | 2 |
| severe | 0.16 | 2 | 0.09 | 2 |

**Explanation:**

The table shows the mean WER and CER for each severity category. The `wer_count` and `cer_count` columns indicate the number of speakers in each category. From these results, the model performs best on speakers with "mild" speech impairment. Interestingly, performance on "severe" impairment (16% WER) is better than on "moderate" impairment (23% WER) for this development set.

## Per-Speaker Results

This table breaks down the performance by individual speaker, showing the mean WER and CER for each.

| speaker_id | severity | etiology | wer_mean | wer_count | cer_mean | cer_count |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| KES006 | mild | Cerebral Palsy | 0.16 | 50 | 0.06 | 50 |
| KES018 | mild | Multiple Sclerosis (MS) | 0.10 | 94 | 0.05 | 94 |
| KES005 | moderate | Neurological disorder | 0.19 | 10 | 0.11 | 10 |
| KES020 | moderate | Parkinson’s Disease | 0.26 | 60 | 0.17 | 60 |
| KES004 | severe | Neurological disorder | 0.14 | 54 | 0.08 | 54 |
| KES007 | severe | Cerebral Palsy | 0.19 | 74 | 0.11 | 74 |

**Explanation:**

This table provides a more granular view of the model's performance. It shows the WER and CER for each speaker, along with their impairment severity and etiology. The `wer_count` and `cer_count` columns show the number of utterances evaluated for each speaker. This allows for a detailed analysis of which speakers the model performs well or poorly on. For example, speaker `KES020` has the highest WER and CER among all speakers in this set, while `KES018` has the lowest.

## Per-Etiology Results

The following table shows the model's performance aggregated by the etiology (the cause of the speech impairment).

| etiology | wer_mean | wer_count | cer_mean | cer_count |
|:--- | :--- | :--- | :--- | :--- |
| Cerebral Palsy | 0.17 | 2 | 0.08 | 2 |
| Multiple Sclerosis (MS)| 0.10 | 1 | 0.05 | 1 |
| Neurological disorder | 0.17 | 2 | 0.09 | 2 |
| Parkinson’s Disease | 0.26 | 1 | 0.17 | 1 |

**Explanation:**

This table aggregates the results based on the cause of the speech impairment. It shows the mean WER and CER for each etiology. The `wer_count` and `cer_count` columns indicate the number of speakers with each etiology. The model appears to perform best for the speaker with Multiple Sclerosis (MS) and struggles most with Parkinson's Disease in this development set.