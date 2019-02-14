from django.views.generic.base import TemplateView

from accounts.models import User

class HomeView(TemplateView):
    template_name = 'core/index.html'
    context_object_name = 'userz'

    # def get_context_data(self, **kwargs):
    #     context = super(HomeView, self).get_context_data(**kwargs)
    #     return context
