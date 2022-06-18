from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import get_user_model
from .forms import RegisterUser
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail

user = get_user_model()


def registeruserviaemail(request):
    if request.method == 'POST':
        form = RegisterUser(request.POST)
        if form.is_valid():
            try:
                if user.objects.filter(email=request.POST['email']).first():
                    messages.success(request, 'The email id is already present')
                    return redirect('registeruser')

                new_user = user.objects.create(email=form.cleaned_data['email'],
                                               first_name=form.cleaned_data['first_name'],
                                               last_name=form.cleaned_data['last_name'])
                password = form.cleaned_data['password1']
                new_user.set_password(password)

                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                uid64 = urlsafe_base64_encode(force_bytes(new_user.pk))
                print(uid64)
                print(new_user.pk)
                new_user.otp = default_token_generator.make_token(new_user)
                message = render_to_string('activate_email.html', {
                    'user': new_user,
                    'domain': current_site.domain,
                    'uid': uid64,
                    'token': default_token_generator.make_token(new_user),
                })
                to_email = form.cleaned_data.get('email')
                send_mail(mail_subject, message, None, [to_email], fail_silently=False)
                messages.add_message(request, messages.SUCCESS, 'Profile created but  verification is required')


                # return HttpResponse('Please confirm your email address to complete the registration')
            except Exception as e:
                print(e)
        else:
            return render(request,'register_user.html',{'form': form})
    form = RegisterUser()
    return render(request, 'register_user.html', {'form': form})


def activate(request, uidb64, token):
    global user
    try:
        print(uidb64)
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        print(int(uid))

        nuser = user.objects.get(id=int(uid))
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        nuser = None
    print(nuser)
    print(token)
    print(default_token_generator.check_token(nuser, token))
    if nuser is not None and (nuser.otp == token):
        nuser.is_active = True
        nuser.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
