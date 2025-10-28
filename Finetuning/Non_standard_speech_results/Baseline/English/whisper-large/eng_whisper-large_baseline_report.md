# Fine-tuning Report: Whisper Large V3 on Non-Standard Kenyan English Speech

# Summary

This report presents baseline results from the initial fine-tuning of Whisper Large V3 on Kenyan English speech data. The model demonstrates promising performance improvements, achieving a test set WER of 8.9% and CER of 4.0%, representing a solid foundation for future optimization. This output establishes a performance benchmark against which subsequent iterations can be measured

## 1. Experiment Overview

**Model**: `openai/whisper-large-v3`
**Dataset**: `cdli/kenyan_english_nonstandard_speech_v0.9`
**Task**: Transcription (English)

### Key Training Settings
- Learning Rate: 3e-5
- Scheduler: Polynomial decay (power=2)
- Batch Size: 8
- Max Steps: 1000
- Epochs: 10
- SpecAugment: Enabled
  - Time masking: prob=0.05, length=10, min_masks=2
  - Feature masking: prob=0.05, length=10, min_masks=2

### Model Configuration
- Encoder Updates: Enabled
- Projection Layer Updates: Enabled
- Decoder Updates: Disabled
- Mixed Precision (FP16): Enabled

## 2. Dataset Statistics

| Split      | Original Size | Filtered Size (<= 30s) |
|------------|---------------|------------------------|
| Train      | 4,236         | 3,130                  |
| Validation | 572           | 342                    |
| Test       | 993           | 705                    |

## 3. Training Progress

| Step | Training Loss | Validation Loss | WER      | CER      |
|------|---------------|-----------------|----------|----------|
| 0    | No log        | 1.285149        | 0.189868 | 0.111399 |
| 100  | 0.691100      | 0.641501        | 0.175942 | 0.102086 |
| 200  | 0.670600      | 0.588253        | 0.166670 | 0.098805 |
| 300  | 0.658700      | 0.557633        | 0.155871 | 0.092836 |
| 400  | 0.484700      | 0.541017        | 0.153737 | 0.091750 |
| 500  | 0.433800      | 0.540500        | 0.131215 | 0.071058 |
| 600  | 0.374300      | 0.533526        | 0.130914 | 0.072273 |
| 700  | 0.351900      | 0.531478        | 0.132066 | 0.071950 |
| 800  | 0.342600      | 0.526069        | 0.129884 | 0.070896 |
| 900  | 0.289500      | 0.526272        | 0.131130 | 0.072035 |
| 1000 | 0.319800      | 0.526469        | 0.131084 | 0.071916 |

Training Observations: The model shows consistent improvement until step ~500, after which performance plateaus, suggesting potential early stopping opportunities in future iterations

## 4. Final Evaluation Results

### Development Set
- **Loss:** 0.053
- **WER:** 0.130
- **CER:** 0.071

### Test Set
- **Loss:** 0.501
- **WER:** 0.089
- **CER:** 0.040

## 5. Technical Notes

- Training utilized gradient checkpointing for memory efficiency
- Best model selection based on WER metric
- Training completed with model checkpoints saved every 100 steps
- Used polynomial learning rate decay with warmup (100 steps)

## 6. Recommended next steps

1. Hyperparameter Optimization

- Conduct comprehensive learning rate sweep (1e-6 to 1e-4)

- Experiment with cosine annealing vs polynomial decay schedulers

- Test larger batch sizes with gradient accumulation

- Optimize warmup steps and decay parameters

2. Dataset Analysis & Enhancement
- Perform detailed error analysis on high-WER samples

- Implement audio data augmentation:

- Speed perturbation (±10%)

- Background noise injection

- Volume normalization variations

- Review and optimize 30-second filtering criteria

3. Model Configuration Experiments
- Enable decoder fine-tuning for end-to-end comparison

- Test progressive unfreezing of encoder layers

- Experiment with alternative SpecAugment configurations

- Evaluate different dropout rates and regularization strategies
