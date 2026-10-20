import os
import openai
from dotenv import load_dotenv
import sys
import json

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
    
    # Define the different types of content we want to generate
    prompts = {
        "blog": "You are a professional content creator. Turn this transcription into a high-quality, SEO-optimized blog post. Use Markdown, include a catchy title, subheadings, and a concluding summary. Make it engaging and ready for publication.",
        "newsletter": "You are a newsletter editor. Summarize this transcription into a concise, punchy newsletter. Include a 'Key Takeaways' section and a 'Call to Action'.",
        "social_media": "You are a social media manager. Create two pieces of content from this transcription: 1) A Twitter (X) thread of 5-7 tweets. 2) A professional LinkedIn post. Format them clearly.",
        "youtube": "You are a YouTube strategist. Create a YouTube video description, a list of 10 relevant tags, and a suggested title based on this transcription."
    }

    results = {}
    for content_type, prompt in prompts.items():
        print(f"Generating {content_type}...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Here is the transcription: {transcript_text}"}
            ]
        )
        results[content_type] = response.choices[0].message.content
    
    return results

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
        # 1. Transcribe
        transcript = transcribe_file(target_file)
        print(f"Transcription complete. Length: {len(transcript)} characters.")
        
        # 2. Generate Package
        package = generate_content_package(transcript)
        
        # 3. Save results
        os.makedirs("output", exist_ok=True)
        
        with open("output/blog.md", "w", encoding="utf-8") as f:
            f.write(package["blog"])
        with open("output/newsletter.md", "w", encoding="utf-8") as f:
            f.write(package["newsletter"])
        with open("output/social_media.md", "w", encoding="utf-8") as f:
            f.write(package["social_media"])
        with open("output/youtube.md", "w", encoding="utf-8") as f:
            f.write(package["youtube"])
        
        print("--- Success! ---")
        print("The content package has been saved to the 'output/' directory:")
        print("- blog.md")
        print("- newsletter.md")
        print("- social_media.md")
        print("- youtube.md")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
