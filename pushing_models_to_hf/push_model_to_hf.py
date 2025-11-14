"""
Push trained Whisper model from Modal storage to Hugging Face Hub

This script:
1. Loads a trained model from Modal volume storage
2. Pushes it to Hugging Face Hub
"""

import os
import modal

# Create Modal app
app = modal.App("push-model-to-hf")

# Create volume reference - using jupyter_kernel volume (fixed deprecation)
volume = modal.Volume.from_name("jupyter_kernel")

# Create image with required dependencies
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "transformers>=4.30.0",
        "torch>=2.0.0",
        "huggingface_hub>=0.16.0",
    )
)


@app.function(
    image=image,
    volumes={"/jupyter_kernel": volume},
    secrets=[modal.Secret.from_name("huggingface-secret")],
    timeout=3600,
)
def push_model_to_huggingface(
    model_path: str,
    repo_id: str,
    commit_message: str = "Upload fine-tuned Whisper model",
    private: bool = False,
):
    """
    Push a model from Modal storage to Hugging Face Hub
    
    Args:
        model_path: Path to model in Modal volume (e.g., "trained_models/en_nonstandard_tune_whisper_small_run3/best_model")
        repo_id: HuggingFace repo ID (e.g., "my-username/whisper-small-kenyan-english")
        commit_message: Commit message for the upload
        private: Whether to create a private repo
    """
    from huggingface_hub import create_repo
    from transformers import WhisperForConditionalGeneration, WhisperProcessor
    
    # Full path in the mounted volume
    full_model_path = f"/jupyter_kernel/{model_path.lstrip('/')}"
    
    print(f"Loading model from: {full_model_path}")
    
    # Check if path exists
    if not os.path.exists(full_model_path):
        raise FileNotFoundError(f"Model path does not exist: {full_model_path}")
    
    # Load the model and processor
    print("Loading model and processor...")
    try:
        model = WhisperForConditionalGeneration.from_pretrained(full_model_path)
        processor = WhisperProcessor.from_pretrained(full_model_path)
        print("✅ Model and processor loaded successfully")
    except Exception as e:
        raise Exception(f"Failed to load model or processor: {e}")
    
    # Get HF token from environment (set via Modal secret)
    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        raise ValueError("HF_TOKEN not found in environment variables")
    
    # Create repository if it doesn't exist
    print(f"Creating/checking repository: {repo_id}")
    try:
        create_repo(
            repo_id=repo_id,
            token=hf_token,
            private=private,
            repo_type="model",
            exist_ok=True,
        )
        print("✅ Repository created/verified")
    except Exception as e:
        print(f"Note: Repository creation check - {e}")
    
    # Push model to hub
    print(f"Pushing model to {repo_id}...")
    try:
        model.push_to_hub(
            repo_id=repo_id,
            token=hf_token,
            commit_message=commit_message,
            private=private,
        )
        print("✅ Model pushed successfully")
    except Exception as e:
        raise Exception(f"Failed to push model: {e}")
    
    # Push processor to hub
    print(f"Pushing processor to {repo_id}...")
    try:
        processor.push_to_hub(
            repo_id=repo_id,
            token=hf_token,
            commit_message=commit_message,
            private=private,
        )
        print("✅ Processor pushed successfully")
    except Exception as e:
        raise Exception(f"Failed to push processor: {e}")
    
    print(f"✅ Successfully pushed model to https://huggingface.co/{repo_id}")
    return f"https://huggingface.co/{repo_id}"


@app.local_entrypoint()
def main(
    model_path: str = "trained_models/sw_nonstandard_tune_whisper_small_run3/best_model",
    repo_id: str = "smainye/whisper-small-kenyan-swahili-nonstandard",
    commit_message: str = "Upload fine-tuned Whisper Small model on Kenyan Swahili non-standard speech",
    private: bool = False,
):
    """
    Main entry point for pushing model to Hugging Face
    
    Usage:
        modal run push_model_to_hf.py::main
        
        # With custom settings:
        modal run push_model_to_hf.py::main --model-path path/to/model --repo-id username/model-name
    """
    if repo_id is None:
        raise ValueError("Please provide --repo-id argument")
    
    print(f"🚀 Starting model upload process...")
    print(f"📦 Volume: jupyter_kernel")
    print(f"📁 Model path: {model_path}")
    print(f"🎯 Target repo: {repo_id}")
    print(f"🔒 Private: {private}")
    print(f"📝 Commit message: {commit_message}")
    print("-" * 60)
    
    try:
        result = push_model_to_huggingface.remote(
            model_path=model_path,
            repo_id=repo_id,
            commit_message=commit_message,
            private=private,
        )
        
        print(f"\n🎉 Model uploaded successfully!")
        print(f"🔗 View at: {result}")
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        raise


# Function to list available models in the jupyter_kernel volume
@app.function(
    image=image,
    volumes={"/jupyter_kernel": volume},
)
def list_models():
    """List all available models in the jupyter_kernel volume"""
    import os
    
    base_dir = "/jupyter_kernel/trained_models"
    
    if not os.path.exists(base_dir):
        print(f"Directory not found: {base_dir}")
        print("Available directories in /jupyter_kernel:")
        for item in os.listdir("/jupyter_kernel"):
            item_path = os.path.join("/jupyter_kernel", item)
            if os.path.isdir(item_path):
                print(f"📁 {item}")
            else:
                print(f"📄 {item}")
        return []
    
    print(f"📂 Available models in {base_dir}:")
    print("=" * 60)
    
    models_found = []
    for model_dir in os.listdir(base_dir):
        model_path = os.path.join(base_dir, model_dir)
        if os.path.isdir(model_path):
            best_model_path = os.path.join(model_path, "best_model")
            has_best = os.path.exists(best_model_path)
            status = "✅ [has best_model]" if has_best else "❌ [no best_model]"
            print(f"  📁 {model_dir} {status}")
            if has_best:
                print(f"     → {best_model_path}")
                models_found.append((model_dir, best_model_path))
    
    print(f"\n📊 Found {len(models_found)} models with 'best_model' directory")
    return models_found


@app.local_entrypoint()
def list_available_models():
    """List all models in jupyter_kernel volume"""
    print("🔍 Scanning for available models in jupyter_kernel volume...")
    models = list_models.remote()
    if models:
        print(f"\n💡 To push a model, run:")
        print(f"   modal run push_model_to_hf.py::main --model-path trained_models/YOUR_MODEL/best_model --repo-id your-username/your-model-name")
    else:
        print(f"\n💡 Check available directories with:")
        print(f"   modal run push_model_to_hf.py::explore")


# Function to explore the jupyter_kernel volume
@app.function(
    image=image,
    volumes={"/jupyter_kernel": volume},
)
def explore_volume():
    """Explore contents of jupyter_kernel volume"""
    import os
    
    volume_path = "/jupyter_kernel"
    
    print(f"📂 Contents of jupyter_kernel volume:")
    print("=" * 60)
    
    def list_dir(path, indent=0):
        try:
            items = os.listdir(path)
            for item in items:
                full_path = os.path.join(path, item)
                prefix = "  " * indent
                if os.path.isdir(full_path):
                    print(f"{prefix}📁 {item}/")
                    list_dir(full_path, indent + 1)
                else:
                    size = os.path.getsize(full_path)
                    print(f"{prefix}📄 {item} ({size} bytes)")
        except Exception as e:
            print(f"{prefix}❌ Cannot access: {e}")
    
    list_dir(volume_path)


@app.local_entrypoint()
def explore():
    """Explore the jupyter_kernel volume contents"""
    explore_volume.remote()


# Test function to verify the model loading
@app.function(
    image=image,
    volumes={"/jupyter_kernel": volume},
)
def test_model_loading(model_path: str):
    """Test if a model can be loaded successfully"""
    from transformers import WhisperForConditionalGeneration, WhisperProcessor
    
    full_model_path = f"/jupyter_kernel/{model_path.lstrip('/')}"
    
    print(f"🧪 Testing model loading from: {full_model_path}")
    
    if not os.path.exists(full_model_path):
        print(f"❌ Path does not exist: {full_model_path}")
        return False
    
    try:
        model = WhisperForConditionalGeneration.from_pretrained(full_model_path)
        processor = WhisperProcessor.from_pretrained(full_model_path)
        print(f"✅ Model loaded successfully!")
        print(f"   Model type: {type(model)}")
        print(f"   Processor type: {type(processor)}")
        return True
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return False


@app.local_entrypoint()
def test_model(
    model_path: str = "trained_models/sw_nonstandard_tune_whisper_small_run3/best_model"
):
    """Test if a specific model can be loaded"""
    success = test_model_loading.remote(model_path)
    if success:
        print("🎉 Model test passed! Ready for upload.")
    else:
        print("💥 Model test failed! Check the model path and files.")