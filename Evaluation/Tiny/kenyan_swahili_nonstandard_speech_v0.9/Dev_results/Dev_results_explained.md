# My Project on Fine-Tuning Whisper for Non-Standard Swahili Speech Recognition

## 1. Project Overview

In this project, I aimed to fine-tune an OpenAI Whisper model for Automatic Speech Recognition (ASR) on a specialized dataset of non-standard Swahili that I worked with. This dataset contains audio recordings from speakers with various speech-affecting conditions, including `Cerebral Palsy`, `Multiple Sclerosis (MS)`, `Parkinson's Disease`, and other neurological disorders, with impairments ranging from mild to severe.

My primary goal was to adapt a general-purpose ASR model to accurately transcribe these atypical speech patterns, a task where I know standard models typically fail. Here, I'll outline the baseline performance I measured using the pre-trained **Whisper Tiny** model and propose the strategy I'll follow for fine-tuning.

---

## 2. My Baseline Evaluation Results (Using Whisper Tiny)

I started by conducting an initial evaluation on my development set using the **`openai/whisper-tiny`** model without any prior fine-tuning. My results confirmed that this very small model struggles significantly with this specialized domain.

### 2.1. Overall Performance

I found the overall error rates to be extremely high, which indicates a failure to correctly transcribe the majority of the speech.

| Metric                 | Average Score |
| :--------------------- | :------------ |
| **Word Error Rate (WER)** | **98.8%** |
| **Character Error Rate (CER)**| **71.6%** |

A WER of nearly 99% was what I expected, given the model's small size and the complexity of my data.

### 2.2. Performance Breakdown by Severity

I observed that the model's performance degraded as the severity of the speech impairment increased. While the WER remained consistently high across the board, the Character Error Rate (CER) worsened, showing a decreased ability on the model's part to capture even basic phonetic sounds.

| Severity | Average WER | Average CER |
| :---     | :---:       | :---:       |
| Mild     | 98%         | 60%         |
| Moderate | 98%         | 67%         |
| Severe   | 99%         | 74%         |

### 2.3. Performance Breakdown by Etiology

My results showed a notable variation in performance across the different causes of the speech disorders.

| Etiology              | Average WER | Average CER |
| :-------------------- | :---:       | :---:       |
| Multiple Sclerosis (MS) | 95%         | **35%** |
| Parkinson’s Disease   | 99%         | 71%         |
| Cerebral Palsy        | 99%         | 73%         |
| Neurological disorder | 98%         | 76%         |

### 2.4. My Key Takeaways from the Baseline

1.  **Model Capacity is a Key Limiter:** I concluded that the `whisper-tiny` model is simply too small to handle the significant acoustic mismatch between standard speech and the non-standard speech in my dataset.
2.  **Interesting Outlier:** I found it interesting that the model performed significantly better at the character level for speakers with Multiple Sclerosis (CER of 35%). This suggests to me that their speech patterns might be acoustically simpler to model, but the `tiny` model still lacks the capacity to form correct words.
3.  **Clear Path for Improvement:** My poor baseline performance strongly indicates that the first and most critical step for me is to use a larger, more capable model for fine-tuning.

---

## 3. My Recommended Fine-Tuning Strategy

To improve upon my baseline, I need to follow a structured fine-tuning approach.

### 3.1. **[CRITICAL]** Selecting a Larger Base Model

I believe the single most impactful change I can make is to **start with a larger Whisper model**. The `tiny` model likely lacks the capacity to learn the complex patterns in my data.

* **My Plan:** I will start my fine-tuning with **`openai/whisper-small`** or **`openai/whisper-base`**. I think these models offer a much better balance of size and capability and are more likely to benefit from fine-tuning on this dataset.

### 3.2. Data Preparation & Augmentation

1.  **Transcript Normalization**:
    * First, I will clean my ground truth transcripts by removing disfluencies (e.g., stutters, repetitions) and non-speech sounds.
    * I'll also ensure all text is lowercase and punctuation is handled consistently.

2.  **Audio Augmentation**:
    * I plan to increase the effective size of my training data using libraries like `audiomentations`.
    * I will apply techniques such as:
        * **Noise Injection:** Adding low-level background noise.
        * **Time/Pitch Shifting:** Slightly altering the speed and pitch of the audio.
        * **SpecAugment:** Masking sections of the audio spectrogram to make my model more robust.

### 3.3. My Training & Model Strategy

1.  **Use a Small Learning Rate**:
    * I will start with a small learning rate (e.g., `1e-5`) to ensure the model adapts slowly without destroying its pre-trained knowledge.

2.  **Parameter-Efficient Fine-Tuning (PEFT)**:
    * I am going to implement **LoRA (Low-Rank Adaptation)**. I find this especially useful now that I'm moving to a larger model, as it will keep my training fast and memory-efficient by only training a small number of adapter weights.

3.  **Curriculum Learning**:
    * I'm considering starting my fine-tuning on what I judge to be the "easiest" subset of the data (e.g., **mild severity** or the **Multiple Sclerosis** cohort) before I introduce more challenging samples.

### 3.4. My Plan for Language Model Integration

1.  **External Swahili Language Model**:
    * For what I hope will be a significant boost in performance, I will train a separate Swahili N-gram language model (e.g., using KenLM) on a large corpus of Swahili text.
    * During inference, I will use a decoder that combines Whisper's acoustic scores with the language model's probabilities. My goal here is to help generate more grammatically correct and coherent Swahili sentences.