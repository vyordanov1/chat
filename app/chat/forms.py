from django import forms

from .models import ChatRoom


class BaseChatRoomForm(forms.ModelForm):
    class Meta:
        abstract = True
        model = ChatRoom
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget = forms.HiddenInput()


class CreateChatRoomForm(BaseChatRoomForm):
    class Meta(BaseChatRoomForm.Meta):
        pass


class DeleteChatRoomForm(BaseChatRoomForm):
    class Meta(BaseChatRoomForm.Meta):
        pass