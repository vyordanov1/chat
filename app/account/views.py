from datetime import timezone, datetime
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, DeleteView, CreateView, UpdateView, TemplateView, ListView, DetailView
from .forms import *
from .models import *
from chat.models import ChatRoom, UserChatRoom
from chat.forms import CreateChatRoomForm
from chat.forms import DeleteChatRoomForm
from app.mixins import RequireLoginMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from chat.models import OffensiveWords, AbuseReport

"""
 importing the user_passes_tests decorator to use with 'admin'
 pages, so that they are not accessible to ordinary users
"""
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator


def is_admin(user):
    if not user.is_authenticated:
        return False
    return user.admins.is_admin


@method_decorator(user_passes_test(is_admin), name='dispatch')
class BlockAbusingUserView(LoginRequiredMixin, FormView):
    form_class = BlockAbusingUserForm
    success_url = reverse_lazy('abuse_reports')
    login_url = reverse_lazy('login')
    template_name = 'account/admin/block_user.html'
    pk_url_kwarg = 'report_id'

    def form_valid(self, form):
        """
        Overwriting the form_valid as the form does not relate to a model due to passing report_id in kwargs
        """
        blocked_until = form.cleaned_data['blocked_until']
        report = get_object_or_404(AbuseReport, pk=self.kwargs['report_id'])
        profile = report.message.sender.profile if report else None
        if report and profile:
            report.processed = True
            report.processed_date = datetime.datetime.now(tz=datetime.timezone.utc)

            profile.blocked_until = blocked_until
            profile.blocked = True

            profile.save()
            report.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        payload = super().get_context_data(**kwargs)
        payload.update(
            {
                "page_data": {
                    "header": "Block User",
                    "leave_btn": {
                        "url": "account",
                        "name": "Return"
                    }
                },
                "profile": self.request.user.profile
            }
        )
        return payload


@method_decorator(user_passes_test(is_admin), name='dispatch')
class AbuseReportsView(LoginRequiredMixin, FormView):
    form_class = SearchForm
    template_name = 'account/admin/abuse_reports.html'
    model = AbuseReport
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        query = form.cleaned_data['query']
        if query:
            self.reports = AbuseReport.objects.filter(message__sender__username__icontains=query).order_by(
                'processed',
                '-report_date'
            )
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        payload = super().get_context_data(**kwargs)
        reports = getattr(self, 'reports', AbuseReport.objects.all().order_by('processed','-report_date'))

        payload.update(
            {
                "page_data": {
                    "header": "Abuse Reports",
                    "leave_btn": {
                        "url": "account",
                        "name": "Return"
                    }
                },
                "object_list": reports
            }
        )
        return payload


@method_decorator(user_passes_test(is_admin), name='dispatch')
class AbuseReportDetailsView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    template_name = 'account/admin/abuse_report_details.html'
    model = AbuseReport
    pk_url_kwarg = 'report_id'

    def get_queryset(self):
        return AbuseReport.objects.get(pk=self.kwargs['report_id'])

    def get_context_data(self, **kwargs):
        payload = super().get_context_data(**kwargs)

        payload.update(
            {
                "page_data": {
                    "header": "Abuse Report Details",
                    "leave_btn": {
                        "url": "abuse_reports",
                        "name": "Return"
                    }
                }
            })

        return payload


@method_decorator(user_passes_test(is_admin), name='dispatch')
class AbuseReportDismissView(LoginRequiredMixin, UpdateView):
    model = AbuseReport
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('abuse_reports')
    pk_url_kwarg = 'report_id'
    form_class = DismissAbuseForm


@method_decorator(user_passes_test(is_admin), name='dispatch')
class OffensiveWordsView(LoginRequiredMixin, FormView):
    template_name = 'account/admin/offensive_words.html'
    form_class = SearchForm
    success_url = reverse_lazy('offensive_words')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        query = form.cleaned_data['query']
        if query:
            self.words = OffensiveWords.objects.filter(word__icontains=query)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        payload = super().get_context_data(**kwargs)
        offensive_words = getattr(self, 'words', OffensiveWords.objects.all())
        create_form = OffensiveWordCreateForm(self.request.POST or None)

        payload.update({
            "page_data": {
                "header": "Offensive Words",
                "leave_btn": {
                    "url": "account",
                    "name": "Return"
                }
            },
            "offensive_words": offensive_words,
            "create_form": create_form
        })
        return payload


@method_decorator(user_passes_test(is_admin), name='dispatch')
class OffensiveWordCreateView(LoginRequiredMixin, CreateView):
    model = OffensiveWords
    form_class = OffensiveWordCreateForm
    success_url = reverse_lazy('offensive_words')
    login_url = reverse_lazy('login')


@method_decorator(user_passes_test(is_admin), name='dispatch')
class DeleteOffensiveWordView(LoginRequiredMixin, DeleteView):
    model = OffensiveWords
    success_url = reverse_lazy('offensive_words')
    login_url = reverse_lazy('login')
    pk_url_kwarg = 'word_id'


@method_decorator(user_passes_test(is_admin), name='dispatch')
class ManageRoomsView(LoginRequiredMixin, FormView):
    template_name = 'account/admin/manage_rooms.html'
    form_class = SearchForm
    success_url = reverse_lazy('manage_rooms')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        query = form.cleaned_data['query']
        if query:
            self.chat_rooms = ChatRoom.objects.filter(name__icontains=query)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        payload = super().get_context_data(**kwargs)
        chat_rooms = getattr(self, 'chat_rooms', ChatRoom.objects.all())
        rooms = []

        for r in chat_rooms:
            if r.uuid not in rooms:
                rooms.append(
                    {
                        "id": r.id,
                        "uuid": r.uuid,
                        "name": r.name,
                        "members": [u.user for u in UserChatRoom.objects.filter(
                            chat_room_id=r.id
                        )]
                    }
                )

        payload.update({
            "page_data": {
                "header": "Existing Chat Rooms",
                "leave_btn": {
                    "url": "account",
                    "name": "Return"
                }
            },
            "rooms": rooms,
        })

        return payload


@method_decorator(user_passes_test(is_admin), name='dispatch')
class ManageUsersView(LoginRequiredMixin, FormView):
    template_name = 'account/admin/manage_users.html'
    form_class = SearchForm
    success_url = reverse_lazy('manage_users')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        query = form.cleaned_data['query']
        if query:
            self.users = User.objects.filter(username__icontains=query)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        payload = super().get_context_data(**kwargs)
        users = getattr(self, 'users', User.objects.all())
        payload.update(
            {
                "page_data": {
                    "header": "Existing Chat Users",
                    "leave_btn": {
                        "url": "account",
                        "name": "Return"
                    }
                },
                "users": users,
            }
        )
        return payload


@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = User.objects.get(pk=user_id)
    form = EditUserForm(request.POST or None,
                        instance=Admins.objects.get_or_create(
                            user_id=user_id,
                        )[0])

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('manage_users')

    payload = {
        "page_data": {
            "header": "Edit User",
            "leave_btn": {
                "url": "manage_users",
                "name": "Return"
            }
        },
        "form": form,
        "u": user,
    }
    return render(request, 'account/admin/edit_user.html', payload)


@method_decorator(user_passes_test(is_admin), name='dispatch')
class DeleteUserView(DeleteView):
    model = User
    success_url = reverse_lazy('manage_users')
    pk_url_kwarg = 'user_id'


@method_decorator(user_passes_test(is_admin), name='dispatch')
class CreateRoomView(CreateView):
    template_name = 'account/admin/manage_users.html'
    model = ChatRoom
    form_class = CreateChatRoomForm
    success_url = reverse_lazy('manage_rooms')

    def form_valid(self, form):
        form.instance.is_public = True
        return super().form_valid(form)


@method_decorator(user_passes_test(is_admin), name='dispatch')
class DeleteRoomView(DeleteView):
    template_name = 'account/admin/manage_users.html'
    model = ChatRoom
    form_class = DeleteChatRoomForm
    success_url = reverse_lazy('manage_rooms')
    slug_url_kwarg = 'room_uuid'
    slug_field = 'uuid'


class AccountView(LoginRequiredMixin, UpdateView):
    template_name = 'account/profile.html'
    success_url = reverse_lazy('account')
    form_class = ProfileForm
    model = User
    login_url = reverse_lazy('login')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        payload = super().get_context_data(**kwargs)
        payload.update({
            "page_data": {
                "header": "Account Page",
                "leave_btn": {
                    "url": "index",
                    "name": "Return"
                }
            },
        })
        return payload


class UploadImageView(UpdateView):
    template_name = 'account/profile.html'
    model = Profile
    form_class = ImageForm
    success_url = reverse_lazy('account')

    def get_object(self):
        return self.request.user.profile


def select_theme(request):
    if not request.user or not request.user.is_authenticated:
        return redirect(reverse_lazy('login'))
    themes = Themes.objects.all()
    if request.method == 'POST':
        theme_id = request.POST.get('theme')
        theme = Themes.objects.get(id=theme_id)
        user = request.user
        user.profile.theme_preference = theme
        user.profile.save()
        return redirect('select_theme')

    payload = {
        "page_data": {
            "header": "Themes",
            "leave_btn": {
                "url": "index",
                "name": "Return"
            }
        },
        "user": request.user,
        "themes": themes,
    }
    return render(request, 'account/themes.html', context=payload)


@method_decorator(user_passes_test(is_admin), name='dispatch')
class ManageThemesView(LoginRequiredMixin, CreateView):
    template_name = 'account/admin/themes.html'
    form_class = ThemeForm
    success_url = reverse_lazy('manage_themes')
    model = Themes
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        payload = super().get_context_data(**kwargs)
        payload.update({
            "page_data": {
                "header": "Themes",
                "leave_btn": {
                    "url": "account",
                    "name": "Return"
                },
            },
            "themes": Themes.objects.all(),
        })
        return payload


@method_decorator(user_passes_test(is_admin), name='dispatch')
class DeleteThemesView(DeleteView):
    model = Themes
    template_name = 'account/admin/themes.html'
    success_url = reverse_lazy('manage_themes')
    pk_url_kwarg = 'theme_id'

