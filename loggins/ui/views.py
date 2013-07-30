from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection
from django.shortcuts import get_object_or_404, render

from ui.models import Location, Session


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
    if library.lower() in ['gelman', 'eckles', 'vstc']:
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
        locations_on_this_floor = locations.filter(building=f['building'],
                                                   floor=f['floor'])
        num_total = locations_on_this_floor.count()
        num_available = \
            locations_on_this_floor.filter(state=Location.AVAILABLE).count()
        f['buildingfloorcode'] = f['building'] + str(f['floor'])
        f['building_display'] = bldgname
        f['floor_display'] = floorname
        f['num_total'] = num_total
        f['num_available'] = num_available

    if library.lower() == 'gelman':
        library_filter = 'Gelman'
    elif library.lower() == 'eckles':
        library_filter = 'Eckles'
    elif library.lower() == 'vstc':
        library_filter = 'VSTC'
    else:
        library_filter = 'All'

    return render(request, 'home.html', {
        'buildingfloors': buildingfloors,
        'library_filter': library_filter,
    })



def location(request, bldgfloorcode, station):
    # TODO make station match non-case-sensitive
    l = Location.objects.filter(building=bldgfloorcode[0],
                                floor=bldgfloorcode[1],
                                station_name=station)
    if len(l) == 0:
        # TODO: need to handle this condition
        x = 0
    temploc = Location(building=bldgfloorcode[0], floor=bldgfloorcode[1])
    # get building name and floor verbage for this building/floor
    bldgname = temploc.get_building_display()
    floorname = temploc.display_floor()
    return render(request, 'location.html', {
        'location': l.values()[0],
        'building': bldgfloorcode[0],
        'floor': bldgfloorcode[1],
        'sessions': {},
        'paginator': {},
        'page': {},
    })


def floor(request, code):
    temploc = Location(building=code[0], floor=code[1])
    # get building name and floor verbage for this building/floor
    bldgname = temploc.get_building_display()
    #TODO: floorname is not displaying properly for 0th floor
    floorname = temploc.display_floor()
    locations = Location.objects.filter(building=code[0],
                                        floor=code[1]).values()
    for l in locations:
        l['state_display'] = Location(state=l['state']).get_state_display()
    return render(request, 'floor.html', {
        'bldgfloorcode': code,
        'locations': locations,
        'building': bldgname,
        'floorname': floorname,
    })
