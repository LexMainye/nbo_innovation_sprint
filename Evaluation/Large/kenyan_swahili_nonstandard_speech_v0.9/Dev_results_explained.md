# My Analysis of the Dev Set: A Major Leap Forward with Whisper Large-v3

## 1. My Executive Summary

I've now completed my evaluation of the **`openai/whisper-large-v3`** model on the **development (dev) set** of my `cdli/kenyan_swahili_nonstandard_speech_v0.9` dataset, and the results are a significant step up from my previous tests with the `small` model.

The key finding is that the larger, more powerful `large-v3` model provides a dramatically better baseline performance. The **domain mismatch** is much less severe, as the model's greater capacity allows it to handle the acoustic variations of non-standard speech far more effectively, even without any fine-tuning. While the error rates show there is still work to do, these results are much closer to a usable system and give me a fantastic foundation to build upon.

---

## 2. My Overall Performance

When I looked at my overall numbers, I was immediately struck by the improvement. My average Word Error Rate (WER) dropped to **72.1%** and, more importantly, my Character Error Rate (CER) fell to **30.6%**. This is a massive improvement over the `small` model and tells me that the `large-v3` model is successfully transcribing a large portion of the characters correctly, even if it still makes mistakes at the word level.

| Metric                      | Average Score |
| :-------------------------- | :-----------: |
| **Word Error Rate (WER)** |   **72.1%** |
| **Character Error Rate (CER)**|   **30.6%** |

---

## 3. My Performance Breakdown by Etiology

The breakdown by condition revealed a phenomenal result. The model's performance on speakers with **Multiple Sclerosis (MS)** was outstanding, achieving a WER of just **40%** and a CER of only **10%**. This is a clear indication that the `large-v3` model is capable of accurately transcribing speech from this subgroup with very high fidelity. Performance on other conditions was also much improved compared to the smaller model.

| Etiology                | Average WER | Average CER |
| :---------------------- | :---------: | :---------: |
| Multiple Sclerosis (MS) |  **40.0%** |  **10.0%** |
| Neurological disorder   |    63.0%    |    37.0%    |
| Cerebral Palsy          |    76.0%    |    27.0%    |
| Parkinson’s Disease     |    75.0%    |    30.0%    |

---

## 4. My Performance Breakdown by Severity

As I expected, the trend of performance degrading with increased severity still holds. However, the error rates at every level are drastically lower than before. A CER of **19%** for "mild" cases is an excellent result and shows that for less severe impairments, the `large-v3` model is already performing at a high level.

| Severity | Average WER | Average CER |
| :------- | :---------: | :---------: |
| Mild     |  **56.0%** |  **19.0%** |
| Moderate |    64.0%    |    31.0%    |
| Severe   |    75.0%    |    34.0%    |

---

## 5. My Conclusion

My main takeaway from this evaluation is clear: **model size and architecture are critical factors for this task**. The `openai/whisper-large-v3` model has a much more robust and generalized understanding of speech, which allows it to overcome the challenges of this non-standard dataset far more effectively than the `small` model could.

These results are no longer just a baseline of failure; they are a strong starting point. The model is already demonstrating a solid ability to transcribe this difficult audio. My next goal is to build on this success.

---

## 6. My Revised Plan for Improvement 🚀

My recommendations are now less about fixing a broken system and more about optimizing a promising one.

### **A. Primary Goal: Strategic Fine-Tuning**

* **Fine-Tune the `large-v3` Model:** My priority is now to fine-tune this `large-v3` model. Even a small amount of training on my specific dataset should help it close the gap on the more challenging "severe" and "moderate" cases and further improve its already impressive performance on the "mild" cases.

### **B. Model Training Strategies**

* **Parameter-Efficient Fine-Tuning (PEFT) is Key:** Since I'm working with a very large model, using **LoRA (Low-Rank Adaptation)** is essential. This will allow me to fine-tune the model efficiently without needing massive computational resources.
* **Focus on a Small Learning Rate:** I will use a very small learning rate (e.g., `1e-6` to `5e-6`) to carefully adapt the model without compromising the powerful representations it already has.

### **C. Data and Post-Processing**

* **Audio Augmentation:** I will still use light audio augmentation, but I will be more conservative. My goal is to add robustness without altering the core characteristics that the model is already handling well.
* **Integrate a Swahili Language Model:** This recommendation is now more important than ever. With a strong acoustic model in place, integrating a Swahili language model during decoding is the most direct way to fix the remaining word-level errors (the WER) and produce grammatically perfect transcripts.