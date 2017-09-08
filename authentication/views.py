#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 09:10
# Last modified: 2017-09-08 17:18
# Filename: views.py
# Description:
import json

from django.views.generic import CreateView, DetailView, View
from django.views.generic import UpdateView, RedirectView, TemplateView
from django.contrib.auth.views import LoginView as _LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
from django.utils.http import is_safe_url
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.urls import NoReverseMatch

from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

from . import USER_IDENTITY_STUDENT, USER_IDENTITY_SOCIAL, USER_IDENTITY_UNSET
from .forms import StudentRegisterForm, SocialRegisterForm, LoginForm
from .models import SocialInfo, StudentInfo
from .utils import get_detail_info_or_404


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'authentication/index.html'


class CaptchaRefresh(View):
    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        response = {}
        response['key'] = CaptchaStore.generate_key()
        response['img'] = captcha_image_url(response['key'])
        return HttpResponse(json.dumps(response),
                            content_type='application/json')


class LoginView(_LoginView):
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True
    form_class = LoginForm

    def get_success_url(self):
        """Ensure the user-originating redirection URL is safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        user = self.request.user
        if not url_is_safe:
            if user.is_authenticated():
                return reverse('index')
            else:
                return reverse('login')
        return redirect_to


class RegisterView(CreateView):
    template_name = 'authentication/register.html'
    form_class = StudentRegisterForm
    success_url = reverse_lazy('index')
    identity = USER_IDENTITY_STUDENT
    form_post_url = reverse_lazy('student_register')
    back_url = 'login'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        first_name = form.cleaned_data['name']
        password = form.cleaned_data['password']
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name)
        form.instance.user = user
        form.instance.identity = self.identity
        login(self.request, user,
              backend='django.contrib.auth.backends.ModelBackend')
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return super(RegisterView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['form_post_url'] = self.form_post_url
        kwargs['back_url'] = self.back_url
        kwargs['identity'] = self.identity
        return super(RegisterView, self).get_context_data(**kwargs)

    def form_invalid(self, form):
        self.template_name = RegisterView.template_name
        return super(RegisterView, self).form_invalid(form)


class AuthFormLoadView(RedirectView):
    def get(self, request, *args, **kwargs):
        register_type = request.GET.get('form_type', None)
        if register_type is None:
            raise Http404()
        try:
            self.url = reverse(register_type)
        except NoReverseMatch:
            raise Http404()
        return super(AuthFormLoadView, self).get(request, *args, **kwargs)


class StudentRegisterView(RegisterView):
    form_class = StudentRegisterForm
    identity = USER_IDENTITY_STUDENT
    template_name = 'authentication/info_form.html'
    form_post_url = reverse_lazy('student_register')


class SocialRegisterView(RegisterView):
    form_class = SocialRegisterForm
    identity = USER_IDENTITY_SOCIAL
    template_name = 'authentication/info_form.html'
    form_post_url = reverse_lazy('social_register')


class InfoMixin(object):
    fields_dict = {
        USER_IDENTITY_SOCIAL: ['citizen_id', 'title', 'education',
                               'political_status'],
        USER_IDENTITY_STUDENT: ['student_id', 'institute'],
    }
    models_dict = {
        USER_IDENTITY_SOCIAL: SocialInfo,
        USER_IDENTITY_STUDENT: StudentInfo,
    }
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def set_related_context(self, request):
        user_info = request.user.user_info
        info = get_detail_info_or_404(user_info)
        self.fields = self.fields_dict[user_info.identity]
        self.object = info
        self.kwargs['uid'] = info.uid
        self.model = self.models_dict[user_info.identity]

    def post(self, request, *args, **kwargs):
        self.set_related_context(request)
        return super(InfoMixin, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.set_related_context(request)
        return super(InfoMixin, self).get(request, *args, **kwargs)


class StudentDetailInfoView(InfoMixin, LoginRequiredMixin, DetailView):
    template_name = 'authentication/student_info_detail.html'
    http_method_names = ['get']

    def get_context_data(self, **kwargs):
        kwargs['title'] = '个人信息'
        return super(StudentDetailInfoView, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        self.set_related_context(request)
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class SocialDetailInfoView(StudentDetailInfoView):
    template_name = 'authentication/social_info_detail.html'


class DetailInfoRedirectView(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        user_info = request.user.user_info
        if user_info.identity == USER_IDENTITY_STUDENT:
            view = 'student_detail_info'
        elif user_info.identity == USER_IDENTITY_SOCIAL:
            view = 'social_detail_info'
        else:
            raise Http404()
        self.url = reverse(view)
        return super(DetailInfoRedirectView, self).get(request,
                                                       *args, **kwargs)


class DetailInfoUpdateView(InfoMixin, LoginRequiredMixin, UpdateView):
    template_name = 'authentication/detail_update.html'
    success_url = reverse_lazy('detail_info')
    back_url = 'detail_info'

    def get_context_data(self, **kwargs):
        kwargs['title'] = '个人信息修改'
        kwargs['back_url'] = self.back_url
        return super(DetailInfoUpdateView, self).get_context_data(**kwargs)

    # TODO: Detail update auth check
