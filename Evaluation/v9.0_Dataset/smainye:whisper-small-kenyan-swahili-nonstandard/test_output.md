# Evaluation Report: Whisper Small (Kenya Swahili - Non-Standard Speech) - Test Set

This report summarizes the performance of the `smainye/whisper-small-kenyan-swahili-nonstandard` model on the **test set**.

## Metrics Defined

*   **Word Error Rate (WER):** A metric for measuring the performance of an automatic speech recognition system. It is the number of errors (substitutions, deletions, and insertions) divided by the number of words in the reference transcript. A lower WER indicates better performance.
*   **Character Error Rate (CER):** Similar to WER, but operates at the character level. It is the number of character-level errors divided by the number of characters in the reference transcript. A lower CER indicates better performance.

## 1. Overall Results

This summary is based on the evaluation of **554 examples** from the test set.

| Metric | Overall (corpus-level) | Average (utterance-level) |
| :--- | :--- | :--- |
| **WER** | 0.300 | 0.296 |
| **CER** | 0.119 | 0.118 |

### Explanation
*   **Performance:** The model achieves an overall WER of **30%** on the test set, which is notably better than the 35.6% WER observed on the development set.
*   **Consistency:** The corpus-level and utterance-level averages are very close (0.300 vs 0.296), suggesting consistent performance across utterances of varying lengths.

---

## 2. Per-Severity Results

The following table shows the model's performance aggregated by the severity of the speaker's speech impairment.

| Severity | Average WER | Speaker Count | Avg Utterances/Speaker | Average CER |
| :--- | :--- | :--- | :--- | :--- |
| **mild** | 0.25 | 3 | 83.33 | 0.09 |
| **moderate** | 0.32 | 3 | 66.67 | 0.14 |
| **severe** | 0.35 | 3 | 34.67 | 0.16 |

### Explanation
This table breaks down performance by speech impairment severity: **mild**, **moderate**, and **severe**.

*   **Expected Trend:** Unlike the development set, the test set results follow the expected trend where performance degrades as severity increases. **Mild** speech has the lowest WER (0.25), followed by **moderate** (0.32), and **severe** speech has the highest error rate (0.35).
*   **Data Balance:** Each severity category has an equal number of speakers (3), providing a balanced view, though the number of utterances varies.

---

## 3. Per-Speaker Results

This table breaks down the performance by individual speaker, providing the most granular view of model behavior.

| Speaker ID | Severity | Etiology | Average WER | Utterance Count | Average CER |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **KES013** | mild | Cerebral Palsy | 0.40 | 89 | 0.17 |
| **KES021** | mild | Parkinson’s Disease | 0.18 | 109 | 0.05 |
| **KES030** | mild | Neurodevelopmental disorder | 0.19 | 52 | 0.07 |
| **KES012** | moderate | Neurodevelopmental disorder | 0.20 | 91 | 0.07 |
| **KES028** | moderate | Cerebral Palsy | 0.41 | 30 | 0.18 |
| **KES035** | moderate | Multiple Sclerosis (MS) | 0.36 | 79 | 0.16 |
| **KES001** | severe | Cerebral Palsy | 0.23 | 7 | 0.13 |
| **KES002** | severe | Cerebral Palsy | 0.32 | 51 | 0.14 |
| **KES010** | severe | Neurodevelopmental disorder | 0.51 | 46 | 0.21 |

### Explanation
*   **Top Performers:** Speakers **`KES021`** (mild, Parkinson’s) and **`KES030`** (mild, Neurodevelopmental) had the best results with WERs below 20%.
*   **Outliers:** 
    *   **`KES013`** (mild, Cerebral Palsy) performed significantly worse (40% WER) than other mild speakers, skewing the mild category average upwards.
    *   **`KES001`** (severe, Cerebral Palsy) had a surprisingly good WER of 23%, though this is based on a very small sample size (7 utterances).
*   **Most Challenging Speaker:** Speaker **`KES010`** (severe, Neurodevelopmental disorder) presented the greatest challenge with a WER of **51%**.

---

## 4. Per-Etiology Results

The following table aggregates performance based on the underlying cause (etiology) of the speech impairment.

| Etiology | Average WER | Speaker Count | Avg Utterances/Speaker | Average CER |
| :--- | :--- | :--- | :--- | :--- |
| **Cerebral Palsy** | 0.34 | 4 | 44.25 | 0.15 |
| **Multiple Sclerosis (MS)** | 0.36 | 1 | 79.00 | 0.16 |
| **Neurodevelopmental disorder** | 0.30 | 3 | 63.00 | 0.11 |
| **Parkinson’s Disease** | 0.18 | 1 | 109.00 | 0.05 |

### Explanation
*   **Best Performance:** The model performed best on speech associated with **Parkinson’s Disease** (18% WER), though this is based on a single speaker.
*   **Consistent Difficulty:** **Cerebral Palsy** (34% WER) and **Multiple Sclerosis** (36% WER) presented similar levels of difficulty for the model. 
*   **Neurodevelopmental Disorders:** This category fell in the middle with a 30% WER, averaging out excellent performance from some speakers (KES012, 20% WER) and poor performance from others (KES010, 51% WER).
