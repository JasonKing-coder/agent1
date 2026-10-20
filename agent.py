import os
import openai
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_file(file_path):
    print(f"--- Transcribing: {file_path} ---")
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript.text

def generate_content_package(transcript_text):
    print("--- Generating Professional Content Package ---")
    
    system_prompt = """
You are an elite content marketing agency and ghostwriter. 
Your goal is to transform a raw transcript into a high-converting content package.
The content must be professional, engaging, and optimized for SEO.

For each piece of content, use high-quality Markdown formatting.

The package must include:
1. **A Compelling Blog Post**: A long-form article with a catchy title, H2/H3 subheadings, a strong hook, and a clear call to action (CTA).
2. **A Newsletter Version**: A shorter, more personal version of the article suitable for an email list.
3. **A Social Media Thread**: A 5-7 post thread for X (Twitter) that summarizes the key takeaways.
4. **A YouTube Description**: A structured description including a summary, timestamps (placeholders), and relevant hashtags.

Tone: Professional yet accessible.
Target Audience: People looking for actionable value.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Here is the raw transcript. Please generate the full content package:\n\n{transcript_text}"}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

def main():
    # Look for audio/video files in the root directory
    extensions = ('.mp3', '.mp4', '.wav', '.m4a', '.mov')
    files = [f for f in os.listdir('.') if f.lower().endswith(extensions)]

    if not files:
        print("No audio or video files found in the root directory.")
        return

    # Process the first file found
    target_file = files[0]
    print(f"Targeting file: {target_file}")
    
    try:
        transcript = transcribe_file(target_file)
        print(f"Transcription complete. Length: {len(transcript)} characters.")
        
        content_package = generate_content_package(transcript)
        
        # Save the package to a single markdown file
        output_filename = "content_package.md"
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(content_package)
        
        print("--- Success! ---")
        print(f"The professional content package has been saved to {output_filename}")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
