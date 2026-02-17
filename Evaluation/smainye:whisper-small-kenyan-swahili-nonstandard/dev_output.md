# Evaluation Report: Whisper Small (Kenya Swahili - Non-Standard Speech)

This report summarizes the performance of the `smainye/whisper-small-kenyan-swahili-nonstandard` model on the development set.

## Metrics Defined

*   **Word Error Rate (WER):** A metric for measuring the performance of an automatic speech recognition system. It is the number of errors (substitutions, deletions, and insertions) divided by the number of words in the reference transcript. A lower WER indicates better performance.
*   **Character Error Rate (CER):** Similar to WER, but operates at the character level. It is the number of character-level errors divided by the number of characters in the reference transcript. A lower CER indicates better performance.

## 1. Overall Results

This summary is based on the evaluation of **272 examples** from the development set.

| Metric | Overall (corpus-level) | Average (utterance-level) |
| :--- | :--- | :--- |
| **WER** | 0.356 | 0.333 |
| **CER** | 0.151 | 0.140 |

### Explanation
*   **Overall (corpus-level):** This is the standard way to calculate WER/CER across the entire dataset. It sums all errors and divides by the total number of words/characters in the reference transcripts. It is sensitive to the length of utterances.
*   **Average (utterance-level):** This calculates the WER/CER for each utterance individually and then averages the scores. This can be useful for understanding typical performance on a per-utterance basis, as it weights each utterance equally regardless of length.

---

## 2. Per-Severity Results

The following table shows the model's performance aggregated by the severity of the speaker's speech impairment.

| Severity | Average WER | Speaker Count | Avg Utterances/Speaker | Average CER |
| :--- | :--- | :--- | :--- | :--- |
| **mild** | 0.33 | 2 | 19.5 | 0.13 |
| **moderate** | 0.45 | 2 | 42.0 | 0.21 |
| **severe** | 0.28 | 2 | 74.5 | 0.12 |

### Explanation
This table breaks down performance by speech impairment severity: **mild**, **moderate**, and **severe**.

*   **Counter-Intuitive Result:** Interestingly, the model performs better on **severe** speech (0.28 WER) than on **mild** (0.33 WER) and **moderate** (0.45 WER) speech in this dataset.
*   **Reason:** This is due to the specific speakers in each category. As shown in the per-speaker results below, the "mild" category includes one speaker with excellent recognition (9% WER) and another with very poor recognition (58% WER), averaging out to a higher error rate than the "severe" group, which had more consistent, moderate performance.

---

## 3. Per-Speaker Results

This table breaks down the performance by individual speaker, providing the most granular view of model behavior.

| Speaker ID | Severity | Etiology | Average WER | Utterance Count | Average CER |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **KES006** | mild | Cerebral Palsy | 0.58 | 23 | 0.23 |
| **KES018** | mild | Multiple Sclerosis (MS) | 0.09 | 16 | 0.04 |
| **KES005** | moderate | Neurological disorder | 0.51 | 10 | 0.26 |
| **KES020** | moderate | Parkinson’s Disease | 0.39 | 74 | 0.17 |
| **KES004** | severe | Neurological disorder | 0.33 | 73 | 0.15 |
| **KES007** | severe | Cerebral Palsy | 0.23 | 76 | 0.08 |

### Explanation
*   **Top Performer:** Speaker **`KES018`** (mild, Multiple Sclerosis) had the best results with a very low WER of **9%**.
*   **Most Challenging Speaker:** Speaker **`KES006`** (mild, Cerebral Palsy) was the most difficult for the model, with a WER of **58%**.
*   **Volume Differences:** Notice that the utterance counts vary significantly (from 10 to 76), which can impact the stability of the aggregate metrics for groups with fewer samples.

---

## 4. Per-Etiology Results

The following table aggregates performance based on the underlying cause (etiology) of the speech impairment.

| Etiology | Average WER | Speaker Count | Avg Utterances/Speaker | Average CER |
| :--- | :--- | :--- | :--- | :--- |
| **Cerebral Palsy** | 0.40 | 2 | 49.5 | 0.16 |
| **Multiple Sclerosis (MS)** | 0.09 | 1 | 16.0 | 0.04 |
| **Neurological disorder** | 0.42 | 2 | 41.5 | 0.20 |
| **Parkinson’s Disease** | 0.39 | 1 | 74.0 | 0.17 |

### Explanation
*   **Best Performance:** The model performed exceptionally well on speech from the speaker with **Multiple Sclerosis (MS)** (9% WER).
*   **Challenges:** Both **Cerebral Palsy** and **Neurological Disorder** etiologies presented significant challenges, with average WERs around 40-42%.
