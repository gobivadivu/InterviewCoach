from transformers import pipeline

#generate = pipeline("text-generation", model="tiiuae/falcon-7b-instruct", trust_remote_code=True, device=0)
generate = pipeline("text2text-generation", model="google/flan-t5-base")


def format_prompt(messages):
    prompt = ""
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        if role=="system":
            prompt += f"[System Instruction]: {content}\n"
        elif role=="user":
            prompt += f"[User]: {content}\n"
        elif role=="assistant":
            prompt += f"[Assistant]: {content}\n"
    return prompt

def generate_follow_up_question(transcript_history, interview_type="technical"):
    messages = [
        {"role":"system",
         "content": f"You are an AI interviewer conducting a {interview_type} interview for hiring the candidate for your comapny for the role of sde. Ask one follow-up question based on candidate's answers."}
    ]
    for t in transcript_history:
        messages.append({"role":"user", "content":t})
    messages.append({"role": "assistant", "content": "Ask the next question."})

    prompt = format_prompt(messages)
    response = generate(prompt, max_new_tokens=100, do_sample=True, temperature=0.7)[0]['generated_text']
    
    last_line = response.strip().split("\n")[-1]
    return last_line.strip()

def generate_final_feedback(transcript_history, interview_type="technical"):
    prompt = f"You are a senior interviewer. Based on the following candidate responses from a {interview_type} interview, provide detailed final feedback:\n\n"
    prompt += "\n".join(transcript_history)

    response = generate(prompt, max_new_tokens=200, do_sample=True, temperature=0.7)[0]['generated_text']

    return response.strip()
