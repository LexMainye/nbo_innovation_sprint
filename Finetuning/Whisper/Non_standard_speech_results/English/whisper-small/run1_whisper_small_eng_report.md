# Run 1 Report: Full Fine-tuning of Whisper-Small on Non-Standard Kenyan English

*This report documents the first iteration of my experiments, building upon the baseline by implementing full fine-tuning.*

## 1. Objective

The objective of this experiment was to improve upon the baseline performance by fine-tuning the entire Whisper-small model (encoder, decoder, and projection layer) and adjusting the learning rate.

## 2. Methodology

### 2.1. The Model: Whisper-Small

I continued to use `openai/whisper-small` for this experiment.

*   **Total Parameters:** 241,734,912
*   **Trainable Parameters (in this run):** 241,734,912

### 2.2. The Dataset: Non-Standard Kenyan English Speech

The same filtered `cdli/kenyan_english_nonstandard_speech_v0.9` dataset was used:

| Split      | Filtered Size (<= 30s) |
|------------|------------------------|
| Train      | 3,130                  |
| Validation | 342                    |
| Test       | 705                    |

### 2.3. Fine-Tuning Strategy: Run 1

This run implemented a more aggressive fine-tuning strategy compared to the baseline:

*   **Full Fine-tuning:** The encoder, decoder, and projection layer were all unfrozen and trained.
*   **Data Augmentation:** SpecAugment was used.
*   **Hyperparameters:** The learning rate was reduced to `1e-5` to allow for more stable training of the full model.
    *   **Learning Rate:** 1e-5
    *   **LR Scheduler:** Polynomial decay
    *   **Warmup Steps:** 50
    *   **Batch Size:** 32
    *   **Max Steps:** 1000
    *   **Epochs:** 10

## 3. Results

### 3.1. Complete Training Progress

The model was trained for 1000 steps. The training progression is as follows:

| Step | Training Loss | Validation Loss | WER      | CER      |
|------|---------------|-----------------|----------|----------|
| 0    | No log        | 1.424863        | 0.278408 | 0.166250 |
| 50   | 1.005900      | 0.738581        | 0.208765 | 0.122503 |
| 100  | 0.775300      | 0.624725        | 0.187770 | 0.112984 |
| 150  | 0.627600      | 0.609756        | 0.179757 | 0.103256 |
| 200  | 0.553100      | 0.595022        | 0.172650 | 0.097870 |
| 250  | 0.485800      | 0.589190        | 0.178310 | 0.102975 |
| 300  | 0.437300      | 0.582490        | 0.175832 | 0.100766 |
| 350  | 0.531900      | 0.584866        | 0.177298 | 0.102685 |
| 400  | 0.436600      | 0.582096        | 0.172732 | 0.099971 |
| 450  | 0.468000      | 0.583160        | 0.174559 | 0.100410 |
| 500  | 0.401100      | 0.583989        | 0.171364 | 0.098087 |
| 550  | 0.415400      | 0.583386        | 0.174623 | 0.100751 |
| 600  | 0.424200      | 0.583977        | 0.171823 | 0.097677 |
| 650  | 0.400700      | 0.584168        | 0.171010 | 0.097718 |
| 700  | 0.432100      | 0.584303        | 0.174935 | 0.100559 |
| 750  | 0.431900      | 0.584455        | 0.173925 | 0.099306 |
| 800  | 0.426700      | 0.584433        | 0.174788 | 0.100192 |
| 850  | 0.374200      | 0.584466        | 0.173584 | 0.099700 |
| 900  | 0.432300      | 0.584505        | 0.174616 | 0.100088 |
| 950  | 0.411500      | 0.584497        | 0.174693 | 0.100149 |
| 1000 | 0.454200      | 0.584459        | 0.174604 | 0.100248 |

### Key Training Observations:
- **Best validation WER:** 17.1% achieved at step 650, a slight improvement over the baseline's 18.0%.
- The validation loss and WER plateaued earlier and more definitively than in the baseline run, suggesting that the model might be overfitting or that the learning rate is too small for the later stages of training.

### 3.2. Final Evaluation: Run 1 vs. Baseline

The model with the best validation WER was evaluated on the development and test sets.

**Development Set:**
- **Run 1 WER:** 0.171
- **Baseline WER:** 0.180

**Test Set:**
- **Run 1 WER:** 0.109
- **Baseline WER:** 0.123

| Metric | Baseline | Run 1 | Improvement |
|---|---|---|---|
| **Dev WER** | 0.180 | **0.171** | 5.0% |
| **Test WER** | 0.123 | **0.109** | 11.4% |
| **Dev CER** | 0.102 | **0.098** | 3.9% |
| **Test CER** | 0.065 | **0.058** | 10.8% |


## 4. Conclusion & Future Directions

This first experimental run successfully improved upon the baseline. Full fine-tuning of the model led to a **11.4% relative improvement in WER on the test set**, bringing it down to **10.9%**.

### Planned Improvements:
- Experiment with different learning rate schedules and optimizers.
- Explore more advanced data augmentation techniques.
- Investigate the training plateau to see if it can be overcome.
