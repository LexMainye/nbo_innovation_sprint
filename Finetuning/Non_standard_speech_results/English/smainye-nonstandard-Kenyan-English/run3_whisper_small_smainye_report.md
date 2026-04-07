# Run 3 Report: Encoder-Only Fine-tuning with Polynomial LR Decay + Weight Decay & Early Stopping of Whisper-Small on Non-Standard Kenyan English

*This report documents the third fine-tuning experiment using the `smainye/whisper-small-kenyan-english-nonstandard` checkpoint. Building on Run 2's introduction of polynomial LR decay, this run re-introduces weight decay and early stopping alongside a shallower polynomial schedule (power=1) and a lower learning rate (2e-6), to investigate whether orthogonal regularisation can yield further sustained improvement.*

## 1. Objective

Runs 1 and 2 established that encoder-only fine-tuning of Whisper-Small reaches a performance ceiling of approximately **21.9% dev WER** and **15.8% test WER**. Run 2 demonstrated that polynomial LR decay produced a smoother, more sustained training trajectory than a constant schedule. This run tests whether combining polynomial decay with the regularisation strategy from Run 1 (weight decay + early stopping) — while using a shallower decay curve (power=1 instead of power=2) at a lower initial learning rate (2e-6 instead of 5e-6) — can push past that ceiling.

## 2. Methodology

### 2.1. The Model: Whisper-Small

This experiment used `smainye/whisper-small-kenyan-english-nonstandard` as the base model (same as Runs 1 and 2).

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
Filtered dataset from 928 to 926 examples with audio length <= 30 seconds     # Test
Filtered dataset from 542 to 542 examples with audio length <= 30 seconds     # Validation
Loaded TRAIN dataset with 4243 examples
```

### 2.3. Fine-Tuning Strategy: Run 3

This run retained the same partial fine-tuning strategy as Runs 1 and 2, with three changes to the LR and regularisation configuration:

*   **Partial Fine-tuning:** Only the encoder and projection layer were unfrozen and trained. The decoder remained frozen.
*   **Data Augmentation:** SpecAugment was applied with the same default settings (time masking prob: 0.05, feature masking prob: 0.05).
*   **Regularisation:** Weight decay of `0.01` and early stopping with patience of `3` were **re-enabled** (as in Run 1), combining orthogonal regularisation with the polynomial LR schedule.
*   **Hyperparameters:**

| Parameter            | Run 1 Value             | Run 2 Value             | Run 3 Value             |
|----------------------|-------------------------|-------------------------|-------------------------|
| Learning Rate        | 1e-5                    | 5e-6                    | **2e-6**                |
| LR Scheduler         | Constant with warmup    | Polynomial decay        | **Polynomial decay**    |
| LR End               | 1e-8                       | 1e-8                    | **1e-8**                |
| LR Decay Power       | 1                      | 2                       | **1**                   |
| Warmup Steps         | 100                     | 100                     | 100                     |
| Batch Size           | 32                      | 32                      | 32                      |
| Max Steps            | 1000                    | 1000                    | 1000                    |
| Epochs               | 10                      | 10                      | 10                      |
| Weight Decay         | 0.01                    | None (disabled)         | **0.01**                |
| Early Stopping       | Patience = 3            | None (disabled)         | **Patience = 3**        |

The polynomial scheduler decays the learning rate linearly (`power=1`) from `2e-6` down to `1e-8` after the warmup phase. Compared to Run 2's squared decay at a higher initial LR, this schedule applies significantly smaller update steps throughout training, providing an even more conservative and gradual adaptation.



## 3. Results

### 3.1. Baseline Evaluation (Step 0)

Before any training, the model was evaluated on the validation set to establish a starting point:

```
adjusted: 0.22780  CER: 0.13977   (Step 0 — initial eval on dev set)
```

This starting WER of **22.8%** matches the baseline from Runs 1 and 2, confirming we are starting from the same checkpoint.

### 3.2. Complete Training Progress

The model was trained for 1000 steps (~7.5 epochs, total training time ~2 hours 7 minutes based on `train_runtime: 7639.7189s`). Evaluation was run every 50 steps on the validation set. The WER and CER values below are the per-example averaged and capped ("adjusted") metrics, which are the primary reported metrics.

| Step | Val WER (adjusted) | Val CER (adjusted) |
|------|--------------------|--------------------|
| 0    | 0.2278             | 0.1398             |
| 50   | 0.2268             | 0.1376             |
| 100  | 0.2261             | 0.1380             |
| 150  | 0.2261             | 0.1381             |
| 200  | 0.2251             | 0.1374             |
| 250  | 0.2249             | 0.1368             |
| 300  | 0.2235             | 0.1357             |
| 350  | 0.2224             | 0.1348             |
| 400  | 0.2215             | 0.1349             |
| 450  | 0.2242             | 0.1361             |
| 500  | 0.2218             | 0.1348             |
| 550  | 0.2218             | 0.1346             |
| 600  | 0.2207             | 0.1337             |
| 650  | 0.2202             | 0.1330             |
| 700  | 0.2187             | 0.1324             |
| 750  | 0.2204             | 0.1331             |
| 800  | 0.2196             | 0.1328             |
| 850  | 0.2199             | 0.1328             |
| 900  | 0.2191             | 0.1324             |
| 950  | 0.2196             | 0.1328             |
| 1000 | 0.2192             | 0.1328             |

The overall training run completed with:
```
TrainOutput(global_step=1000, training_loss=0.47234,
  train_runtime=7639.72s, train_samples_per_second=4.189,
  train_steps_per_second=0.131, epoch=7.52)
```

### Key Training Observations

- **Best validation WER:** ~**21.9%** achieved at step 700 (0.21869), with the model remaining stable between steps 700 and 1000.
- Unlike Run 1, which showed a sharp validation loss rise from step 250 onward, Run 3 shows a smooth and sustained descent in WER throughout training — similar to Run 2 but with an even flatter trajectory owing to the lower LR and shallower decay.
- Unlike Run 2, where WER improved more steeply in the 350–500 step range, Run 3's improvement is more gradual and linear, consistent with the linear (power=1) decay schedule.
- The small temporary WER increase at step 450 (0.2242) is consistent with noise in the per-example-averaged metric and does not indicate sustained overfitting.
- Weight decay and early stopping did not cause the early plateau seen in Run 1, suggesting that the polynomial LR schedule remains the dominant stabilising factor and the regularisation is complementary rather than disruptive at this lower learning rate.
- A `missing keys` warning appeared at end of training (`proj_out.weight` not found in best checkpoint); this is the same known HuggingFace behaviour as in Runs 1 and 2 and does not affect the saved model.

### 3.3. Final Evaluation

The model checkpoint with the best validation WER was evaluated on both the development and test sets. Results from the final `trainer.evaluate()` calls:

**Development (Validation) Set:**
```python
{'eval_loss': 0.8558676242828369,
 'eval_wer': 0.21868973750555104,
 'eval_cer': 0.13240523805524387,
 'eval_runtime': 138.98s,
 'eval_samples_per_second': 3.9}
```

**Test Set:**
```python
{'eval_loss': 0.71793532371521,
 'eval_wer': 0.1596156250206942,
 'eval_cer': 0.09454442927163755,
 'eval_runtime': 234.94s,
 'eval_samples_per_second': 3.941}
```

Summarised across all three runs:

| Metric       | Run 1 Score | Run 2 Score | Run 3 Score | Δ (Run 2 → 3) |
|--------------|-------------|-------------|-------------|---------------|
| **Dev WER**  | 0.222       | 0.219       | **0.219**   | ~0            |
| **Dev CER**  | 0.135       | 0.132       | **0.132**   | ~0            |
| **Test WER** | 0.158       | 0.158       | **0.160**   | +0.002        |
| **Test CER** | 0.093       | 0.093       | **0.095**   | +0.002        |

Run 3 achieves the same best dev WER as Run 2 (21.9%) but shows a marginal test WER regression of approximately 0.2 percentage points. This difference is within the noise range for this dataset and evaluation protocol.

## 4. Conclusion & Future Directions

This experiment combined polynomial LR decay with weight decay and early stopping at a lower learning rate (2e-6) and a shallower decay power (1 vs. 2). The result is a **stable, smooth training trajectory** that matches Run 2's best dev performance (21.9% WER) but does not improve on it. Test WER remains essentially equivalent to Runs 1 and 2 at approximately **15.8–16.0%**, suggesting that the encoder-only fine-tuning ceiling has been reached across all three runs regardless of scheduler and regularisation choices.

Across three runs the evidence consistently points to the frozen decoder as the primary bottleneck. The encoder adapts incrementally with each scheduling change, but without the decoder being able to update its language model to Kenyan English patterns, further gains from encoder-only strategies appear minimal.

### Planned Improvements

- **Unfreeze the full decoder** for Run 4 to give the model capacity to fully adapt its language modelling to Kenyan English patterns — the improvement most likely to break the current performance ceiling.
- **Partial decoder unfreezing** (e.g. last 6 decoder layers only) as a more conservative middle ground, retaining the polynomial LR schedule and weight decay from Run 3.
- **Tune LR end and decay power** jointly — Run 2 (power=2) and Run 3 (power=1) produced similar final performance, but a grid search over {1e-7, 1e-8} LR end values combined with {1, 2} power may reveal further room within the encoder-only regime.
- **Explore data augmentation beyond SpecAugment**, such as speed perturbation or noise injection, to address the inherent scarcity of non-standard Kenyan English speech data.
- **Evaluate on additional Kenyan speech varieties** (e.g. Swahili-accented English, Sheng code-switching) to determine whether the performance ceiling is specific to the `cdli` dataset or reflects a fundamental limit of the encoder-only strategy.
