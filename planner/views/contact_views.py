from django.views.generic import TemplateView


class ContactView(TemplateView):
    template_name = 'planner/modals/contact_modal.html'
