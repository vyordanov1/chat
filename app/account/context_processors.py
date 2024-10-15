from .forms import ImageForm


def image_upload_form(request):
    """
     Context processor ensures the context passed by the function
     is being passed to all templates globally.
     Unnecessary for all templates, but useful on the admin page for
     the image upload form!
    """
    if request.user.is_authenticated:
        form = ImageForm(request.POST, request.FILES,
                         instance=request.user.profile)
        return {'image_form': form}
    return {}