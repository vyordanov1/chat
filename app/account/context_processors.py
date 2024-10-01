from .forms import ImageForm


def image_upload_form(request):
    if request.user.is_authenticated:
        form = ImageForm(request.POST, request.FILES,
                         instance=request.user.profile)
        return {'image_form': form}
    return {}