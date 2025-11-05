# Run 3 Report: Constant Learning Rate Scheduler with Full Fine-tuning

*This report documents the third iteration of my experiments, investigating the impact of a different learning rate scheduler.*

## 1. Objective

The objective of this experiment was to see if a `constant_with_warmup` learning rate scheduler would improve performance compared to the polynomial decay scheduler used in previous runs.

## 2. Methodology

### 2.1. The Model: Whisper-Small

I continued to use `openai/whisper-small` for this experiment.

* **Total Parameters:** 241,734,912
* **Trainable Parameters (in this run):** 241,734,912

### 2.2. The Dataset: Non-Standard Kenyan English Speech

The same filtered `cdli/kenyan_english_nonstandard_speech_v0.9` dataset was used:

| Split      | Filtered Size (<= 30s) |
|------------|------------------------|
| Train      | 3,130                  |
| Validation | 342                    |
| Test       | 705                    |

### 2.3. Fine-Tuning Strategy: Run 3

This run reverted to full fine-tuning, similar to Run 1, but with a different learning rate scheduler:

* **Full Fine-tuning:** The encoder, decoder, and projection layer were all unfrozen and trained.
* **Data Augmentation:** SpecAugment was used.
* **Hyperparameters:** The key change was the `LR_SCHEDULER_TYPE`.
    * **Learning Rate:** 1e-5
    * **LR Scheduler:** `constant_with_warmup`
    * **Warmup Steps:** 50
    * **Batch Size:** 32
    * **Max Steps:** 1000
    * **Epochs:** 10

## 3. Results

### 3.1. Complete Training Progress

The model was trained for 1000 steps. The training progression is as follows:

| Step | Training Loss | Validation Loss | WER      | CER      |
|------|---------------|-----------------|----------|----------|
| 0    | No log        | 1.424863        | 0.278408 | 0.166250 |
| 50   | 1.005900      | 0.738640        | 0.208147 | 0.122270 |
| 100  | 0.770100      | 0.621953        | 0.187142 | 0.112549 |
| 150  | 0.615200      | 0.606184        | 0.178924 | 0.103041 |
| 200  | 0.510800      | 0.589157        | 0.167526 | 0.094345 |
| 250  | 0.439700      | 0.587849        | 0.196233 | 0.122290 |
| 300  | 0.345600      | 0.579521        | 0.172695 | 0.097257 |
| 350  | 0.424800      | 0.584356        | 0.171236 | 0.096389 |
| 400  | 0.288300      | 0.589411        | 0.167286 | 0.092906 |
| 450  | 0.324100      | 0.594746        | 0.170454 | 0.098264 |
| 500  | 0.213300      | 0.614631        | 0.165092 | 0.093255 |
| 550  | 0.226400      | 0.622494        | 0.167437 | 0.093478 |
| 600  | 0.181300      | 0.638331        | 0.165730 | 0.092453 |
| 650  | 0.165300      | 0.659297        | 0.170195 | 0.094956 |
| 700  | 0.127700      | 0.702008        | 0.171768 | 0.095806 |
| 750  | 0.145900      | 0.700598        | 0.171276 | 0.096932 |
| 800  | 0.087900      | 0.716936        | 0.174192 | 0.096676 |
| 850  | 0.087300      | 0.729518        | 0.172560 | 0.097084 |
| 900  | 0.079200      | 0.769923        | 0.173109 | 0.096814 |
| 950  | 0.075100      | 0.750335        | 0.174966 | 0.098814 |
| 1000 | 0.055100      | 0.792211        | 0.169441 | 0.092904 |

### Key Training Observations:
- **Best validation WER:** 16.51% achieved at step 500.
- The `constant_with_warmup` scheduler led to a lower validation WER at an earlier stage of training compared to the polynomial decay scheduler.

### 3.2. Final Evaluation: Run 3 vs. Previous Runs

The model with the best validation WER was evaluated on the development and test sets.

**Development Set:**
- **Run 3 WER:** 0.165
- **Run 2 WER:** 0.173
- **Run 1 WER:** 0.171
- **Baseline WER:** 0.180

**Test Set:**
- **Run 3 WER:** 0.108
- **Run 2 WER:** 0.113
- **Run 1 WER:** 0.109
- **Baseline WER:** 0.123

| Metric | Baseline | Run 1 (Full FT, Poly) | Run 2 (Partial FT, Poly) | Run 3 (Full FT, Constant) |
|---|---|---|---|---|
| **Dev WER** | 0.180 | 0.171 | 0.173 | **0.165** |
| **Test WER** | 0.123 | 0.109 | 0.113 | **0.108** |
| **Dev CER** | 0.102 | 0.098 | 0.098 | **0.093** |
| **Test CER** | 0.065 | 0.058 | 0.058 | **0.056** |


## 4. Conclusion & Future Directions

This third experimental run, using a `constant_with_warmup` learning rate scheduler, yielded the best results so far, with a **Test WER of 10.8%**. This represents a **12.2% relative improvement over the baseline** and a slight improvement over Run 1.

The `constant_with_warmup` scheduler appears to be a better choice for this fine-tuning task.

### Planned Improvements:
- Given the success of the new scheduler, the next logical step is to apply it to a larger model, such as `whisper-large-v3`, to see if further improvements can be made.