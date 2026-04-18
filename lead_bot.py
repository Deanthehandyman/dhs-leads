import os
from twikit import Client
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Tailored queries for YOUR services + area (Starlink + WiFi mesh + cameras + RV/off-grid)
QUERY = '("Starlink" OR "star link") (install OR installer OR mount OR setup OR mesh OR "WiFi" OR "security camera" OR "smart home" OR "smart lock") ("need" OR recommend OR "who can" OR "looking for" OR help OR frustration OR issue) ("Pittsburg" OR "Sulphur Springs" OR Texarkana OR "East Texas" OR "Ark-La-Tex" OR "North Texas" OR "RV park" OR ranch OR farm OR "off grid")'

client = Client('en-US')

async def main():
    # Login (twikit handles session securely)
    await client.login(
        auth_info_1=os.getenv('TWITTER_USERNAME'),
        auth_info_2=os.getenv('TWITTER_PASSWORD'),
        password=os.getenv('TWITTER_PASSWORD')
    )
    
    tweets = await client.search_tweet(QUERY, product='Latest', count=20)
    
    leads = []
    for tweet in tweets:
        text_lower = tweet.full_text.lower()
        # Extra filter to catch only high-intent + your tech niches
        if any(word in text_lower for word in ['install', 'mount', 'setup', 'mesh', 'camera', 'rv', 'off-grid', 'security']):
            lead = f"🚨 NEW LEAD for Dean's Handyman:\n\nUser: {tweet.user.name} (@{tweet.user.screen_name})\nPost: {tweet.full_text}\nLink: https://x.com/{tweet.user.screen_name}/status/{tweet.id}\nTime: {tweet.created_at}\n---\n"
            leads.append(lead)
    
    if leads:
        body = f"🔥 Dean's Handyman Lead Bot Report — {datetime.now().strftime('%Y-%m-%d %H:%M CDT')}\n\nFound {len(leads)} fresh Starlink / smart home / WiFi / camera jobs in your East Texas radius:\n\n" + "\n".join(leads)
        body += "\n\nReply fast from @DeansHandymanTX or 281-917-9914 — mention your cash discount + free 100-mile travel!"
        
        msg = MIMEText(body)
        msg['Subject'] = f"🚀 {len(leads)} New Tech Leads — Starlink/Smart Home (Deanshandymanservice1@gmail.com)"
        msg['From'] = os.getenv('EMAIL_USER')
        msg['To'] = "Deanshandymanservice1@gmail.com"  # Your exact email pre-filled
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
            server.sendmail(os.getenv('EMAIL_USER'), "Deanshandymanservice1@gmail.com", msg.as_string())
        print("✅ Email sent to Deanshandymanservice1@gmail.com with leads!")
    else:
        print("No new leads this cycle — bot will check again in 6 hours.")

import asyncio
asyncio.run(main())
