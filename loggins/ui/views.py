from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from ui.models import Record


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
        )
        AND ui_host.id = r1.host_id
        AND ui_host.is_active IS true
        ORDER BY ui_host.name''')

    return render(request, 'home.html', {
        'title': 'home',
        'records': records,
        'state': state,
    })
