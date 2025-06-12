from django.shortcuts import render
from .forms import RegisterForm, LoginForm, FileUploadForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
import whisper
from .models import InterviewResponse

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
                print("Logging in user:", user.username)  # Debugging line
                login(request, user)
                return render(request, 'login_success.html', {'user': user})
            else:
                print("Hello")
                messages.error(request, "Invalid username or password.")
    else:
        print("HHH")
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def audio_input(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = form.cleaned_data['audio_file']
            qresponse = InterviewResponse(user=request.user, audio_file=audio_file)
            qresponse.save()

            model = whisper.load_model("base")  # Use "base" or "small" for deployable testing
            file_path = qresponse.audio_file.path  # Get the actual file path
            result = model.transcribe(file_path)

            model = whisper.load_model("base")
            result = model.transcribe(file_path)
            qresponse.transcript = result['text']
            qresponse.save()
            
            messages.success(request, "Audio file uploaded successfully.")
            return render(request, 'audio_success.html', {'transcript': result['text']})
    else:
        form = FileUploadForm()
    return render(request, 'audio_upload.html', {'form': form})
