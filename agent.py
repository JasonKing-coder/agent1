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

def generate_blog_post(transcript_text):
    print("--- Generating High-Conversion Blog Post ---")
    system_prompt = (
        "You are a world-class content marketer and SEO expert. "
        "Your goal is to turn a raw transcript into a high-converting, "
        "authoritative blog post that establishes the speaker as a leader. "
        "Use emotional hooks, clear headings, and a strong call to action (CTA)."
    )
    user_prompt = f"""
    Analyze the following transcript and write a comprehensive, SEO-optimized blog post.
    
    TRANSCRIPT:
    {transcript_text}

    REQUIREMENTS:
    1. Catchy, click-worthy title.
    2. Engaging introduction with a strong hook.
    3. Use H2 and H3 tags for readability.
    4. Include a 'Key Takeaways' section.
    5. End with a powerful Call to Action.
    6. Write in a professional yet accessible tone.
    7. Format in Markdown.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content

def generate_marketing_package(blog_post_content):
    print("--- Generating Multi-Channel Marketing Package ---")
    system_prompt = (
        "You are a social media strategist and newsletter expert. "
        "Your goal is to repurpose a high-quality blog post into "
        "multiple high-engagement formats for different platforms."
    )
    
    user_prompt = f"""
    Based on the following blog post, create a complete marketing package.
    
    BLOG POST:
    {blog_post_content}

    REQUIRED OUTPUT FORMAT (JSON):
    {{
        "newsletter": {{
            "subject_line": "High-open-rate subject line",
            "body": "A punchy, engaging newsletter summary with a CTA."
        }},
        "social_media": {{
            "twitter_thread": "A 5-tweet thread with hooks and emojis.",
            "linkedin_post": "A professional thought-leadership post.",
            "instagram_reels_script": "A 60-second script for a Reel/TikTok with visual cues."
        }},
        "youtube": {{
            "script": "A structured video script (Intro, Body, Outro).",
            "description": "SEO-optimized description with timestamps and keywords."
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
    extensions = ('.mp3', '.mp4', '.wav', '.m4a', '.mov')
    files = [f for f in os.listdir('.') if f.lower().endswith(extensions)]

    if not files:
        print("No audio or video files found in the root directory.")
        return

    target_file = files[0]
    
    try:
        # Step 1: Transcribe
        transcript = transcribe_file(target_file)
        print(f"Transcription complete. Length: {len(transcript)} characters.")
        
        # Step 2: Generate Blog Post (High Quality)
        blog_post = generate_blog_post(transcript)
        
        # Step 3: Generate Marketing Package from Blog Post
        package = generate_marketing_package(blog_post)
        
        # Create output directory
        output_dir = "content_package"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save Blog Post
        with open(f"{output_dir}/blog_post.md", "w", encoding="utf-8") as f:
            f.write(blog_post)
        
        # Save Newsletter
        with open(f"{output_dir}/newsletter.md", "w", encoding="utf-8") as f:
            f.write(f"Subject: {package['newsletter']['subject_line']}\n\n{package['newsletter']['body']}")
        
        # Save Social Media
        with open(f"{output_dir}/social_media.md", "w", encoding="utf-8") as f:
            f.write(f"## Twitter Thread\n{package['social_media']['twitter_thread']}\n\n## LinkedIn Post\n{package['social_media']['linkedin_post']}\n\n## Instagram/TikTok Script\n{package['social_media']['instagram_reels_script']}")
        
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
