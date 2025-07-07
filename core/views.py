from django.shortcuts import render
from .forms import RegisterForm, LoginForm, FileUploadForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
import whisper
import numpy
from .models import InterviewResponse
from .openai_helper import generate_follow_up_question, generate_final_feedback
# Create your views here.
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Create user instance but don't save to DB yet
            user.set_password(form.cleaned_data['password'])  # Hash the password properly # Hash the password
            user.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Invalid registration details. Please try again.")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Authenticate user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Log the user in
                login(request, user)
                return redirect('chatbot_interview')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def chatbot_interview(request):
    if 'question_count' not in request.session:
        request.session['question_count'] = 0
        request.session['transcript_history'] = []
        request.session['interview_type'] = None

    count = request.session['question_count']
    history = request.session['transcript_history']
    interview_type = request.session['interview_type']

    chat_log = []

    if request.method == "POST":
        if 'question_type' in request.POST:
            interview_type = request.POST['question_type']
            request.session['interview_type'] = interview_type
        elif 'end_interview' in request.POST:
            final_feedback = generate_final_feedback(history, interview_type)
            request.session.flush()
            return render(request, 'chat.html', {'chat_log':history, 'final_feedback':final_feedback})
        else:
            form = FileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                audio_file = form.cleaned_data['audio_file']
                response = InterviewResponse(user=request.user, audio_file=audio_file)
                response.save()

                model = whisper.load_model("base")
                result = model.transcribe(response.audio_file.path)
                transcript = result['text']

                response.transcript = transcript
                response.save()

                history.append(f"User: {transcript}")

                count+=1
                request.session['question_count'] = count
                request.session['transcript_history'] = history

                if count>=5:
                    chat_log = history
                    chat_log.append("You've completed 5 questions. End interview to get feedback or continue answering.")
                    return render(request, 'chat.html', {
                        'chat_log': chat_log,
                        'form': FileUploadForm(),
                        'show_question': False
                    })
    if interview_type and count < 5:
        question = generate_follow_up_question(history, interview_type)
        history.append(f"AI: {question}")
        request.session['transcript_history'] = history
    
    return render(request, 'chat.html', {
        'chat_log': history,
        'form': FileUploadForm(),
        'show_question': True,
        'interview_type': interview_type
    })


