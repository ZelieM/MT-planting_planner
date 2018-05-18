from django.views.generic import TemplateView


class PWAOfflineView(TemplateView):
    template_name = 'planner/pwa_offline_view.html'