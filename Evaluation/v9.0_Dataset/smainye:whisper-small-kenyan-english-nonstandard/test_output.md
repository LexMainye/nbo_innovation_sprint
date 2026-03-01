# Evaluation Output Report for smainye/whisper-small-kenyan-english-nonstandard on Test Set

This report summarizes the evaluation results of the `smainye/whisper-small-kenyan-english-nonstandard` model on the **test split** of the `cdli/kenyan_english_nonstandard_speech_v0.9` dataset. The key metrics used for evaluation are Word Error Rate (WER) and Character Error Rate (CER).

*   **Word Error Rate (WER):** A metric for measuring the performance of an automatic speech recognition system. It is the number of errors (substitutions, deletions, and insertions) divided by the number of words in the reference transcript. A lower WER indicates better performance.
*   **Character Error Rate (CER):** Similar to WER, but operates at the character level. It is the number of character-level errors divided by the number of characters in the reference transcript. A lower CER indicates better performance.

## Overall Results

*   **Overall WER (corpus-level):** 9.8%
*   **Overall CER (corpus-level):** 5.0%
*   **Average Utterance-level WER:** 10.6%
*   **Average Utterance-level CER:** 5.4%

**Explanation:**
The overall corpus-level WER is 9.8%, which is the standard way of measuring performance on a dataset. The average utterance-level WER is slightly higher at 10.6%; this metric is calculated by averaging the WER of each individual utterance and can be more sensitive to high error rates on short utterances.

## Per-Severity Results

The following table shows the model's performance aggregated by the severity of the speaker's speech impairment. The results are averaged across speakers for each severity level.

| severity | wer_mean | wer_count | cer_mean | cer_count |
| :--- | :--- | :--- | :--- | :--- |
| mild | 0.08 | 3 | 0.04 | 3 |
| moderate | 0.15 | 3 | 0.09 | 3 |
| severe | 0.11 | 3 | 0.06 | 3 |

**Explanation:**

The table shows the mean WER and CER for each severity category. The `wer_count` and `cer_count` columns indicate the number of speakers in each category. From these results, the model performs best on speakers with "mild" speech impairment. Similar to the development set, performance on "severe" impairment (11% WER) is recorded as better than on "moderate" impairment (15% WER) for this test set.

## Per-Speaker Results

This table breaks down the performance by individual speaker, showing the mean WER and CER for each.

| speaker_id | severity | etiology | wer_mean | wer_count | cer_mean | cer_count |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| KES013 | mild | Cerebral Palsy | 0.10 | 62 | 0.05 | 62 |
| KES021 | mild | Parkinson’s Disease | 0.07 | 125 | 0.03 | 125 |
| KES030 | mild | Neurodevelopmental disorder| 0.07 | 95 | 0.03 | 95 |
| KES012 | moderate | Neurodevelopmental disorder| 0.09 | 111 | 0.05 | 111 |
| KES028 | moderate | Cerebral Palsy | 0.20 | 56 | 0.10 | 56 |
| KES035 | moderate | Multiple Sclerosis (MS) | 0.17 | 38 | 0.12 | 38 |
| KES001 | severe | Cerebral Palsy | 0.08 | 62 | 0.04 | 62 |
| KES002 | severe | Cerebral Palsy | 0.11 | 69 | 0.06 | 69 |
| KES010 | severe | Neurodevelopmental disorder| 0.14 | 87 | 0.07 | 87 |

**Explanation:**

This table provides a more granular view of the model's performance. It shows the WER and CER for each speaker, along with their impairment severity and etiology. The `wer_count` and `cer_count` columns show the number of utterances evaluated for each speaker. This allows for a detailed analysis of which speakers the model performs well or poorly on. For example, speaker `KES028` has the highest WER (0.20) among all speakers in this set, while `KES021` and `KES030` achieve the lowest WER (0.07).

## Per-Etiology Results

The following table shows the model's performance aggregated by the etiology (the cause of the speech impairment).

| etiology | wer_mean | wer_count | cer_mean | cer_count |
|:--- | :--- | :--- | :--- | :--- |
| Cerebral Palsy | 0.12 | 4 | 0.06 | 4 |
| Multiple Sclerosis (MS)| 0.17 | 1 | 0.12 | 1 |
| Neurodevelopmental disorder| 0.10 | 3 | 0.05 | 3 |
| Parkinson’s Disease | 0.07 | 1 | 0.03 | 1 |

**Explanation:**

This table aggregates the results based on the cause of the speech impairment. It shows the mean WER and CER for each etiology. The `wer_count` and `cer_count` columns indicate the number of speakers with each etiology. The model appears to perform best for the speaker with Parkinson's Disease (0.07 WER) and struggles most with Multiple Sclerosis (MS) (0.17 WER) in this test set.
