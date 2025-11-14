# Model Push to Hugging Face Hub

This script pushes trained Whisper models from Modal volume storage to Hugging Face Hub.

## Available Commands

### 1. Explore Volume Contents
```bash
modal run push_model_to_hf.py::explore
```

### 2. List Available Models

```bash 
modal run push_model_to_hf.py::list_available_models
```

- Shows all trained models with their paths and indicates which ones have `best_model` directories ready for upload.

### 3. Test Model Loading

```bash
modal run push_model_to_hf.py::test_model --model-path "trained_models/your_model_name/best_model"
```

- Verifies that a specific model can be loaded successfully before uploading.

### 4. Push Model to Hugging Face

``` bash
modal run push_model_to_hf.py::main \
  --model-path "trained_models/your_model_name/best_model" \
  --repo-id "your-username/your-model-name" \
  --commit-message "Your commit message" \
  --private
```

### Parameters:

* `--model-path` : Path to model in Modal volume (relative to /jupyter_kernel)

* `--repo-id` : HuggingFace repository ID (format: username/model-name)

* `--commit-message` : Description of the upload (optional)

* `--private` : Make repository private (optional flag)


### Prerequisites

* Modal account and CLI configured

* Hugging Face token stored as Modal secret named huggingface-secret

* Trained models stored in jupyter_kernel volume under trained_models/

### Workflow

* Explore → Check what's in your volume

* List → Find available models

* Test → Verify model loads correctly

* Push → Upload to Hugging Face Hub

