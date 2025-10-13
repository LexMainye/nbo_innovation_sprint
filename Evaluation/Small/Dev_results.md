# My Analysis of the Test Set Results for Non-Standard Swahili ASR

## 1. Executive Summary

In this document, I've analyzed the performance of the **`openai/whisper-small`** model on the **test set** of my `cdli/kenyan_swahili_nonstandard_speech_v0.9` dataset.

The model I evaluated is a general-purpose, pre-trained model that I haven't specifically fine-tuned on this type of atypical speech. My results, while showing a slight improvement over the dev set, still reflect a significant **domain mismatch**. The model isn't equipped to handle the unique acoustic properties of non-standard speech out-of-the-box. These findings establish my final baseline performance and reinforce the need for me to move forward with specialized fine-tuning.

---

## 2. My Overall Performance

I found that my model's overall performance on the test set was poor, with a high Word Error Rate (WER) that indicates a failure to correctly transcribe the majority of the content. However, I noticed the Character Error Rate (CER) was notably better than on the dev set, which suggests the `openai/whisper-small` is capturing some phonetic elements correctly, even if it fails to form the right words.

| Metric                      | Average Score |
| :-------------------------- | :-----------: |
| **Word Error Rate (WER)** |   **83.7%** |
| **Character Error Rate (CER)**|   **32.8%** |

---

## 3. Performance Breakdown by Etiology

I observed that my model's performance varies significantly depending on the speaker's condition. It performed best on speakers with **Parkinson's Disease**, achieving a much lower WER (78%) and CER (21%) compared to other groups. My hypothesis is that the acoustic patterns in this specific subset of the test data were less challenging for the standard model.

| Etiology                    | Average WER | Average CER |
| :-------------------------- | :---------: | :---------: |
| Parkinson’s Disease         |  **78.0%** |  **21.0%** |
| Neurodevelopmental disorder |    82.0%    |    34.0%    |
| Cerebral Palsy              |    88.0%    |    39.0%    |
| Multiple Sclerosis (MS)     |    90.0%    |    38.0%    |

---

## 4. Performance Breakdown by Severity

My results show a clear trend where the model's performance degrades as the severity of the speech impairment increases. I saw that the error rates for "moderate" and "severe" cases are significantly higher than for "mild" ones, confirming the model's lack of robustness to more pronounced speech deviations.

| Severity | Average WER | Average CER |
| :------- | :---------: | :---------: |
| Mild     |  **78.0%** |  **28.0%** |
| Moderate |    89.0%    |    36.0%    |
| Severe   |    89.0%    |    40.0%    |

---

## 5. My Conclusion

My analysis of the test set confirms what I found in the development set: the standard `openai/whisper-small` model, as is, is not suitable for my task of transcribing non-standard Swahili speech. The high error rates are a direct result of the model's lack of exposure to this specific and complex speech domain. These results give me a definitive baseline and highlight that **domain adaptation via fine-tuning is the essential next step for my project**.

---

## 6. My Plan for Improvement 🚀

To significantly improve upon these baseline results, I will implement a focused fine-tuning strategy.

### **A. Primary Goal: Fine-Tuning**

* **Fine-Tune the Model:** My most critical step is to **fine-tune the `openai/whisper-small` model** (or a larger variant like `whisper-base`) directly on my `cdli/kenyan_swahili_nonstandard_speech_v0.9` training set. This will allow the model to learn the specific acoustic features of the atypical speech.

### **B. Data-Centric Strategies**

* **Audio Augmentation:** I will artificially increase the size and diversity of my training data using libraries like `audiomentations` to introduce small variations to my existing audio files, such as adding noise or changing the pitch/speed.
* **Transcript Normalization:** I need to ensure my ground truth text is clean and consistent by removing disfluencies (e.g., stutters) so the model learns to predict the intended, clean transcript.

### **C. Model Training Strategies**

* **Use a Small Learning Rate:** When I start fine-tuning, I will use a small learning rate (e.g., between `1e-5` and `5e-6`) to make sure the model adapts to the new data without forgetting its powerful general-purpose knowledge.
* **Parameter-Efficient Fine-Tuning (PEFT):** To train more efficiently, I will use techniques like **LoRA (Low-Rank Adaptation)**. This will freeze most of the model and only train a small set of new weights, saving time and computational resources.
* **Curriculum Learning:** I am considering a staged training approach. I might start by fine-tuning the model only on the "easiest" data (e.g., samples with "mild" severity) before introducing the more complex examples.

### **D. Post-Processing Enhancement**

* **Integrate a Swahili Language Model:** After fine-tuning, I can further boost performance by using an external Swahili language model (e.g., KenLM) during the decoding process. This should help the model choose sequences of words that are grammatically correct and contextually plausible in Swahili.