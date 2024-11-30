import os
import time

import boto3
from botocore.exceptions import BotoCoreError, ClientError

AWS_REGIONS = [
    "us-east-1",      # US East (N. Virginia)    
    "us-west-2",      # US West (Oregon)
    "ca-central-1",   # Canada (Central)
    "eu-west-1",      # Europe (Ireland)
    #"eu-west-2",      # Europe (London)
    #"eu-west-3",      # Europe (Paris)
    #"eu-central-1",   # Europe (Frankfurt)
    #"ap-northeast-1", # Asia Pacific (Tokyo)
    #"ap-northeast-2", # Asia Pacific (Seoul)
    #"ap-northeast-3",
    #"ap-southeast-1", # Asia Pacific (Singapore)
    #"ap-southeast-2", # Asia Pacific (Sydney)
    #"ap-south-1",     # Asia Pacific (Mumbai)
]

POLLY_CLIENTS = {
    'us-east-1': boto3.client('polly', region_name='us-east-1'),
    'us-west-2': boto3.client('polly', region_name='us-west-2'), 
    'ca-central-1': boto3.client('polly', region_name='ca-central-1'),
    'eu-west-1': boto3.client('polly', region_name='eu-west-1')
}

AWS_VOICE_MAP = {
        'es-ES': 'Lucia',
        'fr-FR': 'Lea',
        'de-DE': 'Vicki',
        'it-IT': 'Bianca',
        'pt-PT': 'Ines',
        'hi-IN': 'Kajal',
        'ja-JP': 'Takumi',
        # Add more language-voice mappings as needed
    }

def generate_speech(text, output_file="speech.mp3", voice_id="Joanna", language_code="en-US", region="us-east-1", engine='neural'):
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
        polly_client = POLLY_CLIENTS[region]
        # Request speech synthesis
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice_id,
            Engine=engine,  # Using neural engine for better quality
            LanguageCode=language_code  # Added language code parameter
        )
        
        # Write the audio stream to file
        if "AudioStream" in response:
            with open(output_file, 'wb') as file:
                file.write(response['AudioStream'].read())
            print(f"Audio saved successfully to {output_file} in region {region}")
        
    except (BotoCoreError, ClientError) as error:
        print(f"Error generating speech for region {region} : {error}")
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
        'it-IT': 'Cristiano',
        'pt-PT': 'Ines',
        'hi-IN': 'Kajal',
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
                            language_code=language_code,
                            engine=engine
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
def generate_speech_from_file(input_file, output_dir, voice_id='Joanna', language_code='en-US'):
    """
    Generate speech audio files from lines in a text file using Amazon Polly.
    
    Args:
        input_file (str): Path to input text file
        output_dir (str): Directory to save generated audio files
        voice_id (str): Amazon Polly voice ID to use (default: Joanna)
        language_code (str): Language code for the voice (default: en-US)
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    count = 0
    region_index = 0
    region_count = 0
    last_ts = int(time.time() * 1000)
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                    
                output_file = os.path.join(output_dir, f'speech_{language_code}_{count:04d}.mp3')
                region_index = int(region_count / 8)
                if (region_index >= len(AWS_REGIONS)):
                    current_ts = int(time.time() * 1000)
                    if (current_ts - last_ts < 1.0):
                        print("Adding delay.")
                        time.sleep(current_ts - last_ts + 0.1)
                    last_ts = current_ts
                    region_index = 0
                    region_count = 0

                engine = "neural"
                if language_code == "pt-PT":
                    engine = "standard"
                try:
                    generate_speech(
                        text=line,
                        output_file=output_file,
                        voice_id=voice_id,
                        language_code=language_code,
                        region=AWS_REGIONS[region_index],
                        engine=engine
                    )
                    count += 1
                    region_count += 1
                    
                except Exception as e:
                    print(f"Error processing line {count}: {e}")
                    continue
                    
        print(f"Successfully generated {count} audio files in {output_dir}")
        
    except Exception as e:
        print(f"Error reading input file: {e}")
        raise


def main():
    """
    Main function to run speech generation from command line arguments.
    Expected arguments: input_file output_dir voice_id language_code
    """
    import sys
    
    if len(sys.argv) != 5:
        print("Usage: python polly_q.py input_file output_dir voice_id language_code")
        print("Example: python polly_q.py input.txt output/audio Lucia es-ES")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_dir = sys.argv[2] 
    voice_id = sys.argv[3]
    language_code = sys.argv[4]
    
    try:
        generate_speech_from_file(
            input_file=input_file,
            output_dir=output_dir,
            voice_id=voice_id,
            language_code=language_code
        )
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

