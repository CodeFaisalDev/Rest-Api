# from django.shortcuts import render
# from watchlist_app.models import Movie
# from django.http import JsonResponse

# # Create your views here.
# def movie_list(request):
#     movie = Movie.objects.all()
#     data = {
#         'movies' : list(movie.values()),
#     }

#     return JsonResponse(data)

# def movie_details(request, pk):
#     movie = Movie.objects.get(pk=pk)
#     data = {
#         'Name' : movie.name,
#         'description' : movie.discription,
#         'available' : movie.active,
#     }

#     return JsonResponse(data)