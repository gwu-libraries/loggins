from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render

from ui.models import Host, Record


def _paginate(request, paginator):
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return page, items


def home(request):
    qs_records = Record.objects.order_by('-timestamp')
    paginator = Paginator(qs_records, 50)
    page, records = _paginate(request, paginator)
    state = Record.objects.raw('''
        SELECT *
        FROM ui_record r1, ui_host
        WHERE timestamp=(
            SELECT MAX(timestamp)
            FROM ui_record
            WHERE host_id=r1.host_id
            AND location != ''
        )
        AND ui_host.id = r1.host_id
        AND ui_host.is_active IS true
        ORDER BY location''')

    return render(request, 'home.html', {
        'title': 'home',
        'records': records,
        'state': state,
    })


def host(request, host_id):
    host = get_object_or_404(Host, pk=host_id)
    paginator = Paginator(host.records.order_by('-timestamp'), 25)
    page, records = _paginate(request, paginator)
    return render(request, 'host.html', {
        'title': 'host: %s (%s)' % (host.id, host.location),
        'host': host,
        'records': records,
        'paginator': paginator,
        'page': page,
    })
