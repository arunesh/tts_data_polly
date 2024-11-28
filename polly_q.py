import os

import boto3
from botocore.exceptions import BotoCoreError, ClientError

AWS_REGIONS = [
    "us-east-1",      # US East (N. Virginia)
    "us-east-2",      # US East (Ohio)
    "us-west-1",      # US West (N. California) 
    "us-west-2",      # US West (Oregon)
    "ca-central-1",   # Canada (Central)
    "eu-west-1",      # Europe (Ireland)
    "eu-west-2",      # Europe (London)
    "eu-west-3",      # Europe (Paris)
    "eu-central-1",   # Europe (Frankfurt)
    "eu-north-1",     # Europe (Stockholm)
    "ap-northeast-1", # Asia Pacific (Tokyo)
    "ap-northeast-2", # Asia Pacific (Seoul)
    "ap-southeast-1", # Asia Pacific (Singapore)
    "ap-southeast-2", # Asia Pacific (Sydney)
    "ap-south-1",     # Asia Pacific (Mumbai)
    "sa-east-1"       # South America (São Paulo)
]

def generate_speech(text, output_file="speech.mp3", voice_id="Joanna", language_code="en-US", region="us-east-1"):
    """
    Generate speech from text using Amazon Polly and save to a file
    
    Args:
        text (str): The text to convert to speech
        output_file (str): Path to save the audio file (default: speech.mp3)
        voice_id (str): Polly voice ID to use (default: Joanna)
        language_code (str): Language code for the input text (default: en-US)
    """
    try:
        # Create a client using specified AWS region
        polly_client = boto3.client('polly', region_name=region)
        # Request speech synthesis
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice_id,
            Engine='neural',  # Using neural engine for better quality
            LanguageCode=language_code  # Added language code parameter
        )
        
        # Write the audio stream to file
        if "AudioStream" in response:
            with open(output_file, 'wb') as file:
                file.write(response['AudioStream'].read())
            print(f"Audio saved successfully to {output_file}")
        
    except (BotoCoreError, ClientError) as error:
        print(f"Error generating speech: {error}")
        raise
    except IOError as error:
        print(f"Error saving audio file: {error}")
        raise




# Example usage:
# generate_speech("Hello, this is a test of Amazon Polly text to speech.")
def generate_speech_dataset(language_code, dataset_path, output_dir, num_samples=100):
    """
    Generate speech audio files from CCMatrix dataset for a given language
    
    Args:
        language_code (str): Target language code (e.g. 'es-ES' for Spanish)
        dataset_path (str): Path to CCMatrix dataset file
        output_dir (str): Directory to save generated audio files
        num_samples (int): Number of samples to generate (default: 100)
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Map of language codes to Polly voices
    voice_map = {
        'es-ES': 'Lucia',
        'fr-FR': 'Lea',
        'de-DE': 'Vicki',
        'it-IT': 'Bianca',
        'pt-PT': 'Ines'
        # Add more language-voice mappings as needed
    }
    
    if language_code not in voice_map:
        raise ValueError(f"Unsupported language code: {language_code}")
        
    voice_id = voice_map[language_code]
    count = 0
    
    try:
        with open(dataset_path, 'r', encoding='utf-8') as file:
            for line in file:
                if count >= num_samples:
                    break
                    
                # CCMatrix format is typically: source_text\ttarget_text
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    target_text = parts[1]  # Get the foreign language text
                    
                    # Generate unique filename for each audio file
                    output_file = os.path.join(output_dir, f"sample_{count}_{language_code}.mp3")
                    
                    try:
                        generate_speech(
                            text=target_text,
                            output_file=output_file,
                            voice_id=voice_id,
                            language_code=language_code
                        )
                        count += 1
                        
                    except Exception as e:
                        print(f"Error processing sample {count}: {e}")
                        continue
                        
        print(f"Successfully generated {count} audio samples in {output_dir}")
        
    except Exception as e:
        print(f"Error reading dataset file: {e}")
        raise

# Example usage:
# generate_speech_dataset('es-ES', 'path/to/ccmatrix/en-es.tsv', 'output/spanish_audio')

generate_speech("Hello, this is a test of Amazon Polly text to speech.")
