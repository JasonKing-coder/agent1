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

def generate_article(transcript_text):
    print("--- Generating Article ---")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a professional content creator and ghostwriter. Your goal is to take a raw transcription and turn it into a compelling, high-quality blog post. Use Markdown formatting, include a catchy title, subheadings, and a concluding summary. Make it engaging and ready for publication."},
            {"role": "user", "content": f"Here is the transcription: {transcript_text}"}
        ]
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
    
    try:
        transcript = transcribe_file(target_file)
        print(f"Transcription complete. Length: {len(transcript)} characters.")
        
        article = generate_article(transcript)
        
        with open("output.md", "w", encoding="utf-8") as f:
            f.write(article)
        
        print("--- Success! ---")
        print("The final article has been saved to output.md")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
