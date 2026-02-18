import os
import subprocess
import argparse
import sys

def correct_text_with_ollama(text, model):
    """Correct text using Ollama"""
    prompt = (
        "The following text came from an audio transcription. Can you correct it? "
        "Return ONLY the corrected text, without any additional comments, explanations, "
        "or formatting. Return only the clean corrected text.\n\n"
        f"Text: {text}"
    )

    try:
        # Using subprocess to call Ollama
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=120,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            # Return only the corrected text, stripped of extra whitespace
            return result.stdout.strip()
        else:
            print(f"Ollama error: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        print("Timeout when calling Ollama")
        return None
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return None

def process_files(input_dir, output_dir, model):
    """Process all .txt files from input directory"""
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # List .txt files
    files = [f for f in os.listdir(input_dir) 
             if f.lower().endswith('.txt') and os.path.isfile(os.path.join(input_dir, f))]
    
    if not files:
        print("No .txt files found in input directory")
        return
    
    print(f"Found {len(files)} files to process")
    
    for i, file in enumerate(files, 1):
        input_path = os.path.join(input_dir, file)
        output_path = os.path.join(output_dir, f"corrected_{file}")
        
        print(f"Processing file {i}/{len(files)}: {file}")
        
        # Read file content
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file {file}: {e}")
            continue
        
        # Correct text with Ollama
        corrected_text = correct_text_with_ollama(content, model)
        
        if corrected_text:
            # Save result - ONLY the corrected text
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(corrected_text)
                print(f"Corrected file saved: {output_path}")
            except Exception as e:
                print(f"Error saving file {output_path}: {e}")
        else:
            print(f"Failed to correct file: {file}")

def main():
    parser = argparse.ArgumentParser(
        description="Correct texts from files using Ollama",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:
  python text_corrector.py --input ./original_texts --output ./corrected_texts --model llama3
  python text_corrector.py -i /input/path -o /output/path -m mistral
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Directory containing .txt files to be corrected'
    )
    
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Directory where corrected files will be saved'
    )
    
    parser.add_argument(
        '--model', '-m',
        default='llama3',
        help='Ollama model to use (default: llama3)'
    )
    
    args = parser.parse_args()
    
    # Check if directories exist
    if not os.path.exists(args.input):
        print(f"Error: Input directory '{args.input}' does not exist")
        sys.exit(1)
    
    if not os.path.isdir(args.input):
        print(f"Error: '{args.input}' is not a directory")
        sys.exit(1)
    
    # Process files
    process_files(args.input, args.output, args.model)

if __name__ == "__main__":
    main()
