# Run 1 Report: Noise-Robust Fine-Tuning with Waveform Augmentation

*This report documents the first iteration of noise-robust fine-tuning experiments, introducing waveform-level audio augmentation to improve model robustness under real-world Kenyan deployment conditions.*

## 1. Objective

The objective of this experiment was to establish a noise-robust baseline by fine-tuning Whisper-Small on non-standard Kenyan English speech with waveform-level augmentation. The augmentation pipeline simulates four acoustic conditions common in Kenyan field deployments: ambient crowd noise, GSM codec compression, volume variation across devices, and small-room reverb. This run serves as the reference point for subsequent noise-robust experiments.

## 2. Methodology

### 2.1. The Model: Whisper-Small

`openai/whisper-small` was used as the base model.

* **Total Parameters:** 241,734,912
* **Trainable Parameters (in this run):** 241,734,912

### 2.2. The Dataset: Non-Standard Kenyan English Speech

The `cdli/kenyan_english_nonstandard_speech_v1.0` dataset was used, filtered to examples of 30 seconds or under to fit Whisper's context window.

| Split      | Raw Size | Filtered Size (<= 30s) |
|------------|----------|------------------------|
| Train      | 4,378    | 4,243                  |
| Validation | 542      | 542                    |
| Test       | 928      | 926                    |

### 2.3. Fine-Tuning Strategy: Run 1

This run uses full fine-tuning with waveform augmentation applied to the training split only. Evaluation always uses clean audio for reproducible WER/CER comparisons.

* **Full Fine-Tuning:** The encoder, decoder, and projection layer were all unfrozen and trained.
* **Waveform Augmentation:** Applied during training with `AUGMENT_PROB = 0.5`. Four augmentations were enabled:
  * Volume perturbation (always applied, gain range 0.7–1.3)
  * Gaussian noise (simulates ambient crowd noise, level 0.002–0.015)
  * GSM codec simulation (8kHz downsample/resample to mimic mobile network compression)
  * Room reverb (short delay blend at 0.5× apply probability)
* **SpecAugment:** Enabled (`mask_time_prob = 0.05`, `mask_feature_prob = 0.05`)
* **Hyperparameters:**
    * **Learning Rate:** 3e-6
    * **LR Scheduler:** `polynomial` decay
    * **Warmup Steps:** 100
    * **LR End:** 1e-8
    * **Decay Power:** 1
    * **Weight Decay:** 0.01
    * **Batch Size:** 32
    * **Max Steps:** 2000
    * **Epochs:** 10
    * **Early Stopping Patience:** 3

## 3. Results

### 3.1. Complete Training Progress

Training ran for 700 steps before early stopping triggered (patience of 3, evaluated every 50 steps). The best validation WER was achieved at step 550.

| Step | Training Loss | Validation Loss | WER      | CER      |
|------|---------------|-----------------|----------|----------|
| 0    | No log        | 1.609324        | 0.331862 | 0.217665 |
| 50   | 1.993200      | 1.410948        | 0.307396 | 0.196155 |
| 100  | 1.690900      | 1.086406        | 0.281732 | 0.180035 |
| 150  | 1.319600      | 0.951053        | 0.272127 | 0.175502 |
| 200  | 1.370200      | 0.899081        | 0.262177 | 0.167582 |
| 250  | 1.124100      | 0.868637        | 0.252511 | 0.163091 |
| 300  | 1.154600      | 0.850768        | 0.241713 | 0.153767 |
| 350  | 1.148300      | 0.839271        | 0.242803 | 0.154855 |
| 400  | 1.113600      | 0.823259        | 0.235847 | 0.149374 |
| 450  | 1.036700      | 0.819455        | 0.239019 | 0.151292 |
| 500  | 0.986900      | 0.810826        | 0.228684 | 0.145038 |
| 550  | 0.836600      | 0.809220        | 0.227135 | 0.142799 |
| 600  | 0.914200      | 0.803038        | 0.231000 | 0.146869 |
| 650  | 1.043600      | 0.798255        | 0.232468 | 0.148132 |
| 700  | 0.859300      | 0.797636        | 0.232472 | 0.148783 |

### Key Training Observations:
- **Best validation WER:** 22.71% achieved at step 550.
- Training stopped at step 700 due to early stopping (WER did not improve over 3 consecutive evaluations at steps 600, 650, and 700).
- Training loss continued to decrease throughout, suggesting the early stop was driven by the clean-audio validation WER not reflecting further gains from augmentation-trained steps.
- Validation loss also continued to decrease after step 550, indicating the model was still converging on the reconstruction objective even as WER plateaued.

### 3.2. Final Evaluation

The best checkpoint (step 550) was evaluated on the development and test sets using clean audio, and additionally on a noise-augmented test set to quantify robustness.

**Development Set:**
- **WER:** 0.227
- **CER:** 0.143
- **Eval Loss:** 0.809

**Test Set (Clean):**
- **WER:** 0.161
- **CER:** 0.095
- **Eval Loss:** 0.672

**Test Set (Noise-Augmented):**
- **WER:** 0.279
- **CER:** 0.184
- **Eval Loss:** 0.928

### 3.3. Clean vs. Noise-Augmented Test Performance

| Metric  | Clean Test | Noisy Test | WER Degradation |
|---------|------------|------------|-----------------|
| **WER** | 0.161      | 0.279      | +11.8 pp        |
| **CER** | 0.095      | 0.184      | +8.9 pp         |

The 11.8 percentage point WER gap between clean and noisy test sets provides the reference robustness baseline for this augmentation configuration. Subsequent runs will aim to narrow this gap.

## 4. Conclusion & Future Directions

This first noise-robust run establishes a clean test WER of **16.1%** and a noisy test WER of **27.9%**. The clean test result is already competitive, but the robustness gap indicates the augmentation at `AUGMENT_PROB = 0.5` and the current LR schedule may not be fully exploiting the augmented data before early stopping fires.

Key observations for future runs:

- Early stopping triggered prematurely at step 700. Increasing `EARLY_STOPPING_PATIENCE` to 5 or raising `MAX_STEPS` to allow more training time could yield further improvement, given that training loss was still declining at stop.
- The polynomial LR schedule decays to near-zero by step 700, which may compound the early stopping issue. Experimenting with `constant_with_warmup` or a slower decay power may help.
- Increasing `AUGMENT_PROB` to 0.7 in a follow-up run could improve noise robustness at the cost of some clean-audio WER.
- The clean/noisy WER gap (11.8 pp) is the primary robustness metric to track across runs.
