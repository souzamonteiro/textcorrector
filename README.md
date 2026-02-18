# Text Corrector with Ollama

A Python script that automatically corrects text files using Ollama AI models. Perfect for fixing transcription errors from audio recordings.

## Features

- Batch process multiple text files
- Uses Ollama AI models for text correction
- Command-line interface with flexible options
- Progress tracking and error handling
- Automatic output directory creation

## Prerequisites

1. **Ollama** installed and running on your system
   - Download from: https://ollama.ai/
   - Install and start the Ollama service

2. **Python 3.x** installed

3. Pull the model you want to use:
   ```bash
   ollama pull llama3
   # or
   ollama pull mistral
   ```

## Installation

1. Clone or download this repository
2. Make sure Ollama is running
3. No additional Python packages are required (uses only standard library)

## Usage

```bash
python text_corrector.py --input ./input_texts --output ./corrected_texts --model llama3
```

### Options

- `--input` or `-i`: Directory containing .txt files to be corrected *(required)*
- `--output` or `-o`: Directory where corrected files will be saved *(required)*
- `--model` or `-m`: Ollama model to use (default: llama3)

### Examples

```bash
# Basic usage
python text_corrector.py --input ./transcriptions --output ./corrected --model llama3

# Using different model
python text_corrector.py -i ./audio_texts -o ./fixed_texts -m mistral

# Short paths
python text_corrector.py -i . -o ./output -m codellama
```

## How It Works

1. The script reads all `.txt` files from the input directory
2. For each file, it sends the content to Ollama with the prompt:
   > "The following text came from an audio transcription. Can you correct it?"
3. Saves the corrected text to the output directory with prefix "corrected_"

## Directory Structure Example

```
textcorrector/
├── text_corrector.py
├── inbox/
│   ├── lecture1.txt
│   ├── meeting_notes.txt
│   └── interview.txt
└── outbox/                          # Auto-created
    ├── corrected_lecture1.txt
    ├── corrected_meeting_notes.txt
    └── corrected_interview.txt
```

## Error Handling

- Files that fail to process will show error messages
- Timeout errors for long-running corrections
- Invalid directories are detected and reported
- Encoding issues are handled gracefully

## License

Apache-2.0 license - Feel free to modify and distribute

## Contributing

Suggestions and improvements are welcome! Please submit issues or pull requests.

---

**Note**: Make sure Ollama is running before executing the script. The first time using a model may take longer as it downloads the necessary files.