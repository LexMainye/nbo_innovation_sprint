# Comparison of Dev vs. Test Set Results for Non-Standard Swahili ASR

## 1. Introduction

This document provides a comparative analysis of the evaluation results from the **development (dev) set** and the **test set** of the `cdli/kenyan_swahili_nonstandard_speech_v0.9` dataset.

The model used for this evaluation was the standard **`openai/whisper-small`**, a multilingual model pre-trained on a vast amount of general speech data. The consistently poor performance across both sets is a direct result of a **domain mismatch**. While the model has been exposed to standard Swahili, it has not been trained to handle the unique acoustic characteristics of atypical or non-standard speech. This comparison confirms that the model's failure on this specialized task is reproducible and not an anomaly.

---

## 2. Overall Performance Comparison

The overall error rates are extremely high for both sets, indicating the model's inability to cope with the non-standard speech domain. The test set shows a slightly better Word Error Rate (WER) and a notably better Character Error Rate (CER), suggesting minor differences in the overall difficulty between the two datasets. However, both results represent a failure to perform the task without specialized training.

| Metric | Dev Set | Test Set |
| :--- | :---: | :---: |
| **Avg. Word Error Rate (WER)** | 98.8% | 96.1% |
| **Avg. Character Error Rate (CER)**| 71.6% | 52.8% |

---

## 3. Performance Comparison by Etiology

The breakdown by etiology reveals interesting variations. The model performed best (at the character level) on Multiple Sclerosis (MS) in the dev set but best on Parkinson's Disease in the test set. This highlights that performance on specific conditions can be highly dependent on the individual speakers present in each dataset and their deviation from "standard" speech patterns.

| Etiology | Dev Set CER | Test Set CER | Dev Set WER | Test Set WER |
| :--- | :---: | :---: | :---: | :---: |
| Cerebral Palsy | 73% | 66% | 99% | 99% |
| Multiple Sclerosis (MS) | **35%** | 56% | **95%** | 99% |
| Parkinson’s Disease | 71% | **35%** | 99% | **93%** |
| Neurological / Neuro. | 76% | 52% | 98% | 95% |

---

## 4. Performance Comparison by Severity

The trend of worsening performance with increasing severity is consistent across both datasets. The error rates for each severity level are comparable, reinforcing the conclusion that the standard `whisper-small` model is not robust to these acoustic variations.

| Severity | Dev Set CER | Test Set CER | Dev Set WER | Test Set WER |
| :--- | :---: | :---: | :---: | :---: |
| Mild | 60.0% | 45.0% | 98.0% | 93.9% |
| Moderate | 67.0% | 54.3% | 98.0% | 97.6% |
| Severe | 74.0% | 67.8% | 99.0% | 97.7% |

---

## 5. Overall Conclusion

The comparison between the dev and test sets confirms that the standard `openai/whisper-small` model, without any fine-tuning, is unsuitable for transcribing non-standard Swahili speech. The results are consistently poor across both data splits, with minor variations attributable to differences in speaker and audio composition.

This analysis validates that a general-purpose model cannot handle this specialized domain out-of-the-box. The essential next step is to **fine-tune the Whisper model directly on the Swahili non-standard speech dataset** to adapt it to these unique acoustic patterns.

---

## 6. Recommendations for Improvement 🚀

To significantly improve upon these baseline results, a focused fine-tuning strategy is required.

### **A. Primary Recommendation: Fine-Tuning**

* **Fine-Tune the Model:** The most critical step is to **fine-tune the `openai/whisper-small` model** (or a larger variant like `whisper-base`) directly on your `cdli/kenyan_swahili_nonstandard_speech_v0.9` training set. This will allow the model to learn the specific acoustic features of the atypical speech and adapt its internal representations.

### **B. Data-Centric Strategies**

* **Audio Augmentation:** Artificially increase the size and diversity of your training data. Use libraries like `audiomentations` to introduce small variations to your existing audio files, such as:
    * Adding background noise.
    * Slightly changing the pitch or speed.
    * Applying SpecAugment to mask parts of the audio spectrogram, forcing the model to learn more robust features.
* **Transcript Normalization:** Ensure your ground truth text is clean and consistent. Remove disfluencies (e.g., stutters, repetitions) and non-speech sounds so the model learns to predict the intended, clean transcript.

### **C. Model Training Strategies**

* **Use a Small Learning Rate:** When fine-tuning, use a small learning rate (e.g., between `1e-5` and `5e-6`) to ensure the model adapts to the new data without forgetting the powerful general-purpose knowledge it already has.
* **Parameter-Efficient Fine-Tuning (PEFT):** To train more efficiently (especially with larger models), use techniques like **LoRA (Low-Rank Adaptation)**. This freezes most of the model and only trains a small set of new weights, which saves time and computational resources.
* **Curriculum Learning:** Consider a staged training approach. Start by fine-tuning the model only on the "easiest" data (e.g., samples with "mild" severity or from the etiology with the lowest baseline CER) before introducing the more complex and severe examples.

### **D. Post-Processing Enhancement**

* **Integrate a Swahili Language Model:** After fine-tuning, you can further boost performance by using an external Swahili language model (e.g., KenLM) during the decoding process. This will help the model choose sequences of words that are grammatically correct and contextually plausible in Swahili, correcting many errors and improving the final output.