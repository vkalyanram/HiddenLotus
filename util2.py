import openai
import speech_recognition as sr
from gtts import gTTS
from datetime import datetime
import os
import json
import pydub
import random
import sqlite3
# Set your OpenAI API Key
openai.api_key = "YOUR_KEY"
def detect_language(text):
    """
    Detect the language and return a proper language code (e.g., "en" for English, "hi" for Hindi).
    """
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system",
             "content": "You are a language detector. Return only the language code (e.g., 'en', 'hi')."},
            {"role": "user", "content": f"Detect the language of this text and return the language code only: {text}"}
        ]
    )

    detected_language = response.choices[0].message.content.strip().lower()

    # Ensure it's a valid language code for gTTS
    supported_languages = {"english": "en", "hindi": "hi"}  # Add more if needed
    return supported_languages.get(detected_language, "en")  # Default to English if not found
def text_to_speech(text):
    """
    Convert text to speech by detecting the language dynamically.
    """
    lang = detect_language(text)
    tts = gTTS(text=text, lang=lang, slow=False)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"speech_{timestamp}.mp3"
    tts.save(output_file)
    print(f"Saved audio: {output_file}")
    return output_file
def translate_text(text, target_language=None):
    """
    Translate text to another language. If no target language is provided, it defaults to English.
    """
    source_language = detect_language(text)
    target_language = "en" if target_language is None else target_language

    if source_language == target_language:
        return text  # No translation needed

    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a translator."},
            {"role": "user", "content": f"Translate this from {source_language} to {target_language}: {text}"}
        ]
    )
    translated_text = response.choices[0].message.content.strip()
    return translated_text
def detect_language1(text):
    """
    Detect the language of the given text and return a language code ('en' or 'hi').
    """
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system",
             "content": "You are a language detector. Return only 'en' for English or 'hi' for Hindi."},
            {"role": "user", "content": f"Detect the language of this text and return only 'en' or 'hi': {text}"}
        ]
    )

    detected_language = response.choices[0].message.content.strip().lower()
    return detected_language if detected_language in ["en", "hi"] else "en"  # Default to English
def translate_text1(text, target_language="en"):
    """
    Translate text to the target language (default: English).
    """
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a translator."},
            {"role": "user", "content": f"Translate this to {target_language}: {text}"}
        ]
    )
    return response.choices[0].message.content.strip()
def speech_to_text(audio_file):
    """
    Convert speech from an audio file (MP3) to text with auto language detection.
    """
    recognizer = sr.Recognizer()

    # Convert MP3 to WAV (since SpeechRecognition needs WAV format)
    audio = pydub.AudioSegment.from_mp3(audio_file)
    wav_file = audio_file.replace(".mp3", ".wav")
    audio.export(wav_file, format="wav")

    with sr.AudioFile(wav_file) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)  # Let Google auto-detect language
        detected_lang = detect_language1(text)

        print(f"Recognized Text: {text} (Detected Language: {detected_lang})")

        # If detected as Hindi, translate it to English
        if detected_lang == "hi":
            translated_text = translate_text1(text, "en")
            print(f"Translated to English: {translated_text}")
            return translated_text
        else:
            return text  # If already English, return as is

    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return None
    except sr.RequestError:
        print("Could not request results.")
        return None
def get_one_user_without_interaction():
    """Fetch one user who hasn't had any interaction."""
    conn = sqlite3.connect('agent.db')
    cursor = conn.cursor()

    query = """
    SELECT id, name, contact_number, product_id
    FROM users 
    WHERE last_interaction IS NULL
    """
    cursor.execute(query)

    users = cursor.fetchall()  # List of (id, name, contact_number, product_id, preferred_language)
    conn.close()

    if not users:
        return None  # No users found

    selected_user = random.choice(users)  # Randomly pick one user
    return selected_user  # Returns (id, name, contact_number, product_id, preferred_language)

def get_ai_response(prompt):
    """Generate AI response using OpenAI's latest API."""
    client = openai.Client(api_key=openai.api_key )  # Pass API key explicitly
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content  # Extract AI response
from twilio.rest import Client
#Replace your keys
account_sid = "SID"
auth_token = "TOKEN"
client = Client(account_sid, auth_token)

def make_call(message,contact_number="+910000000000"):
    """Call user using Twilio and deliver message."""
    call = client.calls.create(
        twiml=f'<Response><Say>{message}</Say></Response>',
        to=contact_number,
        from_="0000000000"
    )
    return call.sid
def save_conversation(user_id, conversation_log):
    """Save conversation log to a JSON file."""
    filename = f"conversation_logs/{user_id}.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)  # Ensure directory exists
    with open(filename, "w") as f:
        json.dump(conversation_log, f, indent=4)

def update_user_status(user_id):
    """Mark user as contacted and update last interaction date in database."""
    today_date = datetime.today().strftime('%Y-%m-%d')  # Format: YYYY-MM-DD

    conn = sqlite3.connect("agent.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET last_interaction = ? WHERE user_id = ?", (today_date, user_id))
    conn.commit()
    conn.close()
