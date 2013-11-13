from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.shortcuts import render
from ui.models import Location, Zone, Building


def _paginate(request, paginator):
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return page, items


def home(request, library, width=0):
    zones = Zone.objects.order_by('floor__building__name', 'display_order')
    locations = Location.objects.all()

    # find library in buildings
    building = [str(b) for b
                in Building.objects.values_list('name', flat=True)
                if library.lower() == str(b).lower()]
    # if it's found in the list, then filter further
    if building:
        zones = zones.filter(floor__building__name=building[0])
        library_title = " (" + building[0] + ") "
    else:
        building = 'All'
        library_title = ""

    # compute display info for each floor
    zonelist = []
    for zone in zones:
        z = {}
        locations_zone = locations.filter(zone=zone)
        locations_win = locations_zone.filter(os=Location.WINDOWS7)
        locations_win_available = locations_win.filter(
            state=Location.AVAILABLE)
        locations_mac = locations_zone.filter(os=Location.MACOSX)
        locations_mac_available = locations_mac.filter(
            state=Location.AVAILABLE)
        z['building_display'] = str(zone.floor.building.name)
        # change this to use floor.name if present
        z['floor_display'] = zone.name
        z['num_total_win'] = locations_win.count()
        z['num_available_win'] = locations_win_available.count()
        z['num_total_mac'] = locations_mac.count()
        z['num_available_mac'] = locations_mac_available.count()
        #TODO: Remove this after eliminating dependencies
        z['buildingfloorcode'] = 'g2'
        zonelist.append(z)
        print(z)

    return render(request, 'home.html', {
        'title': 'Computers Available %s - GW Libraries' % library_title,
        'buildingfloors': zonelist,
        'library_filter': building,
        'google_analytics_ua': settings.GOOGLE_ANALYTICS_UA,
        'fixedwidth': int(width),
    })


def location(request, bldgfloorcode, station):
    l = Location.objects.filter(building=bldgfloorcode[0].lower(),
                                floor=int(bldgfloorcode[1]),
                                station_name__iexact=station)
    # TODO: Need to gracefully handle consition where len(l) = 0
    temploc = Location(building=bldgfloorcode[0].lower(),
                       floor=bldgfloorcode[1])
    # get building name and floor verbage for this building/floor
    bldgname = temploc.get_building_display()
    floorname = temploc.display_floor()
    return render(request, 'location.html', {
        'title': 'Station %s - GW Libraries' % station,
        'bldgname': bldgname,
        'floorname': floorname,
        'building': bldgfloorcode[0],
        'location': l.values()[0],
        'floor': bldgfloorcode[1],
        'sessions': {},
        'paginator': {},
        'page': {},
        'google_analytics_ua': settings.GOOGLE_ANALYTICS_UA,
    })


def floor(request, code):
    bldgcode = code[0].lower()
    floornum = int(code[1])
    temploc = Location(building=bldgcode, floor=floornum)
    # get building name and floor verbage for this building/floor
    bldgname = temploc.get_building_display()
    floorname = temploc.display_floor()
    locations = Location.objects.filter(building=bldgcode, floor=floornum).\
        order_by('state', 'os', 'station_name').values()
    for l in locations:
        l['state_display'] = Location(state=l['state']).get_state_display()
        l['os_display'] = Location(os=l['os']).get_os_display()
    return render(request, 'floor.html', {
        'title': 'Computers Available: %s %s - GW Libraries' % (bldgname,
                                                                floorname),
        'bldgfloorcode': code,
        'locations': locations,
        'building': bldgname,
        'floorname': floorname,
        'google_analytics_ua': settings.GOOGLE_ANALYTICS_UA,
    })


def offline(request, library):
    library = library.lower()
    if library in ['gelman', 'eckles', 'vstc']:
        # WARNING: this makes an assumption about
        # the choices dictionary in the model
        librarycode = {'gelman': 'g', 'eckles': 'e', 'vstc': 'v'}[library]

    locations = Location.objects.filter(building=librarycode,
                                        state=Location.NO_RESPONSE).\
        order_by('floor', 'last_offline_start_time').values()
    temploc = Location(building=librarycode)
    # get building name and floor verbage for this building/floor
    bldgname = temploc.get_building_display()
    for l in locations:
        temploc = Location(building=l['building'], floor=l['floor'])
        floorname = temploc.display_floor()
        l['floorname'] = floorname
        l['state_display'] = Location(state=l['state']).get_state_display()
        l['os_display'] = Location(os=l['os']).get_os_display()
        l['bldgfloorcode'] = l['building'] + str(l['floor'])
        l['offlinesince'] = l['last_offline_start_time']

    return render(request, 'offline.html', {
        'title': 'Computers Offline - GW Libraries',
        'locations': locations,
        'building': bldgname,
        'google_analytics_ua': settings.GOOGLE_ANALYTICS_UA,
    })
