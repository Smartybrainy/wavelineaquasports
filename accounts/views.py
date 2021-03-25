from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.views import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage

import json
import threading

from .models import CustomUser
from .forms import (
    CustomSignupForm,
    PhoneVerificationForm,
    CustomLoginForm,
    PhoneVerificationForm
)
from .authy import send_verification_code, verify_sent_code
from .tokens import account_activation_token


class EmailThread(threading.Thread):
    def __init__(self, send_email):
        self.send_email = send_email
        threading.Thread.__init__(self)

    def run(self):
        return self.send_email.send(fail_silently=True)


class CustomSignupView(SuccessMessageMixin, FormView):
    template_name = 'accounts/signup.html'
    form_class = CustomSignupForm
    success_message = "One-Time password sent to your registered mobile number.\
                       The verification code is valid for 5 minutes."

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.info(
                self.request, f"{self.request.user} you are logged in")
            return redirect('/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            if user is not None:
                # for email confirmation
                raw_email = form.cleaned_data.get('email')
                domain = get_current_site(self.request).domain
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = account_activation_token.make_token(user)
                link = reverse('accounts:activate', kwargs={
                    'uidb64': uidb64, 'token': token})
                activate_url = domain+link

                email_subject = 'Activate Your Wavelineaquasports Account.'
                email_body = f'Hi {user} Please use this link to activate your account,\n If you are unable to click the link copy it to a new browser tab.\n\n{activate_url}'
                send_email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@wavelineaquasports.com',
                    [raw_email],
                )
                EmailThread(send_email).start()
                messages.info(
                    self.request, "An email has been sent to your mailbox click on the link to complete your account registration.")
                return redirect('/')
            else:
                pass
        else:
            pass

    # phone_number = self.request.POST.get('phone_number')
    # password = self.request.POST.get('password1')
    # authenticate(phone_number=phone_number, password=password)
    # try:
    #     response = send_verification_code(user)
    #     messages.add_message(
    #         self.request, messages.INFO, self.success_message)
    # except Exception as e:
    #     messages.add_message(self.request, messages.WARNING,
    #                          'verification code not sent. \n'
    #                          'Please re-register.')
    #     user.delete()  # make sure user not saved
    #     return redirect('accounts:signup')
    # data = json.loads(response.text)

    # print(response.status_code, response.reason)
    # print(response.text)
    # print(data['success'])

    # if data.get('success') == False:
    #     messages.add_message(self.request, messages.WARNING,
    #                          data.get('message'))
    #     return redirect('accounts:signup')
    # else:
    #     kwargs = {'user': user}
    #     return phone_verification_view(self.request, **kwargs)


class CustomLoginView(SuccessMessageMixin, FormView):
    template_name = 'accounts/login.html'
    form_class = CustomLoginForm
    success_url = '/'
    success_message = "One-Time password sent to your registered mobile number.\
                       The verification code is valid for 5 minutes."

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.info(
                self.request, f"{self.request.user} you are logged in")
            return redirect('/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            user = form.login(self.request)
            if user is not None:
                login(self.request, user)
            return redirect('/')

        # if user.two_factor_auth is False:
        #     login(self.request, user)
        #     return redirect('/')
        # else:
        #     try:
        #         response = send_verification_code(user)
        #         messages.add_message(
        #             self.request, messages.INFO, self.success_message)
        #     except Exception as e:
        #         messages.warning(
        #             self.request, "Verifacation code not sent. \n Please retry logging in")
        #         return redirect('accounts:login')
        #     data = json.loads(response.text)

        #     if data.get('success') == False:
        #         messages.info(
        #             self.request, data.get('message'))
        #         return redirect('accounts:login')

        #     print(response.status_code, response.reason)
        #     print(response.text)

        #     if data.get('success') == True:
        #         kwargs = {'user': user}
        #         return phone_verification_view(self.request, **kwargs)
        #     else:
        #         messages.add_message(self.request, messages.WARNING,
        #                              data.get('message'))
        #         return redirect('accounts:login')


# def phone_verification_view(request, **kwargs):
#     template_name = 'accounts/phone_confirm.html'

#     if request.user.is_authenticated:
#         messages.info(
#             request, f"{request.user} you are logged in")
#         return redirect('/')

#     if request.method == "POST":
#         phone_number = request.POST.get('phone_number')
#         user = CustomUser.objects.get(phone_number=phone_number)

#         form = PhoneVerificationForm(request.POST or None)
#         if form.is_valid():
#             verification_code = form.cleaned_data.get('one_time_password')
#             response = verify_sent_code(verification_code, user)

#             print(response.text)
#             data = json.loads(response.text)
#             if data.get('success') == True:
#                 if user.is_active == False:
#                     user.is_active = True
#                     user.save()

#                 login(request, user)

#                 if user.phone_number_verified is False:
#                     user.phone_number_verified = True
#                     user.save()
#                     return redirect('/')
#             else:
#                 messages.add_message(request, messages.WARNING,
#                                      data.get('message'))
#                 return render(request, template_name, {'user': user})
#         else:
#             context = {
#                 'user': user,
#                 'form': form,
#             }
#             return render(request, template_name, context)

#     elif request.method == "GET":
#         try:
#             user = kwargs.get('user')
#             if user:
#                 return render(request, template_name, {'user': user})
#             return HttpResponse("<h4>Not Allowed!</h4>")
#         except:
#             return HttpResponse("<h4>Not Allowed!</h4>")


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (ValueError, TypeError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(
            request, f"{user} your email verification was successful")
        return redirect('/')
    else:
        user.delete()  # make sure user is not saved
        messages.success(
            request, f"{user} your email verification was cancelled, please retry.")
    return redirect('/')
