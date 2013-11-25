from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.shortcuts import render
from ui.models import Location, Zone, Building, Session


def _paginate(request, paginator):
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return page, items


# match item with item in list with 'official' capitalization
def _get_original_string_from_list(s, thelist):
    matches = [x for x in thelist if s.lower() == x.lower()]
    if matches:
        return matches[0]
    else:
        return None


def home(request, library, width=0):
    zones = Zone.objects.order_by('floor__building__name', 'display_order')
    locations = Location.objects.all()

    # find library in buildings list, and clean up capitalization
    building = _get_original_string_from_list(
        library, map(str, Building.objects.values_list('name', flat=True)))
    if building:
        zones = zones.filter(floor__building__name=building)
        library_title = " (" + building + ") "
    else:
        building = 'All'
        library_title = ""

    zonelist = []
    # compute display info for each zone
    for zone in zones:
        z = {}
        locations_in_zone = locations.filter(zone=zone)
        locations_win = locations_in_zone.filter(os=Location.WINDOWS7)
        locations_win_available = locations_win.filter(
            state=Location.AVAILABLE)
        locations_mac = locations_in_zone.filter(os=Location.MACOSX)
        locations_mac_available = locations_mac.filter(
            state=Location.AVAILABLE)
        z['building_display'] = str(zone.floor.building.name)
        z['zone_display'] = zone.name
        z['floor_number'] = zone.floor.floor
        z['num_total_win'] = locations_win.count()
        z['num_available_win'] = locations_win_available.count()
        z['num_total_mac'] = locations_mac.count()
        z['num_available_mac'] = locations_mac_available.count()
        #TODO: Remove this after eliminating dependencies
        zonelist.append(z)
        print(z)

    return render(request, 'home.html', {
        'title': 'Computers Available %s - GW Libraries' % library_title,
        'zones': zonelist,
        'library_filter': building,
        'google_analytics_ua': settings.GOOGLE_ANALYTICS_UA,
        'fixedwidth': int(width),
    })


def location(request, library, station):
    locations = Location.objects.filter(
        zone__floor__building__name__iexact=library,
        station_name__iexact=station)
    # TODO: Need to gracefully handle condition where len(l) = 0
    location = locations[0]
    sessions = Session.objects.filter(location=location)
    building = _get_original_string_from_list(
        library, map(str, Building.objects.values_list('name', flat=True)))
    # get building name and floor verbage for this building/floor
    return render(request, 'location.html', {
        'title': 'Station %s - GW Libraries' % station,
        'zone': location.zone.name,
        'bldgname': building,
        'location': location,
        'floor': location.zone.floor.floor,
        'sessions': sessions,
        'paginator': {},
        'page': {},
        'google_analytics_ua': settings.GOOGLE_ANALYTICS_UA,
    })


def floor(request, library, floor_number):
    building = _get_original_string_from_list(
        library, map(str, Building.objects.values_list('name', flat=True)))

    locations = Location.objects.filter(zone__floor__building__name=building,
                                        zone__floor__floor=floor_number)
    locations = locations.order_by('zone__display_order',
                                   'station_name')
    loclist = []
    for location in locations:
        l = {}
        l['zonename'] = location.zone.name
        l['building'] = location.zone.floor.building.name
        l['station_name'] = location.station_name
        l['state_display'] = location.get_state_display()
        l['os_display'] = location.get_os_display()
        loclist.append(l)

    return render(request, 'floor.html', {
        'title': 'Computers Offline - GW Libraries',
        'locations': loclist,
        'building': building,
        'bldgfloorcode': 'g2',
        'google_analytics_ua': settings.GOOGLE_ANALYTICS_UA,
    })


def offline(request, library):
    building = _get_original_string_from_list(
        library, map(str, Building.objects.values_list('name', flat=True)))

    locations = Location.objects.filter(state=Location.NO_RESPONSE)
    if building:
        locations = locations.filter(zone__floor__building__name=building)
    locations = locations.order_by('zone__floor__building__name',
                                   'zone__floor__floor',
                                   'zone__display_order',
                                   'last_offline_start_time')
    loclist = []
    for location in locations:
        l = {}
        l['zonename'] = location.zone.name
        l['building'] = location.zone.floor.building.name
        l['station_name'] = location.station_name
        l['state_display'] = location.get_state_display()
        l['os_display'] = location.get_os_display()
        l['offlinesince'] = location.last_offline_start_time
        loclist.append(l)

    return render(request, 'offline.html', {
        'title': 'Computers Offline - GW Libraries',
        'locations': loclist,
        'building': building,
        'google_analytics_ua': settings.GOOGLE_ANALYTICS_UA,
    })
