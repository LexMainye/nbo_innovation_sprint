# My Analysis of Test Set Results for Non-Standard Swahili ASR

## 1. Executive Summary

In this document, I provide a detailed analysis of how a Whisper model performed on the **test set** of my non-standard Swahili speech dataset.

It's critical for me to note that the model I used for this evaluation was **`openai/whisper-tiny`**. I had fine-tuned this model on **English** atypical speech and then evaluated it on **Swahili** atypical speech. I believe this fundamental language mismatch is the primary reason for the extremely high error rates I observed. My results confirm that the model cannot effectively transcribe Swahili, as I never trained it on Swahili atypical speech data.

---

## 2. My Overall Performance Findings

I found the model's overall performance on the test set to be exceptionally poor, with error rates indicating a near-complete failure to correctly transcribe the audio.

| Metric | Average Score |
| :--- | :---: |
| **Word Error Rate (WER)** | **96.1%** |
| **Character Error Rate (CER)**| **52.8%** |

A WER of 96.1% tells me that, on average, the number of word errors was almost equal to the total number of words in the reference transcript. The CER, while lower, still indicates that I saw approximately half of all characters being incorrectly transcribed.

---

## 3. Performance Breakdown by Etiology

I noticed the model's performance varied significantly depending on the speaker's condition, which highlights how different acoustic patterns presented unique challenges for my model. I saw that the model performed best at the character level on speakers with Parkinson's Disease.

| Etiology | Average WER | Average CER |
| :--- | :---: | :---: |
| Parkinson’s Disease | 93% | **35%** |
| Neurodevelopmental disorder | 95% | 52% |
| Multiple Sclerosis (MS) | 99% | 56% |
| Cerebral Palsy | 99% | 66% |

---

## 4. Performance Breakdown by Severity

As I expected, the model's ability to transcribe speech degraded as the severity of the speech impairment increased. I found this trend to be consistent across both WER and CER, with the highest error rates observed in the "severe" category.

| Severity | Average WER | Average CER |
| :--- | :---: | :---: |
| Mild | 93.9% | 45.0% |
| Moderate | 97.6% | 54.3% |
| Severe | 97.7% | 67.8% |

---

## 5. My Conclusion

My test set results provide a clear and consistent picture: a model I fine-tuned on English atypical speech cannot be used for Swahili atypical speech transcription. The high error rates are not an indication of the model's potential but rather a direct consequence of the language mismatch in my experiment. I believe the only viable path forward is to **fine-tune a new model directly on the Swahili non-standard speech dataset.**