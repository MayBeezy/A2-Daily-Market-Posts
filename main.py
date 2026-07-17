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
    # BUYER TIPS
    "First-time homebuyer mistakes to avoid - what I wish every buyer knew",
    "The importance of getting pre-approved before house hunting",
    "Home inspection red flags that could cost you thousands",
    "Negotiation tactics that actually work in today's Cedar Rapids market",
    "Understanding closing costs - what's normal, what's not",
    
    # SELLER TIPS
    "How to price your home in today's market - the data tells the story",
    "Top 5 things that turn buyers away before they even enter",
    "The power of curb appeal - investing in what buyers see first",
    "Disclosure requirements - be honest, protect yourself",
    "When to accept an offer - waiting for perfect can cost you",
    
    # STAGING & PRESENTATION
    "Staging on a budget - make your home sing without breaking the bank",
    "Decluttering secrets professionals use to sell homes faster",
    "Lighting, neutrals, and small touches that increase perceived value",
    
    # FINANCING & MONEY
    "Credit scores and home buying - what really matters to lenders",
    "Investment property strategies in Cedar Rapids' growing market",
    "Understanding ARM vs. fixed-rate mortgages - long-term implications",
    "Tax benefits of homeownership that surprise people every year",
    
    # COMMUNITY & LOCAL
    "Cedar Rapids hidden gems - neighborhoods buyers fall in love with",
    "Top schools, parks, and why location truly is everything",
    "New development in Cedar Rapids that's changing the real estate game",
    
    # MAINTENANCE & HOME CARE
    "Home maintenance checklist - what every homeowner should do this season",
    "Foundation issues, roof age, and those expensive surprises",
    "Warranties explained - what they really cover",
    
    # SUCCESS STORIES - CREATIVE SOLUTIONS
    "When credit seemed impossible - the loan officer who believed in my clients",
    "Bad credit, good heart - how creative financing saved a family's dream",
    "The power of connecting with the right lender at the right time",
    
    # SUCCESS STORIES - GOING ABOVE AND BEYOND
    "I painted with my sellers to get their home market-ready - and they got full asking price",
    "Cleaning, repairs, and the extra mile that changes outcomes",
    "When a realtor becomes part of your family",
    
    # SUCCESS STORIES - NAVIGATING LIFE'S HARDEST MOMENTS
    "Helping clients through divorce - real estate, emotions, and moving forward",
    "Settling an estate after a parent's passing - with compassion and clarity",
    "Family drama, legal hurdles, and saving deals that seemed impossible",
    
    # SUCCESS STORIES - MULTI-GENERATIONAL CLIENTS
    "Selling my clients' first home, helping them buy their dream, and now their kids too",
    "Three generations, one realtor - the relationships that last 30 years",
    
    # SUCCESS STORIES - 11TH HOUR MIRACLES
    "Title issues at the 11th hour - how persistence and connections saved the day",
    "Liens, problems, and one tough client who refused to give up",
    "When everything falls apart 3 days before closing - and we fixed it",
    
    # SUCCESS STORIES - EMOTIONAL WINS
    "The client tears when signing the purchase agreement - moments that remind me why I do this",
    "First home, emotional milestone, trusted guide through the biggest decision",
    
    # SUCCESS STORIES - HONESTY & INTEGRITY
    "When I had to tell clients the deal wouldn't work - and why they thanked me for honesty",
    "The hard conversation about unanticipated costs - losing a deal, gaining a client's respect",
    "Transparency over commission - why integrity matters in Cedar Rapids",
    
    # SUCCESS STORIES - RELOCATING & NEW STARTS
    "Relocating families who chose Cedar Rapids - tours, resources, and making it feel like home",
    "Connecting trailing spouses with jobs, schools, and community",
    "The joy of helping families settle into their new city",
    
    # MARKET & TRENDS
    "What today's interest rates mean for your buying power",
    "Cedar Rapids market trends - spring is already here",
    "Buyer's market vs. seller's market - what changes and what doesn't",
    
    # SEASONAL ADVICE
    "Spring selling season - timing your move for maximum impact",
    "Summer buying - benefits, competition, and strategy",
    "Fall market secrets that buyers don't always know",
    "Winter deals - the surprising advantages of off-season buying",
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
