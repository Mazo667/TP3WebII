from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Cuenta creada para {username}!")
            return redirect("post:post_list")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenido, {username}!")
                return redirect("post:post_list") 
            else:
                messages.error(request, "Usuario invalido o contraseña invalida.")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {'form': form})

# Custom Logout View
class CustomLogoutView(LogoutView):
    next_page = 'accounts:login'

# Password Change View
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'password_change.html'
    success_url = reverse_lazy('accounts:password_change_done')

# Password Change Done View
class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'

# Password Reset View
class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    from_email = 'mafava@udc.edu.ar'

# Password Reset Done View
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'