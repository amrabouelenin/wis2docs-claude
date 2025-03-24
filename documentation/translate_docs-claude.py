import os
import anthropic
import markdown
import time

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
# OPENAI_API_KEY =os.getenv('OPENAI_API_KEY')

# openai.api_key = OPENAI_API_KEY
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def translate_text(text, target_language):
    prompt = f"Translate the following Markdown content into {target_language}:\n\n{text}"
    
    response = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=4000,
        system="You are a Markdown-aware translator.",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    
    # Extract the translated text from the response
    translated_text = response.content[0].text
    return translated_text

def process_markdown_files(input_folder, output_folder, languages):
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}")
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                for lang in languages:
                    # get lang_code from lang_dict
                    lang_path = lang_dict[lang]
                    # file_path i.e docs/en/ctical-sessions/accessing-your-student-vm.md
                    # relative_path i.e. practical-sessions/
                    relative_path = os.path.relpath(file_path, input_folder)
                    relative_path = os.path.dirname(relative_path)
                    print(f"relative path: {relative_path}")
                    target_dir = os.path.join(output_folder, lang_path, relative_path)
                    os.makedirs(target_dir, exist_ok=True)
                    # final target path i.e. docs/zh/practical-session/file.md
                    target_file_path = os.path.join(target_dir, file)   
                    print(f"target file path: {target_file_path}")
                    # check if target_file_path exists the file exists then skip the translation
                    if os.path.exists(target_file_path):
                        print(f"Skipping {file} to {lang} as file already exists")
                        continue
                    
                    print(f"Translating {file} to {lang}")
                    translated_text = translate_text(content, lang)
                    print(f"writting translated text to {target_file_path}")
                    with open(target_file_path, "w", encoding="utf-8") as f:
                        f.write(translated_text)

                    print(f"Translated {file} to {lang}")

                time.sleep(1)  # Avoid rate limits

# Set paths
input_folder = "docs/en"  # Change this to your Markdown folder
output_folder = "docs"
# languages = ["Portuguese", "French"]
# Arabic, Chinese, English, French, Russian and Spanish
# lang_dict contain lang_name and lang_code
lang_dict = {
    # "Arabic": "ar",
    # "Chinese": "zh",
    # "French": "fr",
    # "Russian": "ru",
    # "Spanish": "es",
    # "Portuguese": "pt",
    "German": "de",
    # "Italian": "it",
}

# Run translation
process_markdown_files(input_folder, output_folder, lang_dict)
