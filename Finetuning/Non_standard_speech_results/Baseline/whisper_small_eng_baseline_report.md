# Report: Fine-tuning the Whisper-Small Model on Non-Standard Kenyan English

This report details the process and results of fine-tuning the `openai/whisper-small` model for automatic speech recognition (ASR) on the `cdli/kenyan_english_nonstandard_speech_v0.9` dataset.

## 1. Objective

The primary objective of this experiment was to adapt a pre-trained Whisper model to improve its transcription accuracy on non-standard Kenyan English, a dialect often underrepresented in standard ASR training data.

## 2. Methodology

### 2.1. The Model: Whisper-Small

I chose the `openai/whisper-small` model as the foundation for this task. It offers a good balance between performance and computational requirements. Here are some of its key characteristics:

*   **Total Parameters:** 241,734,912
*   **Trainable Parameters (in this experiment):** 127,986,432

### 2.2. The Dataset: Non-Standard Kenyan English Speech

I used the `cdli/kenyan_english_nonstandard_speech_v0.9` dataset from the Hugging Face Hub. The dataset is split into training, validation, and test sets.

Because the Whisper model is pre-trained on audio segments of 30 seconds or less, I filtered the dataset accordingly. The table below shows the number of samples before and after filtering:

| Split      | Original Size | Filtered Size (<= 30s) |
|------------|---------------|------------------------|
| Train      | 4,236         | 3,130                  |
| Validation | 572           | 342                    |
| Test       | 993           | 705                    |

### 2.3. Fine-Tuning Strategy

My fine-tuning approach involved the following key decisions:

*   **Partial Fine-tuning:** To retain the strong language modeling capabilities of the pre-trained decoder, I chose to freeze its weights. I only trained the **encoder** and the **projection layer**, which are more directly involved in learning the acoustic features of the input audio.
*   **Data Augmentation (SpecAugment):** I used SpecAugment to create more robust acoustic representations. This technique randomly masks parts of the audio in the frequency and time domains, which helps the model generalize better.
*   **Hyperparameters:** The training was configured with the following hyperparameters:
    *   **Learning Rate:** 1e-4
    *   **LR Scheduler:** Polynomial decay
    *   **Warmup Steps:** 50
    *   **Batch Size:** 32
    *   **Max Steps:** 1000
    *   **Epochs:** 10

## 3. Results

### 3.1. Training Progress

The model was trained for 1000 steps. The validation Word Error Rate (WER) and Character Error Rate (CER) were monitored throughout the process.

| Step | Training Loss | Validation Loss | Wer      | Cer      |
|------|---------------|-----------------|----------|----------|
| 0    | No log        | 1.424880        | 0.278409 | 0.166156 |
| 50   | 0.935700      | 0.737602        | 0.216053 | 0.123037 |
| 100  | 0.713700      | 0.687359        | 0.216708 | 0.132061 |
| 150  | 0.502300      | 0.679826        | 0.203396 | 0.122316 |
| 200  | 0.362500      | 0.668027        | 0.204071 | 0.122224 |
| 250  | 0.318100      | 0.665594        | 0.202272 | 0.118560 |
| 300  | 0.219300      | 0.649036        | 0.182868 | 0.105684 |
| 350  | 0.295200      | 0.654805        | 0.188066 | 0.109171 |
| 400  | 0.205200      | 0.655462        | 0.184652 | 0.106480 |
| 450  | 0.224000      | 0.662525        | 0.186053 | 0.109224 |
| 500  | 0.167100      | 0.666398        | 0.180363 | 0.101654 |
| 550  | 0.168000      | 0.672540        | 0.185231 | 0.106131 |
| 600  | 0.167600      | 0.671067        | 0.184393 | 0.105272 |
| 650  | 0.152700      | 0.673863        | 0.184035 | 0.106334 |
| 700  | 0.165600      | 0.673125        | 0.181144 | 0.103453 |
| 750  | 0.159000      | 0.674710        | 0.186322 | 0.107135 |
| 800  | 0.161100      | 0.674365        | 0.185028 | 0.105985 |
| 850  | 0.145500      | 0.674453        | 0.185355 | 0.106129 |
| 900  | 0.160800      | 0.674399        | 0.184706 | 0.105806 |
| 950  | 0.148300      | 0.674431        | 0.184282 | 0.105735 |
| 1000 | 0.170000      | 0.674457        | 0.185004 | 0.105964 |

### 3.2. Final Evaluation

After training, the model with the best validation WER was loaded for a final evaluation on the development (validation) and test sets.

**Development Set:**
- **Loss:** 0.666
- **WER:** 0.180
- **CER:** 0.102

**Test Set:**
- **Loss:** 0.604
- **WER:** 0.123
- **CER:** 0.065

## 4. Deployment

The fine-tuned model and its tokenizer have been uploaded to the Hugging Face Hub. They are publicly available at:
[smainye/eng_finetunned_tune_whisper_small_model_baseline](https://huggingface.co/smainye/eng_finetunned_tune_whisper_small_model_baseline)

## 5. Conclusion

The experiment successfully demonstrated that fine-tuning the Whisper-small model on a specific dialect can lead to significant improvements in transcription accuracy. The final model achieved a WER of 12.3% on the test set, which is a strong result. The model is now available on the Hugging Face Hub for broader use.