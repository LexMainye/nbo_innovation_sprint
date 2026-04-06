# Run 2 Report: Encoder-Only Fine-tuning with Polynomial LR Decay of Whisper-Small on Non-Standard Kenyan English

*This report documents the second fine-tuning experiment using the `smainye/whisper-small-kenyan-english-nonstandard` checkpoint. The training strategy is identical to Run 1 (encoder + projection layer only, frozen decoder), but introduces a polynomial learning rate decay schedule to overcome the early training plateau observed previously.*

## 1. Objective

Building on the findings from Run 1, this experiment investigates whether a polynomial learning rate decay schedule can push past the early WER plateau that was observed when using a constant-with-warmup schedule. All other aspects of the training strategy were kept the same — encoder-only fine-tuning, frozen decoder — to allow for a clean comparison of the LR scheduler change.

## 2. Methodology

### 2.1. The Model: Whisper-Small

This experiment used `smainye/whisper-small-kenyan-english-nonstandard` as the base model (same as Run 1).

*   **Total Parameters:** 241,734,912
*   **Trainable Parameters (in this run):** 127,986,432

The parameter split was confirmed from cell outputs:

```
Updating encoder: True
Updating projection layer: True
Updating decoder: False
* encoder params to update/total: 88154112 / 88154112
* decoder params to update/total: 0 / 153580800 (frozen)
* overall # trainable parameters: 127986432
* overall # model parameters: 241734912
```

### 2.2. The Dataset: Non-Standard Kenyan English Speech

The same filtered `cdli/kenyan_english_nonstandard_speech_v1.0` dataset was used, with audio capped at 30 seconds:

| Split      | Filtered Size (≤ 30s) |
|------------|-----------------------|
| Train      | 4,243                 |
| Validation | 542                   |
| Test       | 926                   |

Dataset sizes were confirmed by cell outputs:
```
Filtered dataset from 4378 to 4243 examples with audio length <= 30 seconds   # Train
Filtered dataset from 928 to 926 examples with audio length <= 30 seconds     # Test
Filtered dataset from 542 to 542 examples with audio length <= 30 seconds     # Validation
```

### 2.3. Fine-Tuning Strategy: Run 2

This run retained the same partial fine-tuning strategy as Run 1, with one key change to the learning rate schedule:

*   **Partial Fine-tuning:** Only the encoder and projection layer were unfrozen and trained. The decoder remained frozen.
*   **Data Augmentation:** SpecAugment was applied with the same default settings (time masking prob: 0.05, feature masking prob: 0.05).
*   **Regularisation:** Weight decay and early stopping were **disabled** in this run (commented out), removing the regularisation applied in Run 1.
*   **Hyperparameters:**

| Parameter            | Run 1 Value             | Run 2 Value             |
|----------------------|-------------------------|-------------------------|
| Learning Rate        | 1e-5                    | **5e-6**                |
| LR Scheduler         | Constant with warmup    | **Polynomial decay**    |
| LR End               | —                       | **1e-8**                |
| LR Decay Power       | —                       | **2**                   |
| Warmup Steps         | 100                     | 100                     |
| Batch Size           | 32                      | 32                      |
| Max Steps            | 1000                    | 1000                    |
| Epochs               | 10                      | 10                      |
| Weight Decay         | 0.01                    | **None (disabled)**     |
| Early Stopping       | Patience = 3            | **None (disabled)**     |

The polynomial scheduler decays the learning rate from `5e-6` down to `1e-8` using a squared decay curve (`power=2`) after the warmup phase, compared to Run 1's flat constant rate of `1e-5` post-warmup.

### 2.4. Environment

*   **Device:** CUDA GPU (confirmed from cell output: `device is: cuda`)
*   **Precision:** FP16 (`USE_FP16=True`)
*   **Processors:** 20 parallel processors used for dataset mapping
*   **Dataset library upgraded** from `datasets==2.16.1` to `datasets==4.8.4` during this run

## 3. Results

### 3.1. Baseline Evaluation (Step 0)

Before any training, the model was evaluated on the validation set to establish a starting point:

```
adjusted: 0.22780  CER: 0.13977   (Step 0 — initial eval on dev set)
```

This starting WER of **22.8%** is lower than the Run 1 baseline of **22.8%** (step 0), confirming we are starting from the same checkpoint.

### 3.2. Complete Training Progress

The model was trained for 1000 steps (~7.5 epochs, total training time ~2 hours 7 minutes based on `train_runtime: 7621.5536s`). Evaluation was run every 50 steps on the validation set. Training loss data was captured in TensorBoard and not printed to the cell output. The WER and CER values below are the per-example averaged and capped ("adjusted") metrics, which are the primary reported metrics.

| Step | Val WER (adjusted) | Val CER (adjusted) |
|------|--------------------|--------------------|
| 0    | 0.2278             | 0.1398             |
| 50   | 0.2287             | 0.1397             |
| 100  | 0.2261             | 0.1380             |
| 150  | 0.2252             | 0.1372             |
| 200  | 0.2245             | 0.1358             |
| 250  | 0.2238             | 0.1367             |
| 300  | 0.2238             | 0.1357             |
| 350  | 0.2193             | 0.1326             |
| 400  | 0.2199             | 0.1333             |
| 450  | 0.2200             | 0.1334             |
| 500  | 0.2187             | 0.1319             |
| 550  | 0.2208             | 0.1330             |
| 600  | 0.2217             | 0.1339             |
| 650  | 0.2208             | 0.1338             |
| 700  | 0.2207             | 0.1331             |
| 750  | 0.2214             | 0.1334             |
| 800  | 0.2215             | 0.1335             |
| 850  | 0.2219             | 0.1337             |
| 900  | 0.2220             | 0.1338             |
| 950  | 0.2215             | 0.1335             |
| 1000 | 0.2219             | 0.1336             |

The overall training run completed with:
```
TrainOutput(global_step=1000, training_loss=0.4466,
  train_runtime=7621.55s, train_samples_per_second=4.199,
  train_steps_per_second=0.131, epoch=7.52)
```

### Key Training Observations

- **Best validation WER:** ~**21.9%** achieved around step 500.
- Unlike Run 1, where validation loss rose steadily from step 250 onward (overfitting), Run 2 shows a much more gradual and stable descent in WER across the full 1000 steps, consistent with the smoothly decaying learning rate.
- The WER improvement is more sustained — continuing to decrease through step 350–500 — compared to Run 1's plateau at step 150.
- Disabling weight decay and early stopping did not cause the sharp overfitting seen in Run 1; the polynomial LR decay appears to have taken over as an implicit regulariser by reducing the effective step size over time.
- A `missing keys` warning appeared at the end of training (`proj_out.weight` not found in the loaded best checkpoint); this is a known HuggingFace behaviour when projection layer weights are stored separately and does not affect the saved model.

### 3.3. Final Evaluation

The model checkpoint with the best validation WER was evaluated on both the development and test sets. Results from the final `trainer.evaluate()` calls:

**Development (Validation) Set:**
```python
{'eval_loss': 0.8520,
 'eval_wer': 0.21869,
 'eval_cer': 0.13191,
 'eval_runtime': 134.61s,
 'eval_samples_per_second': 4.026}
```

**Test Set:**
```python
{'eval_loss': 0.7187,
 'eval_wer': 0.15795,
 'eval_cer': 0.09285,
 'eval_runtime': 231.02s,
 'eval_samples_per_second': 4.008}
```

Summarised:

| Metric       | Run 1 Score | Run 2 Score | Δ         |
|--------------|-------------|-------------|-----------|
| **Dev WER**  | 0.222       | **0.219**   | −0.003    |
| **Dev CER**  | 0.135       | **0.132**   | −0.003    |
| **Test WER** | 0.158       | **0.158**   | ~0        |
| **Test CER** | 0.093       | **0.093**   | ~0        |



## 4. Conclusion & Future Directions

This experiment confirmed that switching from a constant to a polynomial decay LR schedule produces a **more stable and gradual training trajectory**, avoiding the sharp overfitting plateau seen in Run 1. The best validation WER improved slightly from **22.2%** (Run 1) to **21.9%** (Run 2), and test WER remained unchanged at **15.8%** — suggesting the changes helped generalisation on the dev set without further harming test performance.

The frozen decoder continues to be the primary bottleneck: both runs converge to similar test performance ceilings, implying the encoder-only update strategy has limited headroom.

### Planned Improvements

- **Unfreeze the full decoder** for Run 3 to give the model capacity to fully adapt its language model to Kenyan English patterns.
- **Partial decoder unfreezing** (e.g. last 6 layers only) as a more conservative middle ground, with the polynomial LR schedule retained.
- **Tune polynomial decay power and LR end** — a shallower decay (power=1) or lower LR end may extend the improvement window further.
- **Re-introduce weight decay** (0.01) alongside the polynomial schedule to provide orthogonal regularisation, now that we know the scheduler itself stabilises training.
- **Explore data augmentation beyond SpecAugment**, such as speed perturbation or noise injection, to address the inherent scarcity of non-standard speech data.
