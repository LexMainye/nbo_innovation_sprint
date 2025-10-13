# Analysis of Test Set Results for Non-Standard Swahili ASR

## 1. Executive Summary

This document provides a detailed analysis of the performance of a Whisper model on the **test set** of the non-standard Swahili speech dataset.

It is critical to note that the model used for this evaluation was **`openai/whisper-tiny`**. This model was fine-tuned on **English** atypical speech, and then evaluated on **Swahili** atypical speech. This fundamental language mismatch is the primary reason for the extremely high error rates observed. The results confirm that the model cannot effectively transcribe Swahili, as it was never trained on Swahili atypical speech data.

---

## 2. Overall Performance

The model's overall performance on the test set is exceptionally poor, with error rates indicating a near-complete failure to correctly transcribe the audio.

| Metric | Average Score |
| :--- | :---: |
| **Word Error Rate (WER)** | **96.1%** |
| **Character Error Rate (CER)**| **52.8%** |

A WER of 96.1% signifies that, on average, the number of word errors is almost equal to the total number of words in the reference transcript. The CER, while lower, still indicates that approximately half of all characters are incorrectly transcribed.

---

## 3. Performance Breakdown by Etiology

The model's performance varies significantly depending on the speaker's condition, highlighting how different acoustic patterns present unique challenges. The model performed best at the character level on speakers with Parkinson's Disease.

| Etiology | Average WER | Average CER |
| :--- | :---: | :---: |
| Parkinson’s Disease | 93% | **35%** |
| Neurodevelopmental disorder | 95% | 52% |
| Multiple Sclerosis (MS) | 99% | 56% |
| Cerebral Palsy | 99% | 66% |

---

## 4. Performance Breakdown by Severity

As expected, the model's ability to transcribe speech degrades as the severity of the speech impairment increases. This trend is consistent across both WER and CER, with the highest error rates observed in the "severe" category.

| Severity | Average WER | Average CER |
| :--- | :---: | :---: |
| Mild | 93.9% | 45.0% |
| Moderate | 97.6% | 54.3% |
| Severe | 97.7% | 67.8% |

---

## 5. Conclusion

The test set results provide a clear and consistent picture: a model fine-tuned on English atypical speech cannot be used for Swahili atypical speech transcription. The high error rates are not an indication of the model's potential but rather a direct consequence of the language mismatch. The only viable path to achieving a usable performance is to **fine-tune a new model directly on the Swahili non-standard speech dataset.**