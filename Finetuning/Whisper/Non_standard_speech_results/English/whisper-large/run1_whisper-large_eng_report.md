# Fine-tuning Report: Whisper Large V3 on Non-Standard Kenyan English Speech (Run 1)

# Summary

This report details the results of the first experimental run (Run 1) for fine-tuning the Whisper Large V3 model on non-standard Kenyan English speech. This run achieved a **test set WER of 9.1%** and a **CER of 4.6%**. 

Compared to the baseline (8.9% WER, 4.0% CER), this run shows a minor regression in performance. The key changes in this experiment were enabling decoder fine-tuning and increasing the batch size from 8 to 16. The results suggest that enabling decoder updates under these conditions did not improve performance and may have slightly hindered it.

## 1. Experiment Overview

**Model**: `openai/whisper-large-v3`
**Dataset**: `cdli/kenyan_english_nonstandard_speech_v0.9`
**Task**: Transcription (English)

### Key Training Settings
- Learning Rate: 3e-5
- Scheduler: Polynomial decay (power=2)
- **Batch Size: 16** (Baseline: 8)
- Max Steps: 1000
- Epochs: 10
- SpecAugment: Enabled
  - Time masking: prob=0.05, length=10, min_masks=2
  - Feature masking: prob=0.05, length=10, min_masks=2

### Model Configuration
- Encoder Updates: Enabled
- Projection Layer Updates: Enabled
- **Decoder Updates: Enabled** (Baseline: Disabled)
- Mixed Precision (BF16): Enabled

## 2. Dataset Statistics

The dataset statistics remain consistent with the baseline.

| Split      | Original Size | Filtered Size (<= 30s) |
|------------|---------------|------------------------|
| Train      | 4,236         | 3,130                  |
| Validation | 572           | 342                    |
| Test       | 993           | 705                    |

## 3. Training Progress

| Step | Training Loss | Validation Loss | WER      | CER      |
|------|---------------|-----------------|----------|----------|
| 0    | No log        | 1.286609        | 0.191054 | 0.113394 |
| 50   | 0.648000      | 0.567010        | 0.164166 | 0.095832 |
| 100  | 0.701200      | 0.556239        | 0.158475 | 0.092068 |
| 150  | 0.650100      | 0.570458        | 0.155076 | 0.088726 |
| 200  | 0.538500      | 0.539370        | 0.140349 | 0.076922 |
| 250  | 0.384300      | 0.554164        | 0.149140 | 0.082575 |
| 300  | 0.351000      | 0.551159        | 0.147041 | 0.083321 |
| 350  | 0.337800      | 0.533874        | 0.142449 | 0.079113 |
| 400  | 0.220300      | 0.533939        | 0.131361 | 0.070048 |
| 450  | 0.194900      | 0.533819        | 0.148574 | 0.082922 |
| 500  | 0.175300      | 0.551405        | 0.144904 | 0.080610 |
| 550  | 0.180500      | 0.533207        | 0.137615 | 0.074993 |
| 600  | 0.092400      | 0.579920        | 0.137625 | 0.073672 |
| 650  | 0.101000      | 0.600833        | 0.138209 | 0.075923 |
| 700  | 0.111300      | 0.630883        | 0.141267 | 0.076523 |
| 750  | 0.080400      | 0.630889        | 0.135110 | 0.074208 |
| 800  | 0.058500      | 0.657088        | 0.134524 | 0.073771 |
| 850  | 0.047900      | 0.689979        | 0.133999 | 0.073995 |
| 900  | 0.052900      | 0.683515        | 0.135451 | 0.075177 |
| 950  | 0.050000      | 0.686089        | 0.136160 | 0.075641 |
| 1000 | 0.037600      | 0.694312        | 0.136266 | 0.075833 |

**Training Observations**: The model achieved its best validation WER of **13.1% at step 400**. After this point, the validation loss began to increase, indicating overfitting, while the WER fluctuated but did not improve significantly.

## 4. Final Evaluation Results

### Development Set
- **Loss:** 0.534
- **WER:** 0.131
- **CER:** 0.070

### Test Set
- **Loss:** 0.524
- **WER:** 0.091
- **CER:** 0.046

## 5. Comparison with Baseline

| Metric     | Baseline (Decoder Frozen) | Run 1 (Decoder Enabled) | Change |
|------------|---------------------------|-------------------------|--------|
| Test WER   | 8.9%                      | 9.1%                    | +0.2%  |
| Test CER   | 4.0%                      | 4.6%                    | +0.6%  |
| Best Val WER| 13.0%                     | 13.1%                   | +0.1%  |

The results indicate that enabling decoder fine-tuning, in this configuration, did not yield an improvement. The performance slightly degraded across both WER and CER metrics on the test set.

## 6. Recommended Next Steps

1.  **Revert Decoder Fine-Tuning**: Given the negative impact on performance, the next experiments should revert to keeping the decoder frozen, as in the baseline.

2.  **Hyperparameter Optimization**:
    *   Focus on optimizing other hyperparameters while keeping the decoder frozen.
    *   Experiment with different learning rates or schedulers to see if a different combination is more effective.

3.  **Analyze Overfitting**: The training curve shows clear signs of overfitting after step 400. Future runs could benefit from:
    *   Implementing early stopping with patience to save computational resources and prevent overfitting.
    *   Experimenting with weight decay as a regularization technique.

4.  **Batch Size**: While the batch size was increased to 16, it's worth investigating if this had an impact. A run with the baseline batch size of 8 but with the decoder enabled could isolate the effect of that change.
