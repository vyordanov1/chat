from django.views.generic.base import TemplateResponseMixin, ContextMixin


class PageDataMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        payload = super().get_context_data(**kwargs)
        current_page_name = self.request.resolver_match
        payload['page_data'] = {
            "leave_btn": {
                "url": "logout",
                "name": current_page_name.__dict__
            },
            "header": current_page_name,
        }
        return payload
