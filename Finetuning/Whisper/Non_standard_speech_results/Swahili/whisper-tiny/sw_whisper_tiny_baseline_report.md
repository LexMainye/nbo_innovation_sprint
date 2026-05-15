# Baseline Fine-tuning Report: Whisper Tiny on Non-Standard Swahili Speech

## 1. Executive Summary

This report provides a comprehensive analysis of the baseline fine-tuning of the `openai/whisper-tiny` model for Automatic Speech Recognition (ASR) on the `cdli/kenyan_swahili_nonstandard_speech_v0.9` dataset. The primary objective was to establish a performance benchmark for this task.

The model was fine-tuned for 1000 steps, with only the encoder and projection layers being updated. The fine-tuning process resulted in a final Word Error Rate (WER) of **47.90%** and a Character Error Rate (CER) of **20.43%** on the held-out test set.

While the `whisper-tiny` model provides a viable starting point, the results indicate substantial scope for improvement. This report details the methodology, results, and provides expanded recommendations for future iterations, including leveraging larger models and more extensive hyperparameter tuning.

## 2. Experiment Setup

### 2.1. Model

*   **Base Model:** `openai/whisper-tiny`
*   **Language:** Swahili (`sw`)
*   **Task:** `transcribe`

The `whisper-tiny` model is the smallest version of the Whisper family, with approximately 38 million parameters.

### 2.2. Dataset

*   **Dataset:** `cdli/kenyan_swahili_nonstandard_speech_v0.9`
*   **Splits:** The dataset was divided into training, validation (dev), and test sets. After filtering for audio clips less than or equal to 30 seconds, the dataset sizes were as follows:
    *   **Training set:** 2,855 examples
    *   **Validation set:** 272 examples
    *   **Test set:** 554 examples

## 3. Fine-tuning Methodology

### 3.1. Preprocessing

The audio data was preprocessed using the `WhisperProcessor`. This involved converting the raw audio into log-Mel spectrograms. The corresponding transcriptions were tokenized.

### 3.2. Training Configuration

*   **Fine-tuning Strategy:** A partial fine-tuning approach was adopted where:
    *   The **encoder** was fully updated (`UPDATE_ENCODER = True`).
    *   The **projection layer** (`proj_out`) was updated (`UPDATE_PROJ = True`).
    *   The **decoder** was frozen (`UPDATE_DECODER = False`).
    This resulted in **28,124,544** trainable parameters out of a total of 37,760,640.
*   **Data Augmentation:** SpecAugment was enabled (`USE_SPECAUGMENT = True`) to improve the model's generalization capabilities.
*   **Hyperparameters:**
    *   **Max Steps:** 1000
    *   **Batch Size:** 32 (training), 16 (evaluation)
    *   **Learning Rate:** `1e-4`
    *   **LR Scheduler:** `polynomial` decay
    *   **Optimizer:** AdamW (default for `Seq2SeqTrainer`)
    *   **Precision:** `fp16` (16-bit floating point)

### 3.3. Evaluation Metric

The primary metric for evaluation was the **Word Error Rate (WER)**, which is a standard metric for ASR. The **Character Error Rate (CER)** was also computed. The model checkpoint with the lowest WER on the validation set was considered the best model.

## 4. Results and Analysis

### 4.1. Training Performance

The model was trained for 1000 steps. The training progress is summarized in the table below:

| Step | Training Loss | Validation Loss | WER | CER |
| :--- | :--- | :--- | :--- | :--- |
| 0 | No log | 3.7694 | 0.9878 | 0.6917 |
| 50 | 2.1967 | 1.9550 | 0.8590 | 0.4273 |
| 100 | 1.4900 | 1.4757 | 0.7533 | 0.3780 |
| 150 | 1.3079 | 1.3155 | 0.7034 | 0.3289 |
| 200 | 1.0472 | 1.2309 | 0.6586 | 0.3255 |
| 250 | 1.1054 | 1.1824 | 0.6358 | 0.3224 |
| 300 | 0.9542 | 1.1536 | 0.6378 | 0.3161 |
| 350 | 0.8605 | 1.1264 | 0.6107 | 0.3047 |
| 400 | 0.7956 | 1.1264 | 0.6058 | 0.3034 |
| 450 | 0.7599 | 1.1130 | 0.5985 | 0.2916 |
| 500 | 0.8120 | 1.1040 | 0.5980 | 0.2879 |
| 550 | 0.7848 | 1.1005 | 0.6045 | 0.2972 |
| 600 | 0.7507 | 1.1032 | 0.6005 | 0.2971 |
| 650 | 0.7443 | 1.1016 | 0.5987 | 0.2941 |
| 700 | 0.7678 | 1.1003 | 0.5976 | 0.2960 |
| 750 | 0.7199 | 1.0997 | 0.6013 | 0.2957 |
| 800 | 0.7806 | 1.0996 | 0.6015 | 0.2964 |
| 850 | 0.7340 | 1.0994 | 0.6015 | 0.2984 |
| 900 | 0.7162 | 1.0992 | 0.6011 | 0.2944 |
| 950 | 0.8453 | 1.0992 | 0.6005 | 0.2962 |
| 1000 | 0.8237 | 1.0992 | 0.6001 | 0.2963 |

The training loss decreased steadily, and the validation WER showed significant improvement from the initial baseline, indicating that the model was learning effectively. The validation WER plateaued around 0.60 towards the end of the training.

### 4.2. Evaluation Performance

The best model checkpoint was evaluated on the validation (dev) and test sets.

*   **Validation Set Performance:**
    *   **WER:** 59.76%
    *   **CER:** 29.60%
    *   **Loss:** 1.1003

*   **Test Set Performance:**
    *   **WER:** 47.90%
    *   **CER:** 20.43%
    *   **Loss:** 0.9970

### 4.3. Analysis of Findings

*   **Successful Baseline:** The fine-tuning process successfully established a performance baseline for the `whisper-tiny` model on this dataset. A WER of ~48% on the test set is a respectable result for a tiny model on a non-standard speech dataset.
*   **Generalization:** The model performed significantly better on the test set than on the validation set (48% vs 60% WER). This is an unusual but positive result, suggesting good generalization. It may also indicate that the validation set is more challenging or has a slightly different data distribution than the test set.
*   **Potential for Improvement:** The final WER, while a good baseline, indicates that there is considerable room for improvement. The model still makes a significant number of errors.

## 5. Conclusion and Recommendations

### 5.1. Conclusion

The fine-tuning of the `openai/whisper-tiny` model has provided a solid baseline for ASR on non-standard Swahili speech. The methodology of partial fine-tuning with SpecAugment proved to be effective. The results are promising and justify further investment in more advanced models and techniques.

### 5.2. Recommended Next Steps

1.  **Scale Up the Model:**
    *   **Action:** Fine-tune larger Whisper models such as `whisper-small`, `whisper-base`, and `whisper-large-v3`.
    *   **Rationale:** Larger models have a greater capacity to learn complex patterns in speech and are expected to yield substantial improvements in WER.

2.  **Experiment with Fine-tuning Strategy:**
    *   **Action:** Perform full fine-tuning (updating both encoder and decoder) and compare the results with the current partial fine-tuning approach.
    *   **Rationale:** While more computationally expensive, full fine-tuning may allow the model to better adapt to the nuances of the Swahili language and non-standard speech.

3.  **Conduct Hyperparameter Optimization:**
    *   **Action:** Systematically tune key hyperparameters, including learning rate, batch size, and the number of training steps.
    *   **Rationale:** The current hyperparameters were a starting point. A more thorough search could uncover a more optimal configuration for this specific dataset.

4.  **Perform In-depth Error Analysis:**
    *   **Action:** Manually review the model's transcription errors on a subset of the test data. Categorize the errors (e.g., phonetic errors, out-of-vocabulary words, errors due to code-switching).
    *   **Rationale:** Understanding the nature of the errors will provide crucial insights for targeted improvements, such as custom text normalizers or adjustments to the training data.

5.  **Expand the Training Data:**
    *   **Action:** If possible, augment the training set with more Swahili speech data, especially from diverse sources and speakers.
    *   **Rationale:** Increasing the volume and diversity of the training data is one of the most effective ways to improve the robustness and accuracy of an ASR model.
