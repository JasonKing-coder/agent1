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
    print("--- Generating High-Value Content Package ---")
    
    system_prompt = (
        "You are an elite content marketing agency and ghostwriter. "
        "Your goal is to transform a raw transcript into a high-conversion, "
        "multi-channel content package that drives engagement and revenue. "
        "You provide professional, polished, and ready-to-publish content."
    )

    user_prompt = f"""
    Analyze the following transcript and create a complete content package.
    
    TRANSCRIPT:
    {transcript_text}

    REQUIRED OUTPUT FORMAT (JSON):
    {{
        "blog_post": {{
            "title": "Catchy, SEO-optimized title",
            "content": "Full long-form blog post in Markdown with H1, H2, H3 tags, and a concluding summary."
        }},
        "newsletter": {{
            "subject_line": "High-open-rate subject line",
            "body": "A concise, punchy newsletter summary designed for high engagement."
        }},
        "social_media": {{
            "twitter_thread": "A 5-tweet thread summarizing the key points with hooks.",
            "linkedin_post": "A professional, thought-leadership style post for LinkedIn."
        }},
        "youtube": {{
            "script": "A structured video script with Intro, Body, and Outro.",
            "description": "A YouTube description with timestamps, keywords, and a call to action."
        }}
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
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
        output_dir = "content_package"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save Blog Post
        with open(f"{output_dir}/blog_post.md", "w", encoding="utf-8") as f:
            f.write(f"# {package['blog_post']['title']}\n\n{package['blog_post']['content']}")
        
        # Save Newsletter
        with open(f"{output_dir}/newsletter.md", "w", encoding="utf-8") as f:
            f.write(f"Subject: {package['newsletter']['subject_line']}\n\n{package['newsletter']['body']}")
        
        # Save Social Media
        with open(f"{output_dir}/social_media.md", "w", encoding="utf-8") as f:
            f.write(f"## Twitter Thread\n{package['social_media']['twitter_thread']}\n\n## LinkedIn Post\n{package['social_media']['linkedin_post']}")
        
        # Save YouTube
        with open(f"{output_dir}/youtube.md", "w", encoding="utf-8") as f:
            f.write(f"## Script\n{package['youtube']['script']}\n\n## Description\n{package['youtube']['description']}")
        
        print("--- Success! ---")
        print(f"The high-value content package has been saved to the '{output_dir}' directory.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
