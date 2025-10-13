# A First-Person Look at My Test Set Results for Non-Standard Swahili ASR

## 1. Executive Summary

Here, I'm documenting my analysis of the `openai/whisper-small` model's performance on the test set of my `cdli/kenyan_swahili_nonstandard_speech_v0.9` dataset.

The model I used is a general-purpose, pre-trained version that I haven't specifically fine-tuned for this kind of speech. My results, even though they show a slight improvement compared to the dev set, still point to a significant **domain mismatch**. It's clear the model isn't equipped to handle the unique acoustic properties of non-standard speech right out of the box. These findings give me a solid baseline and confirm that my next step has to be specialized fine-tuning.

---

## 2. My Overall Performance

When I looked at the overall numbers, I saw that my model's performance on the test set was poor, with a high Word Error Rate (WER) that shows it failed to transcribe most of the content correctly. However, I did notice that the Character Error Rate (CER) was significantly better than what I saw on the dev set. This tells me that my model is managing to capture some of the phonetic sounds correctly, even if it can't quite form the right words.

| Metric                      | Average Score |
| :-------------------------- | :-----------: |
| **Word Error Rate (WER)** |   **83.7%** |
| **Character Error Rate (CER)**|   **32.8%** |

---

## 3. Performance Breakdown by Etiology

Digging deeper into the results, I noticed that the model's performance varied a lot depending on the speaker's condition. It did its best work on speakers with **Parkinson's Disease**, where it achieved a much lower WER (78%) and CER (21%) compared to the other groups. My hypothesis for this is that the acoustic patterns from this specific group in the test data were just less challenging for the standard model to process.

| Etiology                    | Average WER | Average CER |
| :-------------------------- | :---------: | :---------: |
| Parkinson’s Disease         |  **78._0%** |  **21.0%** |
| Neurodevelopmental disorder |    82.0%    |    34.0%    |
| Cerebral Palsy              |    88.0%    |    39.0%    |
| Multiple Sclerosis (MS)     |    90.0%    |    38.0%    |

---

## 4. Performance Breakdown by Severity

As I expected, my results showed a clear trend: the model's performance got worse as the severity of the speech impairment increased. I saw that the error rates for the "moderate" and "severe" categories were significantly higher than for the "mild" ones, which confirms that the base model isn't robust enough to handle these more pronounced speech differences.

| Severity | Average WER | Average CER |
| :------- | :---------: | :---------: |
| Mild     |  **78.0%** |  **28.0%** |
| Moderate |    89.0%    |    36.0%    |
| Severe   |    89.0%    |    40.0%    |

---

## 5. My Conclusion

After reviewing the test set, my initial conclusions from the dev set were confirmed: the standard `openai/whisper-small` model, as it is, just isn't suitable for my task of transcribing non-standard Swahili speech. The high error rates I'm seeing are a direct result of the model never having been exposed to this specific and complex type of speech. These results give me a definitive baseline and highlight that **domain adaptation through fine-tuning is the essential next step for the ASR sprint project**.

---

## 6. My Plan for Improvement 🚀

To get significantly better results, I've laid out a focused fine-tuning strategy.

### **A. Primary Goal: Fine-Tuning**

* **Fine-Tune the Model:** The first and most critical thing I need to do is **fine-tune the `openai/whisper-small` model** (or maybe a larger one like `whisper-base`) directly on my `cdli/kenyan_swahili_nonstandard_speech_v0.9` training set. This should allow the model to finally learn the specific acoustic features of this atypical speech.

### **B. Data-Centric Strategies**

* **Audio Augmentation:** I'm going to artificially increase the size and diversity of my training data. I'll use libraries like `audiomentations` to add small variations to my audio files, like adding a bit of noise or changing the pitch and speed.
* **Transcript Normalization:** I need to go back and make sure my ground truth text is clean and consistent. I'll remove things like stutters so the model can focus on learning to predict the intended, clean transcript.

### **C. Model Training Strategies**

* **Use a Small Learning Rate:** When I start the fine-tuning process, I'll use a small learning rate (somewhere between `1e-5` and `5e-6`) to make sure the model adapts to the new data slowly, without forgetting all the powerful general knowledge it already has.
* **Parameter-Efficient Fine-Tuning (PEFT):** To make the training more efficient, I plan to use a technique like **LoRA (Low-Rank Adaptation)**. This will let me train only a small set of new weights, which will save me time and computational resources.
* **Curriculum Learning:** I'm also thinking about a staged training approach. I might start by fine-tuning the model only on my "easiest" data (like the "mild" severity samples) before I introduce the more difficult examples.

### **D. Post-Processing Enhancement**

* **Integrate a Swahili Language Model:** Once I have a fine-tuned model, I believe I can boost its performance even more by using an external Swahili language model (like KenLM) when it's making predictions. This should help it choose word sequences that are grammatically correct and make sense in Swahili.