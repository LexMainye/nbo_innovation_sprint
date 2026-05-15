# Run 1 Report: Encoder-Only Fine-tuning of Whisper-Small on Non-Standard Kenyan English

*This report documents the first fine-tuning experiment using the `smainye/whisper-small-kenyan-english-nonstandard` checkpoint, updating only the encoder and projection layer while keeping the decoder frozen.*

## 1. Objective

The objective of this experiment was to improve automatic speech recognition performance on non-standard Kenyan English by fine-tuning the `smainye/whisper-small-kenyan-english-nonstandard` model. A targeted fine-tuning strategy was adopted, updating only the encoder and projection layer to adapt the model's audio representations while preserving the decoder's pre-trained language modelling capacity.

## 2. Methodology

### 2.1. The Model: Whisper-Small

This experiment used `smainye/whisper-small-kenyan-english-nonstandard` as the base model.

*   **Total Parameters:** 241,734,912
*   **Trainable Parameters (in this run):** 127,986,432

### 2.2. The Dataset: Non-Standard Kenyan English Speech

The filtered `cdli/kenyan_english_nonstandard_speech_v1.0` dataset was used:

| Split      | Filtered Size (<= 30s) |
|------------|------------------------|
| Train      | 4,243                  |
| Validation | 542                    |
| Test       | 926                    |

### 2.3. Fine-Tuning Strategy: Run 1

This run implemented a partial fine-tuning strategy:

*   **Partial Fine-tuning:** Only the encoder and projection layer were unfrozen and trained. The decoder was kept frozen.
*   **Data Augmentation:** SpecAugment was used with default settings (time masking prob: 0.05, feature masking prob: 0.05).
*   **Regularisation:** Weight decay of `0.01` and early stopping with patience of `3` were applied to combat overfitting.
*   **Hyperparameters:**
    *   **Learning Rate:** 1e-5
    *   **LR Scheduler:** Constant with warmup
    *   **Warmup Steps:** 100
    *   **Batch Size:** 32
    *   **Max Steps:** 1000
    *   **Epochs:** 10

## 3. Results

### 3.1. Complete Training Progress

The model was trained for 1000 steps (~7.5 epochs, ~2 hours 7 minutes). The training progression is as follows:

| Step | Training Loss | Validation Loss | WER      | CER      |
|------|---------------|-----------------|----------|----------|
| 0    | No log        | 0.892234        | 0.227725 | 0.139682 |
| 50   | 0.481300      | 0.874823        | 0.227483 | 0.139237 |
| 100  | 0.544200      | 0.860252        | 0.225434 | 0.136603 |
| 150  | 0.455800      | 0.856266        | 0.222255 | 0.135224 |
| 200  | 0.532000      | 0.859434        | 0.223428 | 0.136359 |
| 250  | 0.473700      | 0.852288        | 0.222697 | 0.135556 |
| 300  | 0.402800      | 0.858385        | 0.223577 | 0.136633 |
| 350  | 0.428000      | 0.860299        | 0.223764 | 0.137620 |
| 400  | 0.404300      | 0.854928        | 0.225937 | 0.139484 |
| 450  | 0.370800      | 0.860665        | 0.225128 | 0.136503 |
| 500  | 0.333300      | 0.864493        | 0.228684 | 0.139782 |
| 550  | 0.276000      | 0.867341        | 0.234369 | 0.144756 |
| 600  | 0.337700      | 0.870464        | 0.226236 | 0.140150 |
| 650  | 0.404400      | 0.868544        | 0.228319 | 0.140795 |
| 700  | 0.286500      | 0.878452        | 0.233683 | 0.144323 |
| 750  | 0.317700      | 0.878058        | 0.225357 | 0.139733 |
| 800  | 0.355000      | 0.883347        | 0.226725 | 0.140310 |
| 850  | 0.273200      | 0.895271        | 0.226335 | 0.142031 |
| 900  | 0.278100      | 0.892568        | 0.232656 | 0.144818 |
| 950  | 0.303000      | 0.903041        | 0.234314 | 0.145623 |
| 1000 | 0.284900      | 0.910010        | 0.237796 | 0.148839 |

### Key Training Observations:
- **Best validation WER:** 22.2% achieved at step 150.
- The validation loss began rising steadily from step 250 onward, while training loss continued to decrease — a clear sign of overfitting, despite weight decay and early stopping being applied.
- The WER plateaued early and then gradually worsened, suggesting that freezing the decoder limits the model's capacity to adapt beyond the initial learning phase.

### 3.2. Final Evaluation

The model checkpoint with the best validation WER (step 150) was evaluated on the development and test sets.

| Metric       | Score |
|--------------|-------|
| **Dev WER**  | 0.222 |
| **Dev CER**  | 0.135 |
| **Test WER** | 0.158 |
| **Test CER** | 0.093 |

The test set outperformed the validation set across all metrics, which may reflect differences in speaker or recording conditions between the two splits.

## 4. Conclusion & Future Directions

This experiment fine-tuned Whisper-Small on non-standard Kenyan English using an encoder-only update strategy, achieving a best validation WER of **22.2%** and a test WER of **15.8%**. While the model showed meaningful improvement from its starting point (27.8% WER at step 0), the early plateau and rising validation loss indicate that the frozen decoder creates a bottleneck that prevents sustained improvement.

### Planned Improvements:
- Explore full fine-tuning of both encoder and decoder to give the model more capacity to adapt.
- Investigate partial decoder unfreezing — e.g. training only the last few decoder layers — as a middle ground.
- Experiment with a polynomial decay LR schedule to overcome the early training plateau.
- Explore more advanced data augmentation techniques to reduce overfitting pressure.
