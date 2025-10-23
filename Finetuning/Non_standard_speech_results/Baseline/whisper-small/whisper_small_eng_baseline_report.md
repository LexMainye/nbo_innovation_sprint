# Baseline Report: Fine-tuning the Whisper-Small Model on Non-Standard Kenyan English

*This report documents my initial baseline experiment and establishes a starting point for future improvements.*

## 1. Objective

The primary objective of this **baseline experiment** was to establish an initial proof-of-concept for adapting a pre-trained Whisper model to improve transcription accuracy on non-standard Kenyan English. This serves as my foundation for more sophisticated fine-tuning approaches in future iterations.

## 2. Methodology

### 2.1. The Model: Whisper-Small

I selected `openai/whisper-small` as my starting point for this baseline test, prioritizing computational efficiency for initial experimentation.

*   **Total Parameters:** 241,734,912
*   **Trainable Parameters (in this baseline):** 127,986,432

### 2.2. The Dataset: Non-Standard Kenyan English Speech

The `cdli/kenyan_english_nonstandard_speech_v0.9` dataset was filtered to match Whisper's 30-second input constraint:

| Split      | Original Size | Filtered Size (<= 30s) |
|------------|---------------|------------------------|
| Train      | 4,236         | 3,130                  |
| Validation | 572           | 342                    |
| Test       | 993           | 705                    |

### 2.3. Baseline Fine-Tuning Strategy

For this initial approach, I implemented a conservative fine-tuning strategy:

*   **Partial Fine-tuning:** I froze the decoder weights to preserve language modeling capabilities, training only the **encoder** and **projection layer**
*   **Basic Data Augmentation:** Used SpecAugment as a starting point for robustness
*   **Initial Hyperparameters:** These represent my first configuration attempt and will be optimized in future work:
    *   **Learning Rate:** 1e-4
    *   **LR Scheduler:** Polynomial decay
    *   **Warmup Steps:** 50
    *   **Batch Size:** 32
    *   **Max Steps:** 1000
    *   **Epochs:** 10

## 3. Baseline Results

### 3.1. Complete Training Progress

The model was trained for 1000 steps with detailed monitoring throughout the process. The table below shows the complete training progression:

| Step | Training Loss | Validation Loss | WER      | CER      |
|------|---------------|-----------------|----------|----------|
| 0    | No log        | 1.424880        | 0.278409 | 0.166156 |
| 50   | 0.935700      | 0.737602        | 0.216053 | 0.123037 |
| 100  | 0.713700      | 0.687359        | 0.216708 | 0.132061 |
| 150  | 0.502300      | 0.679826        | 0.203396 | 0.122316 |
| 200  | 0.362500      | 0.668027        | 0.204071 | 0.122224 |
| 250  | 0.318100      | 0.665594        | 0.202272 | 0.118560 |
| 300  | 0.219300      | 0.649036        | 0.182868 | 0.105684 |
| 350  | 0.295200      | 0.654805        | 0.188066 | 0.109171 |
| 400  | 0.205200      | 0.655462        | 0.184652 | 0.106480 |
| 450  | 0.224000      | 0.662525        | 0.186053 | 0.109224 |
| 500  | 0.167100      | 0.666398        | 0.180363 | 0.101654 |
| 550  | 0.168000      | 0.672540        | 0.185231 | 0.106131 |
| 600  | 0.167600      | 0.671067        | 0.184393 | 0.105272 |
| 650  | 0.152700      | 0.673863        | 0.184035 | 0.106334 |
| 700  | 0.165600      | 0.673125        | 0.181144 | 0.103453 |
| 750  | 0.159000      | 0.674710        | 0.186322 | 0.107135 |
| 800  | 0.161100      | 0.674365        | 0.185028 | 0.105985 |
| 850  | 0.145500      | 0.674453        | 0.185355 | 0.106129 |
| 900  | 0.160800      | 0.674399        | 0.184706 | 0.105806 |
| 950  | 0.148300      | 0.674431        | 0.184282 | 0.105735 |
| 1000 | 0.170000      | 0.674457        | 0.185004 | 0.105964 |

### Key Training Observations:
- **Rapid initial improvement**: WER dropped from 27.8% to 18.2% in the first 300 steps
- **Stabilization phase**: Performance plateaued around step 500, suggesting potential for better convergence strategies
- **Best validation WER**: 18.0% achieved at step 500
- **Training loss continued decreasing** while validation metrics stabilized, indicating potential for improved regularization

### 3.2. Final Baseline Evaluation

After training, the model with the best validation WER was loaded for final evaluation:

**Development Set:**
- **Loss:** 0.666
- **WER:** 0.180
- **CER:** 0.102

**Test Set:**
- **Loss:** 0.604
- **WER:** 0.123
- **CER:** 0.065

## 4. Current Deployment

This baseline model is available as a starting point for the modelling research:
[smainye/eng_finetunned_tune_whisper_small_model_baseline](https://huggingface.co/smainye/eng_finetunned_tune_whisper_small_model_baseline)

## 5. Conclusion & Future Directions

This baseline experiment successfully demonstrates that even with conservative fine-tuning, significant improvements can be achieved for Kenyan English transcription. The test set WER of 12.3% provides a solid foundation, but I consider this just the beginning.

### Key Limitations of This Baseline:
- Suboptimal convergence in later training stages
- Conservative approach with frozen decoder
- Limited hyperparameter exploration
- Basic data augmentation strategy
- Training plateau after step 500 suggests need for better optimization

### Planned Improvements:
I'm actively working on the following enhancements:
- **Full model fine-tuning** (unfreezing decoder)
- **Advanced hyperparameter optimization** with learning rate scheduling
- **More sophisticated data augmentation** techniques
- **Larger model variants** (Whisper-medium/large)
- **Early stopping** strategies to prevent plateauing
- **Cross-validation** for more robust evaluation
- **Ensemble methods** and **transfer learning** from other dialects

### Training Insights for Future Work:
The complete training table reveals several opportunities:
- Earlier learning rate adjustments could improve convergence
- Additional regularization might help with the validation loss plateau
- The gap between training and validation metrics suggests room for better generalization techniques

This baseline model serves as a reproducible starting point and performance benchmark. I welcome community feedback and collaboration to build upon these initial results.

---

*This report documents my initial baseline findings. I'm committed to iterating and improving upon these results in subsequent versions.*
