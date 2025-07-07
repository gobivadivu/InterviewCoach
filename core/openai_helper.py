import openai
import os
from openai import OpenAI

api_key=os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def generate_follow_up_question(transcript_history, interview_type="technical"):
    messages = [
        {"role":"system",
         "content": f"You are an AI interviewer conducting a {interview_type} interview. Ask one follow-up question based on candidate's answers."}
    ]
    for t in transcript_history:
        messages.append({"role":"user", "content":t})
    messages.append({"role": "assistant", "content": "Ask the next question."})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages
    )

    return response.choices[0].message.content.strip()

def generate_final_feedback(transcript_history, interview_type="technical"):
    messages = [
        {"role": "system", "content": f"You are a senior {interview_type} interviewer. Provide overall feedback to the candidate."},
        {"role": "user", "content": "\n\n".join(transcript_history)}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages
    )

    return response.choices[0].message.content.strip()
