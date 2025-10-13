# My Comparison of Dev vs. Test Set Results for Non-Standard Swahili ASR

## 1. Introduction

In this document, I provide a comparative analysis of the evaluation results I got from the **development (dev) set** and the **test set** of the `cdli/kenyan_swahili_nonstandard_speech_v0.9` dataset.

The model I used for this evaluation was the standard **`openai/whisper-small`**, a multilingual model pre-trained on a vast amount of general speech data. The consistently poor performance I saw across both sets is, in my opinion, a direct result of a **domain mismatch**. While the model has been exposed to standard Swahili, it hasn't been trained to handle the unique acoustic characteristics of atypical or non-standard speech. My comparison confirms that the model's failure on this specialized task is reproducible and not just an anomaly.

---

## 2. My Overall Performance Comparison

I found that the overall error rates are extremely high for both sets, indicating the model's inability to cope with the non-standard speech domain. The test set shows a slightly better Word Error Rate (WER) and a notably better Character Error Rate (CER), which suggests to me that there are minor differences in the overall difficulty between the two datasets. However, I consider both results a failure to perform the task without specialized training.

| Metric | Dev Set | Test Set |
| :--- | :---: | :---: |
| **Avg. Word Error Rate (WER)** | 98.8% | 96.1% |
| **Avg. Character Error Rate (CER)**| 71.6% | 52.8% |

---

## 3. My Performance Comparison by Etiology

When I broke down the performance by etiology, I found some interesting variations. The model performed best (at the character level) on Multiple Sclerosis (MS) in the dev set but best on Parkinson's Disease in the test set. This highlights to me that performance on specific conditions can be highly dependent on the individual speakers present in each dataset and how much their speech patterns deviate from "standard" ones.

| Etiology | Dev Set CER | Test Set CER | Dev Set WER | Test Set WER |
| :--- | :---: | :---: | :---: | :---: |
| Cerebral Palsy | 73% | 66% | 99% | 99% |
| Multiple Sclerosis (MS) | **35%** | 56% | **95%** | 99% |
| Parkinson’s Disease | 71% | **35%** | 99% | **93%** |
| Neurological / Neuro. | 76% | 52% | 98% | 95% |

---

## 4. My Performance Comparison by Severity

I observed a consistent trend of worsening performance with increasing severity across both datasets. The error rates I recorded for each severity level are comparable, reinforcing my conclusion that the standard `whisper-small` model isn't robust to these acoustic variations.

| Severity | Dev Set CER | Test Set CER | Dev Set WER | Test Set WER |
| :--- | :---: | :---: | :---: | :---: |
| Mild | 60.0% | 45.0% | 98.0% | 93.9% |
| Moderate | 67.0% | 54.3% | 98.0% | 97.6% |
| Severe | 74.0% | 67.8% | 99.0% | 97.7% |

---

## 5. My Overall Conclusion

My comparison between the dev and test sets confirms that the standard `openai/whisper-small` model, without any fine-tuning, is unsuitable for transcribing non-standard Swahili speech. The results I found are consistently poor across both data splits, with minor variations that I can attribute to differences in speaker and audio composition.

This analysis validates my belief that a general-purpose model cannot handle this specialized domain out-of-the-box. The essential next step for me is to **fine-tune the Whisper model directly on the Swahili non-standard speech dataset** to adapt it to these unique acoustic patterns.

---

## 6. My Recommendations for Improvement 🚀

To significantly improve upon these baseline results, I need to follow a focused fine-tuning strategy.

### **A. My Primary Recommendation: Fine-Tuning**

* **Fine-Tune the Model:** The most critical step for me is to **fine-tune the `openai/whisper-small` model** (or a larger variant like `whisper-base`) directly on my `cdli/kenyan_swahili_nonstandard_speech_v0.9` training set. This will allow the model to learn the specific acoustic features of the atypical speech and adapt its internal representations.

### **B. My Data-Centric Strategies**

* **Audio Augmentation:** I will artificially increase the size and diversity of my training data. I'll use libraries like `audiomentations` to introduce small variations to my existing audio files, such as:
    * Adding background noise.
    * Slightly changing the pitch or speed.
    * Applying SpecAugment to mask parts of the audio spectrogram, which should force my model to learn more robust features.
* **Transcript Normalization:** I need to ensure my ground truth text is clean and consistent. I will remove disfluencies (e.g., stutters, repetitions) and non-speech sounds so the model learns to predict the intended, clean transcript.

### **C. My Model Training Strategies**

* **Use a Small Learning Rate:** When I fine-tune, I'll use a small learning rate (e.g., between `1e-5` and `5e-6`) to make sure the model adapts to the new data without forgetting the powerful general-purpose knowledge it already has.
* **Parameter-Efficient Fine-Tuning (PEFT):** To train more efficiently, I'm going to use techniques like **LoRA (Low-Rank Adaptation)**. This will freeze most of the model and only train a small set of new weights, saving me time and computational resources.
* **Curriculum Learning:** I am considering a staged training approach. I might start by fine-tuning the model only on the "easiest" data (e.g., samples with "mild" severity) before introducing the more complex and severe examples.

### **D. My Plan for Post-Processing Enhancement**

* **Integrate a Swahili Language Model:** After fine-tuning, I can further boost performance by using an external Swahili language model (e.g., KenLM) during the decoding process. This should help the model choose sequences of words that are grammatically correct and contextually plausible in Swahili, correcting many errors and improving my final output.