from ..models import Album, Image
#from django.db.models import Q

def get_image_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        images = Image.objects.filter(
            #Q(title__icontains=q) | Q(body__icontains=q)
        )#.distinct()
        for image in images:
            queryset.append(image)

    return list(set(queryset))

def get_album_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        albums = Album.objects.filter(
            
        )
        for album in albums:
            queryset.append(album)
            
    return list(set(queryset))





#FOR PAGINATION AND QUERIES
from django.shortcuts import render
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

IMAGES_PER_PAGE = 50

def home_screen_view(request, *args, **kwargs):

	context = {}

	# Search
	query = ""
	if request.GET:
		query = request.GET.get('q', '')
		context['query'] = str(query)

	images = sorted(get_image_queryset(query), key=attrgetter('date_updated'), reverse=True)
	# Pagination
	page = request.GET.get('page', 1)
	images_paginator = Paginator(images, IMAGES_PER_PAGE)
	try:
		images = images_paginator.page(page)
	except PageNotAnInteger:
		images = images_paginator.page(IMAGES_PER_PAGE)
	except EmptyPage:
		images = images_paginator.page(images_paginator.num_pages)

	context['images'] = images
    #return render(request, "personal/home.html", context)