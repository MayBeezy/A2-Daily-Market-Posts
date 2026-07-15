import requests
from anthropic import Anthropic
from datetime import datetime
import json
import os

# Read .env file
env_vars = {}
try:
    with open('.env', 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                env_vars[key] = value
except:
    pass

# Use environment variables
API_KEY = os.environ.get("ANTHROPIC_API_KEY") or env_vars.get("ANTHROPIC_API_KEY")

print(f"✓ API Key loaded: {bool(API_KEY)}")

def generate_post(angle):
    try:
        client = Anthropic(api_key=API_KEY)
        prompt = f"""You are Amy Arrington, a Cedar Rapids realtor with 28 years of experience.
Write a Facebook post in Amy's voice about real estate markets:
- Personal and warm
- 150-200 words
- Include emoji
- End with soft call to action

Focus: {angle}

Write ONLY the post text."""
        
        msg = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.content[0].text
    except Exception as e:
        print(f"Error: {e}")
        return None

angles = [
    "Freddie Mac rates and Cedar Rapids buyers",
    "Market inventory and opportunity",
    "Iowa affordability vs national trends",
    "Building trust in real estate"
]

print(f"\n{'='*70}")
print(f"Generating 4 posts for {datetime.now().strftime('%A, %B %d, %Y')}")
print(f"{'='*70}\n")

posts_list = []

for i, angle in enumerate(angles, 1):
    print(f"Post {i}: {angle}")
    post = generate_post(angle)
    if post:
        print(f"✓ Generated\n")
        posts_list.append({
            "post_number": i,
            "angle": angle,
            "text": post,
            "publish_time": ["9:00 AM", "11:00 AM", "3:00 PM", "4:30 PM"][i-1]
        })
    else:
        print(f"✗ Failed\n")

# Save to file
filename = f"posts_{datetime.now().strftime('%Y-%m-%d')}.json"
try:
    with open(filename, 'w') as f:
        json.dump(posts_list, f, indent=2)
    print(f"\n{'='*70}")
    print(f"✓ Saved to: {filename}")
    print(f"{'='*70}\n")
except Exception as e:
    print(f"Error saving file: {e}")

# Print for copying
print(f"COPY & PASTE TO FACEBOOK:\n")
for post in posts_list:
    print(f"\n--- POST {post['post_number']} ({post['publish_time']}) ---\n")
    print(post['text'])
    print(f"\n{'='*70}")

print("\n✓ Done!")
