from django.template.response import TemplateResponse
from utils.views import render_to
from django.contrib.gis.geoip import GeoIP

from content.forms import TicketSearchForm
from content.models import Log


def home(request, template='home.html'):
    context = {
        'form': TicketSearchForm(),
    }
    return TemplateResponse(request, template, context)


@render_to('chance.html')
def get_chance(request):
    form = TicketSearchForm(request.GET or None)
    context = {'form': form}
    if form.is_valid():
        data = form.get_data_object()
        data.create_log(type=Log.CHANCE)
        context.update({'data': data})
    return context


@render_to('laws.html')
def get_laws(request):
    form = TicketSearchForm(request.GET or None)
    context = {'form': form}
    if form.is_valid():
        start_hour = request.GET['from_time']
        end_hour = request.GET['to_time']
        week_day = request.GET['week_day']
        data = form.get_data_object(start_hour=start_hour, end_hour=end_hour, week_day=week_day)
        data.create_log(type=Log.LAWS)
        context.update({'data': data})
    return context


@render_to('heatmap.html')
def get_heatmap(request):
    form = TicketSearchForm(request.GET or None)
    context = {'form': form}
    if form.is_valid():
        data = form.get_data_object()
        data.create_log(type=Log.HEATMAP)
        if data.tickets_avg_cost <= 0:
            dist = request.GET['distance']
            choices = TicketSearchForm.DISTANCE_CHOICES
            if dist != choices[-1][0]:
                for c in choices:
                    if c[0] == dist:
                        context.update({'next_distance': choices[choices.index(c)+1][0]})
                        break
            context.update({'null': True})
        context.update({'data': data})
    return context


@render_to('debug.html')
def debug(request):
    form = TicketSearchForm(request.GET or None)
    form_is_valid = form.is_valid()
    context = {
        'form': form,
        'form_is_valid': form_is_valid,
    }
    if form_is_valid:
        data = form.get_data_object()
        context.update({'data': data})
    return context