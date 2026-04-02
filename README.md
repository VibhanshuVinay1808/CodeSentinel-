# CodeSentinel

An AI-powered code analysis framework for intelligent test generation, bug detection, and specification generation using transformer models.

## Features

- **Spec Generator**: Generate detailed specifications from requirements using T5 models
- **Test Generator**: Automatically generate unit tests from code and requirements
- **Bug Detector**: Identify buggy code using RoBERTa-based classification
- **End-to-End Pipeline**: Complete workflow from requirement to test and bug analysis

## Installation

### Prerequisites
- Python 3.8+
- Git
- (Optional) CUDA-capable GPU for faster training

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/VibhanshuVinay1808/CodeSentinel.git
   cd CodeSentinel
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   
   # Windows
   .\.venv\Scripts\Activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install sentencepiece (required for T5):**
   ```bash
   pip install sentencepiece
   ```

## Usage

### Fine-tune Bug Detection Model

```bash
python src/detector/train_bug_detector.py --config configs/bug.yaml
```

### Fine-tune Test Generation Model

```bash
python src/generator/train_testgen.py --config configs/testgen.yaml
```

### Run Inference Pipeline

```bash
python src/inference/run_pipeline.py \
  --requirement "User should be able to login with valid credentials" \
  --code_file data/sample_login.py
```

### Run Evaluation

```bash
cd eval
python run_evaluate.py
```

## Project Structure

```
CodeSentinel/
├── src/                          # Source code
│   ├── detector/                 # Bug detection models
│   ├── generator/                # Test generation
│   ├── inference/                # Inference pipeline
│   ├── specs/                    # Specification generation
│   └── utils/                    # Utilities
├── configs/                      # Configuration files (YAML)
├── data/                         # Dataset files
├── eval/                         # Evaluation scripts
├── scripts/                      # Data preparation scripts
├── analysis/                     # Analysis tools
├── notebooks/                    # Jupyter notebooks
├── tests/                        # Test files
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Configuration

All configurations are in `configs/` directory:

- `spec.yaml` - Specification generator config
- `testgen.yaml` - Test generator config
- `bug.yaml` - Bug detector config

## Models

Pre-trained models are stored locally in:
- `spec_model/` - Specification generator
- `testgen_model/` - Test generator
- `codebert_bug/`, `codebert_bug_v1/` - Bug detectors

Models can be uploaded to Hugging Face Hub for easy sharing:
```bash
python upload_models_to_hub.py
```

## License

MIT License

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.
