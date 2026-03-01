# Evaluation Output Report for smainye/whisper-small-kenyan-english-nonstandard on Test Set

This report summarizes the evaluation results of the `smainye/whisper-small-kenyan-english-nonstandard` model on the **test split** of the `cdli/kenyan_english_nonstandard_speech_v1.0` dataset. The key metrics used for evaluation are Word Error Rate (WER) and Character Error Rate (CER).

* **Word Error Rate (WER):** Measures the proportion of word-level transcription errors. It is computed as the total number of substitutions, deletions, and insertions divided by the total number of reference words. Lower values indicate better recognition performance.

* **Character Error Rate (CER):** Similar to WER but computed at the character level. It measures fine-grained transcription accuracy and is often more stable when evaluating non-standard or dysarthric speech.

---

## Overall Results

* **Overall WER (corpus-level):** 16.7%
* **Overall CER (corpus-level):** 10.1%
* **Average Utterance-level WER:** 15.5%
* **Average Utterance-level CER:** 9.2%

### Explanation

The **corpus-level WER of 16.7%** indicates that approximately 1 in every 6 words is incorrectly transcribed across the entire test set. This metric aggregates all word errors before division and is the standard benchmark used in ASR evaluation.

The **average utterance-level WER (15.5%)** is slightly lower. This metric calculates WER per utterance and then averages across all samples. Differences between corpus-level and utterance-level scores typically arise because longer utterances contribute more heavily to corpus-level metrics.

The **CER of 10.1%** suggests that character-level accuracy remains relatively strong, even when word-level errors occur. This is particularly relevant for non-standard speech, where partial-word distortions are common.

Overall, the results indicate solid transcription performance given the presence of dysarthric and non-standard speech patterns in the dataset.

---

## Per-Severity Results

The following summarizes model performance aggregated by speech impairment severity:

| severity | wer_mean | cer_mean |
| :------- | :------- | :------- |
| mild     | 0.10    | 0.05    |
| moderate | 0.18    | 0.12    |
| severe   | 0.19    | 0.11    |

### Explanation

Performance degrades as speech impairment severity increases:

* **Mild severity** speakers achieve the lowest WER (10%), indicating high intelligibility.
* **Moderate and severe** categories show increased error rates (18–19% WER), reflecting greater articulatory distortion.

The pattern is consistent with expected ASR behavior: as acoustic deviation from standard speech increases, recognition accuracy declines. However, the model maintains reasonable robustness even for severe cases.

---

## Per-Etiology Results

Aggregated by cause of speech impairment:
| etiology                    | wer_mean | cer_mean |  
| :-------------------------- | :------- | :------- | 
| Cerebral Palsy              | 0.19     | 0.11     |              
| Multiple Sclerosis (MS)     | 0.17     | 0.12     |             
| Neurodevelopmental disorder | 0.15     | 0.09     |              
| Parkinson’s Disease         | 0.09     | 0.04     |         


### Explanation

The model performs best on **Parkinson’s Disease speech** and shows higher error rates for **Cerebral Palsy and Multiple Sclerosis**.

This suggests:

* Parkinsonian speech may retain clearer phonemic structure.
* CP and MS speech may introduce greater articulatory irregularities, leading to more substitutions and deletions.

These differences highlight the importance of etiology-aware evaluation when designing inclusive ASR systems.

---

## Summary

The fine-tuned Whisper model achieves:

* **16.7% corpus-level WER**
* **10.1% corpus-level CER**
* Stable performance across 926 utterances
* Expected degradation with increasing impairment severity
* Measurable variation across etiologies

Given the complexity of non-standard Kenyan English speech, these results demonstrate meaningful robustness while identifying areas for further domain-specific improvement.


