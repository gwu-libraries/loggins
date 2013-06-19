from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection
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
    cursor = connection.cursor()
    cursor.execute('''
        SELECT COUNT(*), 
            SUBSTRING(ui_host.location FROM 1 FOR 1) AS library, 
            SUBSTRING(ui_host.location FROM 2 FOR 1) AS floor, event
            FROM ui_record r1, ui_host        
            WHERE timestamp=(
                SELECT MAX(timestamp)
                FROM ui_record
                WHERE host_id=r1.host_id
                AND location != ''
            )
            AND ui_host.id = r1.host_id
            AND ui_host.is_active IS true 
            GROUP BY library, floor, event 
            ORDER BY library, floor, event;
        ''')
    codes = {}
    # presuming a small dataset; we can get away with fetchall()
    for row in cursor.fetchall():
        count, library, floor, event = row        
        code = library + floor
        try:
            s = codes[code]
        except:
            # 'available' needs to default to 0; otherwise the logic here 
            # never sets it, in the case where there are 0 hosts available
            # on a floor
            s = {'code': code, 'floor': floor, 'available': 0}
        if library == 'g':
            s['library'] = 'Gelman'
        elif library == 'e':
            s['library'] = 'Eckles'
        elif library == 'v':
            s['library'] = 'VSTC'
        if event == 'i':
            s['unavailable'] = count
        elif event == 'o':
            s['available'] = count
        s['total'] = s.get('available', 0) + s.get('unavailable', 0)
        codes[code] = s
    all_floors = sorted([(code, s) for code, s in codes.items()])
    floors = [floor for code, floor in all_floors]
    return render(request, 'home.html', {
        'title': 'home',
        'codes': codes,
        'floors': floors,
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


def floor(request, code):
    hosts = Record.objects.raw('''
        SELECT *
        FROM ui_record r1, ui_host        
        WHERE timestamp=(
            SELECT MAX(timestamp)
            FROM ui_record
            WHERE host_id=r1.host_id
            AND SUBSTRING(location FROM 1 FOR 2) = %s
        )
        AND ui_host.id = r1.host_id
        AND ui_host.is_active IS true
        ORDER BY location
        ''', [code])
    return render(request, 'floor.html', {
        'title': 'floor: %s' % code,
        'hosts': hosts,
    })
