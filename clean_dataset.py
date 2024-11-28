import os
import re
import unicodedata


def filter_language_sentences(input_file, output_file, allowed_chars):
    """
    Filter sentences from input file, keeping only those that contain characters
    from the specified language character set.
    
    Args:
        input_file (str): Path to input text file
        output_file (str): Path to output filtered text file
        allowed_chars (str): String containing all allowed characters for the language
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:
            
            for line in infile:
                line = line.strip()
                # Skip empty lines
                if not line:
                    continue
                    
                # Check if all characters (excluding whitespace) are in allowed set
                if all(char in allowed_chars or char.isspace() for char in line):
                    outfile.write(line + '\n')
                    
        print(f"Filtered sentences written to {output_file}")
                    
    except IOError as error:
        print(f"Error processing files: {error}")
        raise

# Example character sets for different languages
SPANISH_CHARS = "abcdefghijklmnñopqrstuvwxyzáéíóúü¿¡ABCDEFGHIJKLMNÑOPQRSTUVWXYZÁÉÍÓÚÜ.,;:\"'()!?"
FRENCH_CHARS = "abcdefghijklmnopqrstuvwxyzàâäéèêëîïôöùûüÿçœæABCDEFGHIJKLMNOPQRSTUVWXYZÀÂÄÉÈÊËÎÏÔÖÙÛÜŸÇŒÆ.,;:\"'()!?"
GERMAN_CHARS = "abcdefghijklmnopqrstuvwxyzäöüßABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ.,;:\"'()!?"
HINDI_CHARS = "अआइईउऊएऐओऔकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहक्षत्रज्ञड़ढ़।॥॰॒॑ँंःािीुूृॄेैोौ्.,;:\"'()!?"


def main():
    """
    Main function to run the language filtering script from command line arguments.
    Expected arguments: input_file output_file language
    Supported languages: spanish, french, german, hindi
    """
    import sys
    
    if len(sys.argv) != 4:
        print("Usage: python clean_dataset.py input_file output_file language")
        print("Supported languages: spanish, french, german, hindi")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    language = sys.argv[3].lower()
    
    # Map language names to character sets
    language_chars = {
        'spanish': SPANISH_CHARS,
        'french': FRENCH_CHARS,
        'german': GERMAN_CHARS,
        'hindi': HINDI_CHARS
    }
    
    if language not in language_chars:
        print(f"Error: Unsupported language '{language}'")
        print("Supported languages: spanish, french, german, hindi")
        sys.exit(1)
        
    try:
        filter_language_sentences(input_file, output_file, language_chars[language])
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
