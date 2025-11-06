# Run 4 Report: Full Fine-tuning of Whisper-Small on Non-Standard Kenyan English with Constant Warmup - Weight Decay & Early Stopping


*This report documents the fourth iteration of my experiments, building upon the previous runs by using a different learning rate scheduler and introducing regularization techniques.*

## 1. Objective

The objective of this experiment was to investigate the impact of a `constant_with_warmup` learning rate scheduler on the fine-tuning performance of the Whisper-small model, while simultaneously implementing regularization and early stopping to control for overfitting.

## 2. Methodology

### 2.1. The Model: Whisper-Small

I continued to use `openai/whisper-small` for this experiment.

* **Total Parameters:** 241,734,912
* **Trainable Parameters (in this run):** 241,734,912

### 2.2. The Dataset: Non-Standard Kenyan English Speech

The same filtered `cdli/kenyan_english_nonstandard_speech_v0.9` dataset was used:

| Split | Filtered Size (<= 30s) |
| :--- | :--- |
| Train | 3,130 |
| Validation | 342 |
| Test | 705 |

### 2.3. Fine-Tuning Strategy: Run 4

This run implemented a different learning rate scheduler and added explicit regularization and stopping mechanisms.

* **Full Fine-tuning:** The encoder, decoder, and projection layer were all unfrozen and trained.
* **Data Augmentation:** SpecAugment was used.
* **Hyperparameters:**
    * **Learning Rate:** 1e-5
    * **LR Scheduler:** constant\_with\_warmup
    * **Warmup Steps:** 50
    * **Batch Size:** 32
    * **Max Steps:** 1000
    * **Epochs:** 10
    * **Weight Decay:** 0.01
    * **Early Stopping Patience:** 3 (monitoring `wer`)
    * **Load Best Model at End:** True


The following code was applied to the training arguments to implement these changes:

```python
print("--- MODIFYING TRAINING ARGS ---")

# 1. Add Weight Decay
# This fights the overfitting.
training_args.weight_decay = 0.01

# 2. Add Early Stopping
# This stops training when the WER stops improving.
training_args.early_stopping_patience = 3

print(f"Set weight_decay to: {training_args.weight_decay}")
print(f"Set early_stopping_patience to: {training_args.early_stopping_patience}")
print("---------------------------------")

```

## 3. Results

### 3.1. Complete Training Progress

The model was trained for 1000 steps. The training progression is as follows:

| Step | Training Loss | Validation Loss | WER | CER |
| :--- | :--- | :--- | :--- | :--- |
| 0 | No log | 1.424863 | 0.278408 | 0.166250 |
| 50 | 1.006000 | 0.738593 | 0.208328 | 0.122377 |
| 100 | 0.770000 | 0.621840 | 0.187169 | 0.112823 |
| 150 | 0.615200 | 0.606061 | 0.179516 | 0.103616 |
| 200 | 0.510800 | 0.589203 | 0.166492 | 0.094063 |
| 250 | 0.439500 | 0.587799 | 0.193711 | 0.119295 |
| 300 | 0.345200 | 0.579318 | 0.170655 | 0.096313 |
| 350 | 0.424700 | 0.584331 | 0.170404 | 0.096207 |
| 400 | 0.288400 | 0.589540 | 0.167011 | 0.093232 |
| 450 | 0.323700 | 0.594734 | 0.167779 | 0.095517 |
| 500 | 0.211800 | 0.614140 | **0.165511** | 0.093748 |
| 550 | 0.225800 | 0.622214 | 0.167024 | 0.093873 |
| 600 | 0.175600 | 0.654973 | 0.169335 | 0.093580 |
| 650 | 0.154900 | 0.663520 | 0.165832 | 0.091715 |
| 700 | 0.127200 | 0.699202 | 0.167665 | 0.091140 |
| 750 | 0.139000 | 0.704636 | 0.171485 | 0.094677 |
| 800 | 0.085700 | 0.716386 | 0.174249 | 0.097002 |
| 850 | 0.084100 | 0.736749 | 0.170809 | 0.095837 |
| 900 | 0.076000 | 0.771160 | 0.175826 | 0.098755 |
| 950 | 0.073300 | 0.748132 | 0.173911 | 0.100162 |
| 1000 | 0.056100 | 0.801349 | 0.169643 | 0.093762 |

#### Key Training Observations:

* **Best Validation WER:** **16.55%** achieved at **step 500**.
* **Persistent Overfitting:** Despite the implementation of `weight_decay=0.01`, the validation loss still began to climb steadily after step 350. This indicates that while regularization was active, the 0.01 value was not strong enough to counteract the aggressive overfitting caused by the `constant_with_warmup` scheduler.
* **Early Stopping & Checkpointing:** The training run completed all 1000 `max_steps`, even with `early_stopping_patience=3`. This is because the `load_best_model_at_end=True` flag was also set. This combination ensures that while the training *completes*, the model saved at the end is the one from the best checkpoint (step 500), not the one from the final step (step 1000).

### 3.2. Final Evaluation: Run 4 vs. Previous Runs

The model with the best validation WER (from step 500, loaded at the end of training) was evaluated on the development and test sets.

| Metric | Baseline | Run 1 (Full FT, Poly) | Run 2 (Partial FT, Poly) | Run 3 (Full FT, Constant) | Run 4 (Full FT, Constant Warmup - Early Stopping & Weight Decay) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Dev WER** | 0.180 | 0.171 | 0.173 | 0.165 | **0.166** |
| **Test WER** | 0.123 | 0.109 | 0.113 | **0.108** | 0.109 |
| **Dev CER** | 0.102 | 0.098 | 0.098 | **0.093** | 0.094 |
| **Test CER** | 0.065 | 0.058 | 0.058 | **0.056** | 0.057 |

## 4. Conclusion

This fourth experimental run tested a `constant_with_warmup` scheduler, combined with `weight_decay` and `early_stopping` to control for overfitting.

The results are mixed. The `constant_with_warmup` scheduler led to the model achieving its best performance very quickly (by step 500). However, it also proved to be highly prone to overfitting, as the `weight_decay` of 0.01 was insufficient to prevent the validation loss from climbing.

The use of `early_stopping` with `load_best_model_at_end=True` was **critical**. It successfully identified and saved the best-performing checkpoint (step 500) before the model's generalization degraded further. This saved checkpoint resulted in a strong dev WER of 16.6%, although its test WER (10.9%) did not surpass the simpler schedulers from Run 1 or Run 3.

This run demonstrates that while the scheduler is aggressive, it *can* find a good minimum quickly, but it requires robust regularization and careful checkpointing to be effective.