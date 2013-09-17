from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render
from ui.models import Location


def _paginate(request, paginator):
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return page, items


def home(request, library):
    locations = Location.objects
    # create an iterable with one item per unique building/floor combo
    buildingfloors = locations.values('building', 'floor').distinct(
        'building', 'floor')
    # if URL contained a specific (and known) library, filter reults further
    library = library.lower()
    if library in ['gelman', 'eckles', 'vstc']:
        # WARNING: this makes an assumption about
        # the choices dictionary in the model
        librarycode = {'gelman': 'g', 'eckles': 'e', 'vstc': 'v'}
        buildingfloors = buildingfloors.filter(building=librarycode[library])
    # compute display info for each floor
    for f in buildingfloors:
        temploc = Location(building=f['building'], floor=f['floor'])
        # get building name and floor verbage for this building/floor
        bldgname = temploc.get_building_display()
        floorname = temploc.display_floor()
        # compute total vs. available locations
        locations_on_this_floor = locations.filter(
            building=f['building'], floor=f['floor'])
        winlocations = locations_on_this_floor.filter(os=Location.WINDOWS7)
        num_total_win = winlocations.count()
        num_available_win = winlocations.filter(
            state=Location.AVAILABLE).count()
        maclocations = locations_on_this_floor.filter(os=Location.MACOSX)
        num_total_mac = maclocations.count()
        num_available_mac = maclocations.filter(
            state=Location.AVAILABLE).count()
        f['buildingfloorcode'] = f['building'] + str(f['floor'])
        f['building_display'] = bldgname
        f['floor_display'] = floorname
        f['num_total_win'] = num_total_win
        f['num_available_win'] = num_available_win
        f['num_total_mac'] = num_total_mac
        f['num_available_mac'] = num_available_mac

    if library.lower() == 'gelman':
        library_filter = 'Gelman'
    elif library.lower() == 'eckles':
        library_filter = 'Eckles'
    elif library.lower() == 'vstc':
        library_filter = 'VSTC'
    else:
        library_filter = 'All'

    return render(request, 'home.html', {
        'title': 'Computers Available - GW Libraries',
        'buildingfloors': buildingfloors,
        'library_filter': library_filter,
    })


def location(request, bldgfloorcode, station):
    l = Location.objects.filter(building=bldgfloorcode[0].lower(),
                                floor=int(bldgfloorcode[1]),
                                station_name__iexact=station)
    # TODO: Need to gracefully handle consition where len(l) = 0
    temploc = Location(building=bldgfloorcode[0].lower(), floor=bldgfloorcode[1])
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
        'title': 'Computers Available: %s %s - GW Libraries' % (bldgname, floorname),
        'bldgfloorcode': code,
        'locations': locations,
        'building': bldgname,
        'floorname': floorname,
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
    })
