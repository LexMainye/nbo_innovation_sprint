# Run 2 Report: Constant LR Scheduler with Higher Augmentation Probability

*This report documents the second iteration of noise-robust fine-tuning experiments, investigating the effect of switching to a `constant_with_warmup` LR scheduler and increasing augmentation probability from 0.5 to 0.7.*

## 1. Objective

Run 1 established a noise-robust baseline but was limited by early stopping at step 700 under a polynomial decay schedule. The key hypothesis for Run 2 was that a `constant_with_warmup` scheduler would sustain a higher effective learning rate throughout training, allowing the model to continue improving past the point where Run 1 stalled. Augmentation probability was also increased from 0.5 to 0.7 to expose the model to more diverse acoustic conditions during training.

## 2. Methodology

### 2.1. The Model: Whisper-Small

`openai/whisper-small` was used as the base model.

* **Total Parameters:** 241,734,912
* **Trainable Parameters (in this run):** 241,734,912

### 2.2. The Dataset: Non-Standard Kenyan English Speech

The same `cdli/kenyan_english_nonstandard_speech_v1.0` dataset was used with identical filtering.

| Split      | Raw Size | Filtered Size (<= 30s) |
|------------|----------|------------------------|
| Train      | 4,378    | 4,243                  |
| Validation | 542      | 542                    |
| Test       | 928      | 926                    |

### 2.3. Fine-Tuning Strategy: Run 2

Full fine-tuning with waveform augmentation, matching Run 1's architecture but with two key changes to the training configuration.

* **Full Fine-Tuning:** Encoder, decoder, and projection layer all unfrozen and trained.
* **Waveform Augmentation:** Applied during training. All four augmentations enabled with `AUGMENT_PROB = 0.7` (increased from 0.5 in Run 1):
  * Volume perturbation (always applied, gain range 0.7–1.3)
  * Gaussian noise (crowd/ambient, level 0.002–0.015)
  * GSM codec simulation (8kHz downsample/resample)
  * Room reverb (short delay blend at 0.5× apply probability)
* **SpecAugment:** Enabled (`mask_time_prob = 0.05`, `mask_feature_prob = 0.05`)
* **Hyperparameters:**
    * **Learning Rate:** 3e-6
    * **LR Scheduler:** `constant_with_warmup` (changed from `polynomial` in Run 1)
    * **Warmup Steps:** 100
    * **Weight Decay:** 0.01
    * **Batch Size:** 32
    * **Max Steps:** 2000
    * **Epochs:** 10
    * **Early Stopping Patience:** 5 (increased from 3 in Run 1)

## 3. Results

### 3.1. Complete Training Progress

Training ran for 1,300 steps before early stopping triggered (patience of 5, evaluated every 50 steps). The best validation WER was achieved at step 1,050. Steps 0–750 are sourced from a mid-run screenshot; steps 800–1,300 are from the completed notebook output.

| Step | Training Loss | Validation Loss | WER      | CER      |
|------|---------------|-----------------|----------|----------|
| 0    | No log        | 1.609324        | 0.331862 | 0.217665 |
| 50   | 2.212800      | 1.415255        | 0.306408 | 0.195780 |
| 100  | 1.803200      | 1.098901        | 0.284194 | 0.182322 |
| 150  | 1.459700      | 0.953757        | 0.272092 | 0.176944 |
| 200  | 1.443600      | 0.898554        | 0.264533 | 0.171597 |
| 250  | 1.218200      | 0.867037        | 0.247443 | 0.159057 |
| 300  | 1.248100      | 0.849576        | 0.241865 | 0.155660 |
| 350  | 1.220900      | 0.837024        | 0.242057 | 0.155672 |
| 400  | 1.119700      | 0.821966        | 0.237193 | 0.150647 |
| 450  | 1.083400      | 0.814762        | 0.236999 | 0.152435 |
| 500  | 1.010400      | 0.807254        | 0.234152 | 0.151331 |
| 550  | 0.910900      | 0.805198        | 0.233771 | 0.150718 |
| 600  | 0.915200      | 0.799083        | 0.229666 | 0.146371 |
| 650  | 1.103600      | 0.793131        | 0.225716 | 0.141281 |
| 700  | 0.958900      | 0.791862        | 0.230514 | 0.147253 |
| 750  | 0.859600      | 0.786247        | 0.224436 | 0.142100 |
| 800  | 0.875500      | 0.786279        | 0.229333 | 0.146557 |
| 850  | 0.900800      | 0.786093        | 0.228500 | 0.144537 |
| 900  | 0.864900      | 0.782222        | 0.223969 | 0.140234 |
| 950  | 0.861000      | 0.785021        | 0.221733 | 0.139490 |
| 1000 | 0.867500      | 0.779820        | 0.219909 | 0.136963 |
| 1050 | 0.731700      | 0.783105        | 0.213814 | 0.133141 |
| 1100 | 0.814700      | 0.786614        | 0.220711 | 0.138235 |
| 1150 | 0.834800      | 0.788244        | 0.220876 | 0.139587 |
| 1200 | 0.701300      | 0.786745        | 0.215887 | 0.135305 |
| 1250 | 0.758700      | 0.788262        | 0.219089 | 0.138200 |
| 1300 | 0.734200      | 0.792148        | 0.214900 | 0.132800 |

### Key Training Observations:
- **Best validation WER:** 21.38% achieved at step 1,050.
- Training ran 600 steps longer than Run 1, validating that `constant_with_warmup` sustained useful gradients well past the point where the polynomial scheduler had decayed to near-zero LR.
- Validation loss plateaued in a narrow band from step 750 onward (~0.783–0.792), while WER continued to fluctuate, suggesting the model had largely converged in reconstruction but still had marginal gains available on the transcription metric.
- Early stopping triggered after 5 consecutive evaluations with no WER improvement following the best at step 1,050.

### 3.2. Final Evaluation

The best checkpoint (step 1,050) was evaluated on the development and test sets using clean audio, and additionally on a noise-augmented test set.

**Development Set:**
- **WER:** 0.214
- **CER:** 0.133
- **Eval Loss:** 0.783

**Test Set (Clean):**
- **WER:** 0.155
- **CER:** 0.093
- **Eval Loss:** 0.658

**Test Set (Noise-Augmented):**
- **WER:** 0.290
- **CER:** 0.193
- **Eval Loss:** 0.920

### 3.3. Clean vs. Noise-Augmented Test Performance

| Metric  | Clean Test | Noisy Test | WER Degradation |
|---------|------------|------------|-----------------|
| **WER** | 0.155      | 0.290      | +13.5 pp        |
| **CER** | 0.093      | 0.193      | +10.0 pp        |

The robustness gap widened compared to Run 1 (11.8 pp → 13.5 pp), indicating that the higher augmentation probability at `AUGMENT_PROB = 0.7` did not translate into improved noise robustness on this evaluation set. The noisy eval set applies augmentation at inference time using the same pipeline, which may differ from the augmentation distribution seen during training.

### 3.4. Run 2 vs. Run 1 Comparison

| Metric          | Run 1 (Poly, p=0.5, ES=3) | Run 2 (Const, p=0.7, ES=5) | Delta    |
|-----------------|--------------------------|---------------------------|----------|
| **Steps run**   | 700                      | 1,300                     | +600     |
| **Dev WER**     | 0.227                    | 0.214                     | -0.013   |
| **Test WER**    | 0.161                    | 0.155                     | -0.006   |
| **Test CER**    | 0.095                    | 0.093                     | -0.002   |
| **Noisy WER**   | 0.279                    | 0.290                     | +0.011   |
| **Noisy CER**   | 0.184                    | 0.193                     | +0.009   |

Clean test WER improved by 0.6 pp over Run 1, but the noisy test WER regressed slightly. The benefit of training longer with a stable LR was real but modest for clean audio, and did not carry over to noise robustness.

## 4. Conclusion & Future Directions

Run 2 confirms that `constant_with_warmup` enables substantially longer training before early stopping fires, producing a meaningful improvement on clean test WER (16.1% → 15.5%). However, the robustness gap on noisy audio did not improve despite the higher augmentation probability.

Key observations for future runs:

- Increasing `AUGMENT_PROB` from 0.5 to 0.7 did not reduce the clean/noisy WER gap. The noisy test evaluation pipeline may be applying augmentation more aggressively than what was seen during training, or the model is overfitting to the clean validation signal used for early stopping.
- Evaluating the best checkpoint against the noisy dev set (rather than the clean dev set) as the early stopping criterion may produce a checkpoint that is better calibrated for noisy conditions.
- The WER plateau from step 1,050 onward suggests diminishing returns from the `constant_with_warmup` scheduler at this LR. A mild cosine or linear decay after the warmup phase may help find a better final basin.
- The clean/noisy WER gap (13.5 pp) remains the primary robustness metric to close in subsequent runs.
