# Fine-tuning Baseline Report: Whisper Large V3 on Non-Standard Kenyan Swahili Speech

# Summary

This report presents baseline results from the initial fine-tuning of Whisper Large V3 on **non-standard Kenyan Swahili speech data**. The model demonstrates promising performance, achieving a test set WER of 27.0% and CER of 10.5%. This output establishes a performance benchmark against which subsequent iterations can be measured, specifically for this challenging dialect.

## 1. Experiment Overview

**Model**: `openai/whisper-large-v3`
**Dataset**: `cdli/kenyan_swahili_nonstandard_speech_v0.9`
**Task**: Transcription (Non-Standard Swahili)

### Key Training Settings
- Learning Rate: 3e-5
- Scheduler: Polynomial decay (power=4)
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
| Train      | 3,949         | 2,855                  |
| Validation | 417           | 272                    |
| Test       | 865           | 554                    |

## 3. Training Progress

| Step | Training Loss | Validation Loss | WER      | CER      |
|------|---------------|-----------------|----------|----------|
| 0  | No log      | 1.819755       | 0.723024 | 0.306196 |
| 50  | 0.938100      | 1.091869       | 0.569935 | 0.202795 |
| 100  | 1.007300      | 0.932511        | 0.490911 | 0.178671 |
| 150  | 0.899100      | 0.880250        | 0.473909 | 0.190529 |
| 200  | 0.78110       | 0.826931       | 0.447487 | 0.172235 |
| 250  | 0.978100      | 0.782634        | 0.402978 | 0.161100 |
| 300  | 0.637000      | 0.755129        | 0.376455 | 0.152901 |
| 350  | 0.794900      | 0.727206        | 0.366075 | 0.152198 |
| 400  | 0.566300      | 0.734376        | 0.353400 | 0.142153 |
| 450  | 0.632600      | 0.710018        | 0.360559 | 0.141856 |
| 500  | 0.507900      | 0.705538        | 0.346381 | 0.135529 |
| 600  | 0.674900      | 0.696160        | 0.343000 | 0.137328 |
| 700  | 0.805900      | 0.690501        | 0.336182 | 0.135598 |
| 800  | 0.532200      | 0.691021        | 0.337020 | 0.135724 |
| 900  | 0.746800      | 0.691489        | 0.336311 | 0.135221 |
| 1000 | 0.490300      | 0.691493        | 0.336028 | 0.135273 |

Training Observations: The model shows consistent improvement until step 700, after which performance plateaus, suggesting potential early stopping opportunities in future iterations

## 4. Final Evaluation Results

### Development Set
- **Loss:** 0.691
- **WER:** 0.336
- **CER:** 0.135

### Test Set
- **Loss:** 0.625
- **WER:** 0.270
- **CER:** 0.105

## 5. Model Availability

The fine-tuned model is publicly available on the Hugging Face Hub:
- Model: [smainye/sw_finetunned_whisper_large_v3_model_baseline](https://huggingface.co/smainye/sw_finetunned_whisper_large_v3_model_baseline)

## 6. Technical Notes

- Training utilized gradient checkpointing for memory efficiency
- Best model selection based on WER & CER metric
- Training completed with model checkpoints saved every 50 steps
- Used polynomial learning rate decay with warmup (50 steps)

## 7. Recommended next steps

1. Hyperparameter Optimization

- Conduct comprehensive learning rate sweep (1e-6 to 1e-4)

- Experiment with cosine annealing vs polynomial decay schedulers

- Test larger batch sizes with gradient accumulation

- Optimize warmup steps and decay parameters

2. Dataset Analysis & Enhancement
- Perform detailed error analysis on high-WER samples from the **non-standard Swahili speech data**.

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
