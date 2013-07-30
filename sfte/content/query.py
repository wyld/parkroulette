from decimal import Decimal
from django.core.cache import get_cache
from content.models import Ticket, Path


paths_cache = get_cache('paths')
tickets_cache = get_cache('tickets')


def _get_cache_name(geopoint, distance, week_day=None):
    if week_day:
        return '%s,%s,%s,%s' % (week_day, geopoint._cs[0][0], geopoint._cs[0][1], distance)
    return '%s,%s,%s' % (geopoint._cs[0][0], geopoint._cs[0][1], distance)


def _get_path_qs(geopoint, distance):
    ph_qs = paths_cache.get(_get_cache_name(geopoint, distance), 'empty')
    if ph_qs == 'empty':
        ph_qs = Path.objects.filter(valid=True).filter(path__dwithin=(geopoint, Decimal(distance)))
        paths_cache.set(_get_cache_name(geopoint, distance), ph_qs)
    return ph_qs


def _get_ticket_qs(geopoint, distance, start_hour=None, end_hour=None, week_day=None):
    if week_day:
        tc_qs = tickets_cache.get(_get_cache_name(geopoint, distance, week_day), 'empty')
        if tc_qs == 'empty':
            tc_qs = Ticket.objects.filter(geopoint__dwithin=(geopoint, Decimal(distance)), issue_datetime__week_day=week_day)
            tickets_cache.set(_get_cache_name(geopoint, distance, week_day))
        # for now django can't filter by __hour__lt (only by __hour in dev version) //28.02.2013
    else:
        tc_qs = tickets_cache.get(_get_cache_name(geopoint, distance), 'empty')
        if tc_qs == 'empty':
            tc_qs = Ticket.objects.filter(geopoint__dwithin=(geopoint, Decimal(distance)))
            tickets_cache.set(_get_cache_name(geopoint, distance), tc_qs)
    if start_hour is not None:
        tc_qs = tc_qs.extra(
            where=[
                'EXTRACT(hour FROM issue_datetime) < %s',
                'EXTRACT(hour FROM issue_datetime) >= %s',
            ],
            params=[end_hour, start_hour]
        )
    return tc_qs
