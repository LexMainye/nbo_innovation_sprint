# Fine-tuning Report: Whisper Large V3 on Non-Standard Kenyan English Speech (Run 2)

# Summary

This report details the results of the second experimental run (Run 2) for fine-tuning the Whisper Large V3 model on non-standard Kenyan English speech. This run achieved a **test set WER of 9.08%** and a **CER of 4.76%**.

This experiment aimed to isolate the impact of batch size by keeping the decoder frozen (like the baseline) while using a larger batch size (like Run 1). The results are very similar to Run 1 (9.1% WER), and both are a minor regression from the baseline (8.9% WER). This suggests that increasing the batch size from 8 to 16 may be the primary factor for the slight performance decrease, rather than the status of the decoder.

## 1. Experiment Overview

**Model**: `openai/whisper-large-v3`
**Dataset**: `cdli/kenyan_english_nonstandard_speech_v0.9`
**Task**: Transcription (English)

### Key Training Settings
- Learning Rate: 3e-5
- Scheduler: Polynomial decay (power=2)
- **Batch Size: 16** (Baseline: 8, Run 1: 16)
- Max Steps: 1000
- Epochs: 10
- SpecAugment: Enabled
  - Time masking: prob=0.05, length=10, min_masks=2
  - Feature masking: prob=0.05, length=10, min_masks=2

### Model Configuration
- Encoder Updates: Enabled
- Projection Layer Updates: Enabled
- **Decoder Updates: Disabled** (Baseline: Disabled, Run 1: Enabled)
- Mixed Precision (BF16): Enabled

## 2. Dataset Statistics

The dataset statistics remain consistent with the baseline and Run 1.

| Split      | Original Size | Filtered Size (<= 30s) |
|------------|---------------|------------------------|
| Train      | 4,236         | 3,130                  |
| Validation | 572           | 342                    |
| Test       | 993           | 705                    |

## 3. Training Progress

| Step | Training Loss | Validation Loss | WER      | CER      |
|------|---------------|-----------------|----------|----------|
| 0    | No log        | 1.286653        | 0.188746 | 0.111524 |
| 50   | 0.746300      | 0.683865        | 0.166392 | 0.096210 |
| 100  | 0.708100      | 0.607479        | 0.162458 | 0.090914 |
| 150  | 0.674400      | 0.573668        | 0.155647 | 0.087787 |
| 200  | 0.569800      | 0.551333        | 0.141976 | 0.079451 |
| 250  | 0.478300      | 0.556758        | 0.140438 | 0.077265 |
| 300  | 0.438500      | 0.548904        | 0.138274 | 0.075154 |
| 350  | 0.447100      | 0.542283        | 0.140283 | 0.076162 |
| 400  | 0.351200      | 0.539349        | 0.137888 | 0.076879 |
| 450  | 0.324500      | 0.538646        | 0.140025 | 0.076845 |
| 500  | 0.303500      | 0.535887        | 0.142461 | 0.080448 |
| 550  | 0.342200      | 0.530773        | 0.132569 | 0.070877 |
| 600  | 0.232200      | 0.536843        | 0.134553 | 0.073320 |
| 650  | 0.288600      | 0.540017        | 0.134726 | 0.072878 |
| 700  | 0.324200      | 0.544940        | 0.134702 | 0.073230 |
| 750  | 0.267200      | 0.541475        | 0.133242 | 0.072299 |
| 800  | 0.241500      | 0.542218        | 0.132538 | 0.071344 |
| 850  | 0.227700      | 0.547495        | **0.131424** | 0.070882 |
| 900  | 0.263600      | 0.549396        | 0.134157 | 0.073007 |
| 950  | 0.223000      | 0.547812        | 0.135267 | 0.073347 |
| 1000 | 0.207600      | 0.548439        | 0.135820 | 0.073531 |

**Training Observations**: The model achieved its best validation WER of **13.14% at step 850**. Similar to previous runs, performance on the validation set plateaus and shows signs of overfitting in the later stages of training.

## 4. Final Evaluation Results

### Development Set
- **Loss:** 0.542
- **WER:** 0.1325
- **CER:** 0.0713

### Test Set
- **Loss:** 0.529
- **WER:** 0.0908
- **CER:** 0.0476

## 5. Comparison with Baseline and Run 1

| Metric     | Baseline (BS=8, Decoder Frozen) | Run 1 (BS=16, Decoder Enabled) | Run 2 (BS=16, Decoder Frozen) |
|------------|---------------------------------|--------------------------------|-------------------------------|
| Test WER   | 8.9%                            | 9.1%                           | **9.08%**                     |
| Test CER   | 4.0%                            | 4.6%                           | **4.76%**                     |
| Best Val WER| 13.0%                           | 13.1%                          | **13.14%**                    |

The results from Run 2 are nearly identical to Run 1, suggesting that enabling or disabling the decoder has a negligible impact when the batch size is 16. Both runs with a batch size of 16 underperform the baseline which used a batch size of 8.

## 6. Recommended Next Steps

1.  **Revert to Smaller Batch Size**: Since both experiments with a batch size of 16 resulted in a slight performance degradation, future experiments should revert to the baseline batch size of 8 to confirm this finding and build upon the best-performing configuration.

2.  **Hyperparameter Optimization**:
    *   Continue to focus on optimizing other hyperparameters, such as learning rate and scheduler, while using the baseline configuration (Batch Size 8, Decoder Frozen).


