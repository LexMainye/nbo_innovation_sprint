# Fine-Tuning Whisper for Non-Standard Swahili Speech Recognition

## 1. Project Overview

This project aims to fine-tune an OpenAI Whisper model for the task of Automatic Speech Recognition (ASR) on a specialized dataset of non-standard Swahili. The dataset contains audio recordings from speakers with various speech-affecting conditions, including `Cerebral Palsy`, `Multiple Sclerosis (MS)`, `Parkinson's Disease`, and other neurological disorders, with impairments ranging from mild to severe.

The primary goal is to adapt a general-purpose ASR model to accurately transcribe atypical speech patterns, a task where standard models typically fail. This document outlines the baseline performance of the pre-trained **Whisper Tiny** model and proposes a strategy for fine-tuning.

---

## 2. Baseline Evaluation Results (Using Whisper Tiny)

An initial evaluation was conducted on the development set using the **`openai/whisper-tiny`** model without any prior fine-tuning. The results confirm that this very small model struggles significantly with this specialized domain.

### 2.1. Overall Performance

The overall error rates are extremely high, indicating a failure to correctly transcribe the majority of the speech.

| Metric | Average Score |
| :--- | :--- |
| **Word Error Rate (WER)** | **98.8%** |
| **Character Error Rate (CER)**| **71.6%** |

A WER of nearly 99% is expected given the model's small size and the complexity of the data.

### 2.2. Performance Breakdown by Severity

The model's performance degrades as the severity of the speech impairment increases. While the WER remains consistently high, the Character Error Rate (CER) worsens, showing a decreased ability to capture even basic phonetic sounds.

| Severity | Average WER | Average CER |
| :--- | :---: | :---: |
| Mild | 98% | 60% |
| Moderate | 98% | 67% |
| Severe | 99% | 74% |

### 2.3. Performance Breakdown by Etiology

The results show a notable variation in performance across the different causes of the speech disorders.

| Etiology | Average WER | Average CER |
| :--- | :---: | :---: |
| Multiple Sclerosis (MS) | 95% | **35%** |
| Parkinson’s Disease | 99% | 71% |
| Cerebral Palsy | 99% | 73% |
| Neurological disorder | 98% | 76% |

### 2.4. Key Takeaways from Baseline

1.  **Model Capacity is a Key Limiter:** The `whisper-tiny` model is too small to handle the significant acoustic mismatch between standard speech and the non-standard speech in this dataset.
2.  **Interesting Outlier:** The model performs significantly better at the character level for speakers with Multiple Sclerosis (CER of 35%). This suggests their speech patterns might be acoustically simpler to model, but the `tiny` model still lacks the capacity to form correct words.
3.  **Clear Path for Improvement:** The poor baseline performance strongly indicates that the first and most critical step is to use a larger, more capable model for fine-tuning.

---

## 3. Recommended Fine-Tuning Strategy

To improve upon the baseline, a structured fine-tuning approach is required.

### 3.1. **[CRITICAL]** Select a Larger Base Model

The single most impactful change you can make is to **start with a larger Whisper model**. The `tiny` model likely lacks the capacity to learn the complex patterns in your data.

* **Recommendation:** Start fine-tuning with **`openai/whisper-small`** or **`openai/whisper-base`**. These models offer a much better balance of size and capability and are more likely to benefit from fine-tuning on this dataset.

### 3.2. Data Preparation & Augmentation

1.  **Transcript Normalization**:
    * Clean the ground truth transcripts by removing disfluencies (e.g., stutters, repetitions) and non-speech sounds.
    * Ensure all text is lowercase and punctuation is handled consistently.

2.  **Audio Augmentation**:
    * Increase the effective size of the training data using libraries like `audiomentations`.
    * Apply techniques such as:
        * **Noise Injection:** Adding low-level background noise.
        * **Time/Pitch Shifting:** Slightly altering the speed and pitch of the audio.
        * **SpecAugment:** Masking sections of the audio spectrogram to make the model more robust.

### 3.3. Training & Model Strategy

1.  **Use a Small Learning Rate**:
    * Start with a small learning rate (e.g., `1e-5`) to ensure the model adapts slowly without destroying its pre-trained knowledge.

2.  **Parameter-Efficient Fine-Tuning (PEFT)**:
    * Implement **LoRA (Low-Rank Adaptation)**. This is especially useful when moving to a larger model, as it keeps training fast and memory-efficient by only training a small number of adapter weights.

3.  **Curriculum Learning**:
    * Consider starting your fine-tuning on the "easiest" subset of the data (e.g., **mild severity** or the **Multiple Sclerosis** cohort) before introducing more challenging samples.

### 3.4. Language Model Integration

1.  **External Swahili Language Model**:
    * For a significant boost in performance, train a separate Swahili N-gram language model (e.g., using KenLM) on a large corpus of Swahili text.
    * During inference, use a decoder that combines Whisper's acoustic scores with the language model's probabilities. This will help generate more grammatically correct and coherent Swahili sentences.

