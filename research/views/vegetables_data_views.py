from django.views.generic import TemplateView


class VegetablesView(TemplateView):
    template_name = 'research/vegetables.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from planner.models import Vegetable as gardens_vegetables
        vegetables = gardens_vegetables.objects.filter(garden__activity_data_available_for_research=True)
        context['vegetables'] = vegetables
        from vegetables_library.models import Vegetable as library_vegetables
        library_vegetables = library_vegetables.objects.all()
        context['library_vegetables'] = library_vegetables
        return context
