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
    print("--- Generating Multi-Channel Content Package ---")
    prompt = f"""
You are a world-class content marketing agency. Your goal is to take a raw transcription and turn it into a comprehensive multi-channel content package.

The package must include:
1. A long-form, SEO-optimized Blog Post (Markdown).
2. A punchy, engaging Newsletter (Email format).
3. A set of Social Media posts:
   - A Twitter/X thread (5-7 tweets).
   - A professional LinkedIn post.
   - A short, catchy Instagram caption.
4. A YouTube script or detailed video description.

Return the result strictly as a JSON object with the following keys: 
'blog_post', 'newsletter', 'social_media' (an object with 'twitter_thread', 'linkedin_post', 'instagram_caption'), and 'youtube_script'. 
Use Markdown for the content.

Here is the transcription:
{transcript_text}
"""
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a professional content creator and ghostwriter. You output only valid JSON."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)

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
        
        package = generate_content_package(transcript)
        
        # Create output directory
        if not os.path.exists("output"):
            os.makedirs("output")
        
        # Save each component
        with open("output/blog_post.md", "w", encoding="utf-8") as f:
            f.write(package['blog_post'])
        
        with open("output/newsletter.md", "w", encoding="utf-8") as f:
            f.write(package['newsletter'])
        
        with open("output/youtube_script.md", "w", encoding="utf-8") as f:
            f.write(package['youtube_script'])
            
        # Save social media posts
        sm = package['social_media']
        with open("output/twitter_thread.txt", "w", encoding="utf-8") as f:
            f.write(sm['twitter_thread'])
        with open("output/linkedin_post.txt", "w", encoding="utf-8") as f:
            f.write(sm['linkedin_post'])
        with open("output/instagram_caption.txt", "w", encoding="utf-8") as f:
            f.write(sm['instagram_caption'])
        
        print("--- Success! ---")
        print("The full content package has been saved to the 'output/' directory.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
