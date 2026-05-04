# Run 4 Report: Full Model Fine-tuning with Polynomial LR Decay + Weight Decay & Early Stopping of Whisper-Small on Non-Standard Kenyan English

*This report documents the fourth fine-tuning experiment using the `smainye/whisper-small-kenyan-english-nonstandard` checkpoint. Building on Run 3's combination of polynomial LR decay, weight decay, and early stopping, this run unfreezes the full decoder to test whether end-to-end fine-tuning can break the encoder-only performance ceiling of ~21.9% dev WER and ~15.8% test WER established across Runs 1–3.*

## 1. Objective

Runs 1–3 established that encoder-only fine-tuning of Whisper-Small consistently converges to a dev WER ceiling of approximately **21.9%** and a test WER of **15.8–16.0%**, regardless of LR schedule or regularisation strategy. Run 3 demonstrated that the frozen decoder is the primary bottleneck: the encoder adapts incrementally with each scheduling change, but without the decoder being able to update its language model to Kenyan English patterns, further gains from encoder-only strategies appear minimal. This run tests whether unfreezing the full decoder — while retaining the polynomial LR decay, weight decay, and early stopping configuration from Run 3 — can push past that ceiling.

## 2. Methodology

### 2.1. The Model: Whisper-Small

This experiment used `smainye/whisper-small-kenyan-english-nonstandard` as the base model (same as Runs 1–3).

*   **Total Parameters:** 241,734,912
*   **Trainable Parameters (in this run):** 241,734,912

The parameter split was confirmed from cell outputs:

```
Updating encoder: True
Updating projection layer: True
Updating decoder: True
* encoder params to update/total: 88154112 88154112
* decoder params to update/total: 153580800 153580800
* overall # trainable parameters: 241734912
*     overall # model parameters: 241734912
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

### 2.3. Fine-Tuning Strategy: Run 4

This run retained the same LR and regularisation configuration as Run 3, with one structural change: the decoder was fully unfrozen.

*   **Full Fine-tuning:** The encoder, projection layer, and decoder were all unfrozen and trained end-to-end.
*   **Data Augmentation:** SpecAugment was applied with the same default settings (time masking prob: 0.05, feature masking prob: 0.05).
*   **Regularisation:** Weight decay of `0.01` and early stopping with patience of `3` were retained from Run 3.
*   **Hyperparameters:**

| Parameter            | Run 1 Value             | Run 2 Value             | Run 3 Value             | Run 4 Value             |
|----------------------|-------------------------|-------------------------|-------------------------|-------------------------|
| Learning Rate        | 1e-5                    | 5e-6                    | 2e-6                    | **2e-6**                |
| LR Scheduler         | Constant with warmup    | Polynomial decay        | Polynomial decay        | **Polynomial decay**    |
| LR End               | 1e-8                    | 1e-8                    | 1e-8                    | **1e-8**                |
| LR Decay Power       | 1                       | 2                       | 1                       | **1**                   |
| Warmup Steps         | 100                     | 100                     | 100                     | **100**                 |
| Batch Size           | 32                      | 32                      | 32                      | **32**                  |
| Max Steps            | 1000                    | 1000                    | 1000                    | **1000**                |
| Epochs               | 10                      | 10                      | 10                      | **10**                  |
| Weight Decay         | 0.01                    | None (disabled)         | 0.01                    | **0.01**                |
| Early Stopping       | Patience = 3            | None (disabled)         | Patience = 3            | **Patience = 3**        |
| Decoder Frozen       | Yes                     | Yes                     | Yes                     | **No**                  |
| Trainable Parameters | 127,986,432             | 127,986,432             | 127,986,432             | **241,734,912**         |

The LR schedule is identical to Run 3: polynomial decay with `power=1` from `2e-6` down to `1e-8` after the warmup phase. With the decoder now unfrozen, all 153,580,800 decoder parameters are updated under this same conservative schedule, applying small and gradually diminishing update steps to both encoder and decoder throughout training.

## 3. Results

### 3.1. Baseline Evaluation (Step 0)

Before any training, the model was evaluated on the validation set to establish a starting point:

```
adjusted: 0.22780  CER: 0.13977   (Step 0 — initial eval on dev set)
```

This starting WER of **22.8%** matches the baseline from Runs 1–3, confirming we are starting from the same checkpoint.

### 3.2. Complete Training Progress

The model was trained for 1000 steps (~7.5 epochs, total training time ~2 hours 16 minutes based on `train_runtime: 8184.03s`). Evaluation was run every 50 steps on the validation set. The WER and CER values below are the per-example averaged and capped ("adjusted") metrics, which are the primary reported metrics.

| Step | Val WER (adjusted) | Val CER (adjusted) |
|------|--------------------|--------------------|
| 0    | 0.2278             | 0.1398             |
| 50   | 0.2316             | 0.1422             |
| 100  | 0.2272             | 0.1384             |
| 150  | 0.2235             | 0.1367             |
| 200  | 0.2233             | 0.1366             |
| 250  | 0.2205             | 0.1343             |
| 300  | 0.2207             | 0.1341             |
| 350  | 0.2219             | 0.1363             |
| 400  | 0.2197             | 0.1339             |
| 450  | 0.2184             | 0.1327             |
| 500  | 0.2174             | 0.1326             |
| 550  | 0.2217             | 0.1351             |
| 600  | 0.2206             | 0.1344             |
| 650  | 0.2226             | 0.1361             |
| 700  | 0.2209             | 0.1353             |
| 750  | 0.2190             | 0.1337             |
| 800  | 0.2207             | 0.1352             |
| 850  | 0.2202             | 0.1349             |
| 900  | 0.2198             | 0.1347             |
| 950  | 0.2207             | 0.1349             |
| 1000 | 0.2207             | 0.1348             |

The overall training run completed with:
```
TrainOutput(global_step=1000, training_loss=0.41496,
  train_runtime=8184.03s, train_samples_per_second=3.91,
  train_steps_per_second=0.122, epoch=7.52)
```

### Key Training Observations

- **Best validation WER:** ~**21.7%** achieved at step 500 (0.21737), with the model oscillating without further directional improvement from step 500 to 1000.
- Unlike Runs 1–3, Run 4 shows a brief WER spike at step 50 (0.2316, above the baseline of 0.2278) before recovering. This transient regression is consistent with initial destabilisation of the newly unfrozen decoder weights before the polynomial LR schedule and weight decay stabilise joint training.
- The most rapid WER improvement occurs in the 100–500 step range, steeper than any prior run, reflecting the decoder's additional capacity to adapt to Kenyan English patterns once unfrozen.
- From step 500 onward, WER plateaus and the validation loss rises monotonically (0.849 → 0.860), indicating the model is entering a mild overfit regime driven by the decoder overfitting to the 4,243-example training set.
- Training loss (0.415) is meaningfully lower than Run 3 (0.472), consistent with the decoder's extra parameter capacity reducing training-set error — but this does not translate into equivalent validation improvement.
- A `missing keys` warning appeared at end of training (`proj_out.weight` not found in best checkpoint); this is the same known HuggingFace behaviour as in Runs 1–3 and does not affect the saved model.

### 3.3. Final Evaluation

The model checkpoint with the best validation WER was evaluated on both the development and test sets. Results from the final `trainer.evaluate()` calls:

**Development (Validation) Set:**
```python
{'eval_loss': 0.8493975400924683,
 'eval_wer': 0.21736855187655452,
 'eval_cer': 0.13258574827457084,
 'eval_runtime': 138.9196,
 'eval_samples_per_second': 3.902}
```

**Test Set:**
```python
{'eval_loss': 0.7206200957298279,
 'eval_wer': 0.15617960018050103,
 'eval_cer': 0.09204693467543194,
 'eval_runtime': 237.2009,
 'eval_samples_per_second': 3.904}
```

Summarised across all four runs:

| Metric       | Run 1 Score | Run 2 Score | Run 3 Score | Run 4 Score | Δ (Run 3 → 4) |
|--------------|-------------|-------------|-------------|-------------|---------------|
| **Dev WER**  | 0.222       | 0.219       | 0.219       | **0.217**   | −0.002        |
| **Dev CER**  | 0.135       | 0.132       | 0.132       | **0.133**   | +0.001        |
| **Test WER** | 0.158       | 0.158       | 0.160       | **0.156**   | −0.004        |
| **Test CER** | 0.093       | 0.093       | 0.095       | **0.092**   | −0.003        |

Run 4 achieves the best test WER across all four runs at **15.6%**, breaking below the 15.8% floor that encoder-only fine-tuning consistently reached. Dev WER improves to 21.7% and test CER drops to 9.2%, also bests across all runs.

## 4. Conclusion & Future Directions

This experiment unfroze the full decoder while retaining the polynomial LR decay, weight decay, and early stopping configuration from Run 3. The result is a **steeper early training descent and a new best test WER of 15.6%**, confirming that the frozen decoder was the primary bottleneck across Runs 1–3. However, the gains are modest — approximately 0.4 percentage points on test WER — and the validation loss divergence from step 500 onward suggests the 4,243-example training set is insufficient to fully leverage 241M jointly-trained parameters within 1000 steps.

Across four runs the evidence now points to data scarcity as the next binding constraint. The decoder adapts meaningfully once unfrozen, but overfits quickly; further encoder-decoder co-adaptation requires either more data or stronger regularisation to sustain.

### Planned Improvements

- **Extend training steps or epochs** for full decoder fine-tuning — with early stopping active, increasing `MAX_STEPS` to 2000–3000 would give the model capacity to find a better minimum before overfitting takes hold.
- **Layer-wise learning rates** (higher LR for decoder layers, lower for encoder) to accelerate decoder adaptation without destabilising the already-adapted encoder.
- **Partial decoder unfreezing** (e.g. last 6 decoder layers only) as a more conservative alternative, reducing the number of newly-trained parameters and the risk of overfitting on the small training set.
