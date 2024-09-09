from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from .models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, Your account was created")
            
            # Authenticate and log the user in
            new_user = authenticate(username=form.cleaned_data.get("email"),
                                    password=form.cleaned_data.get("password1"))
            if new_user is not None:
                login(request, new_user)
                return redirect("core:index")
        else:
            print(form.errors)  # Print the form errors to help debug
            return render(request, "userauths/sign-up.html", {"form": form})
    else:
        form = UserRegisterForm()
    
    context = {
        'form': form,
    }
    return render(request, "userauths/sign-up.html", context=context)


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "Hey, you are already logged in!")
        return redirect("core:index")
    
    if request.method == "POST":
        username_or_email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username_or_email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username}")
            return redirect("core:index")
        else:
            messages.warning(request, "Invalid credentials. Please try again.")
    
    return render(request, "userauths/sign-in.html")
    
    
def logout_user(request):
    messages.success(request, "You just Logged out")
    logout(request)
    return redirect("core:index")