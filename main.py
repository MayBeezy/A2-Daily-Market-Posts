import requests
from anthropic import Anthropic
from datetime import datetime
import json
import os
import random

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

# DIVERSE ANGLES - Mix of practical tips and compelling stories
ANGLES = [
    # BUYER TIPS & EDUCATION
    "First-time homebuyer mistakes to avoid - what I wish every buyer knew",
    "The importance of getting pre-approved before house hunting",
    "Home inspection red flags that could cost you thousands",
    "Negotiation tactics that actually work in today's Cedar Rapids market",
    "Understanding closing costs - what's normal, what's not",
    "Credit scores and home buying - what really matters to lenders",
    "Understanding ARM vs. fixed-rate mortgages - long-term implications",
    "What today's interest rates mean for your buying power",
    "Down payment options - more choices than you think",
    
    # SELLER TIPS & EDUCATION
    "How to price your home in today's market - the data tells the story",
    "Top 5 things that turn buyers away before they even enter",
    "The power of curb appeal - investing in what buyers see first",
    "Disclosure requirements - be honest, protect yourself",
    "When to accept an offer - waiting for perfect can cost you",
    "Preparing to sell - timeline and checklist",
    "What happens after the offer - the closing process explained",
    
    # STAGING & PRESENTATION
    "Staging on a budget - make your home shine without breaking the bank",
    "Decluttering secrets professionals use to sell homes faster",
    "Lighting, neutrals, and small touches that increase perceived value",
    
    # HOME MAINTENANCE & CARE
    "Home maintenance checklist - what every homeowner should do this season",
    "Foundation issues, roof age, and those expensive surprises",
    "Warranties explained - what they really cover",
    "Avoiding costly repairs - maintenance that pays for itself",
    
    # MARKET & TRENDS
    "Cedar Rapids market trends - spring is already here",
    "Buyer's market vs. seller's market - what changes and what doesn't",
    "Investment property strategies in Cedar Rapids' growing market",
    "Tax benefits of homeownership that surprise people every year",
    
    # COMMUNITY & LOCAL
    "Cedar Rapids hidden gems - neighborhoods buyers fall in love with",
    "Top schools, parks, and why location truly is everything",
    "New development in Cedar Rapids that's changing the real estate game",
    
    # SUCCESS STORIES - PROBLEM SOLVING
    "When credit seemed impossible - creative financing saved a family's dream",
    "Cleaning, repairs, and the extra mile that changes outcomes",
    "Title issues at the 11th hour - how persistence saved the day",
    
    # SUCCESS STORIES - LIFE'S TOUGH MOMENTS
    "Helping clients through divorce - real estate, emotions, and moving forward",
    "Settling an estate after a parent's passing - with compassion and clarity",
    "Family drama, legal hurdles, and saving deals that seemed impossible",
    
    # SUCCESS STORIES - RELATIONSHIPS & TRUST
    "Selling my clients' first home, helping them buy their dream, now their kids",
    "Three generations, one realtor - relationships that last 30 years",
    "The hard conversation about unanticipated costs - losing a deal, gaining respect",
    
    # SUCCESS STORIES - JOY & MOMENTS THAT MATTER
    "The client tears when signing - moments that remind me why I do this",
    "First home, emotional milestone, trusted guide through the biggest decision",
    
    # SUCCESS STORIES - RELOCATION & NEW STARTS
    "Relocating families to Cedar Rapids - tours, resources, and making it feel like home",
    "Connecting trailing spouses with jobs, schools, and community",
]

def generate_post(angle):
    try:
        client = Anthropic(api_key=API_KEY)
        prompt = f"""You are Amy Arrington, a Cedar Rapids realtor with 28 years of experience. You're warm, personal, relationship-focused, and genuinely care about your clients beyond the transaction.

Write a compelling Facebook post in Amy's authentic voice. The post should:
- Be personal and warm, not salesy
- Be 150-250 words
- Include 1-2 relevant emoji
- End with a soft, genuine call to action (invite them to chat, grab coffee, ask a question, etc.)
- Feel like Amy is sharing wisdom, a success story, or helpful advice from her heart

Topic/Angle: {angle}

Write ONLY the post text - no explanations or preamble."""
        
        msg = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.content[0].text
    except Exception as e:
        print(f"Error: {e}")
        return None

# Select 4 random UNIQUE angles
selected_angles = random.sample(ANGLES, 4)

print(f"\n{'='*70}")
print(f"Generating 4 posts for {datetime.now().strftime('%A, %B %d, %Y')}")
print(f"{'='*70}\n")

posts_list = []

for i, angle in enumerate(selected_angles, 1):
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
