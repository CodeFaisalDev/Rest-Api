from django.forms import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from watchlist_app.api.permissions import AdminOrReadOnly, ReviewUpdateUserOrReadOnly
from watchlist_app.api.serializers import StreamSerializer, WatchListSerializer, ReviewSerializer
from watchlist_app.models import WatchList, Stream, Review

class WatchListAV(ListCreateAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer

class WatchDetailAV(RetrieveUpdateDestroyAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    permission_classes = [AdminOrReadOnly]


class StreamAV(ListCreateAPIView):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer

class StreamDetailsAV(RetrieveUpdateDestroyAPIView):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer

class ReviewCreateAV(CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        movie = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=movie, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError('You can only create one review')

        if movie.review_count == 0:
            movie.average_review = serializer.validated_data['rating']
        else:
            total_rating = movie.average_review * movie.review_count
            total_rating += serializer.validated_data['rating']
            movie.average_review = total_rating / (movie.review_count + 1)

        movie.review_count = movie.review_count + 1
        movie.save()

        serializer.save(watchlist=movie, review_user=review_user)

class ReviewAV(ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist = pk)
        

class ReviewDetailAV(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]


# class WatchListAV(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
    
#     queryset = WatchList.objects.all()
#     serializer_class = WatchListSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class WatchDetailAV(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
    
#     queryset = WatchList.objects.all()
#     serializer_class = WatchListSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
    
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

    
# class StreamAV(mixins.ListModelMixin,
#                mixins.CreateModelMixin,
#                generics.GenericAPIView):
    
#     queryset = Stream.objects.all()
#     serializer_class = StreamSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class StreamDetailsAV(mixins.RetrieveModelMixin, 
#                       mixins.UpdateModelMixin, 
#                       mixins.DestroyModelMixin, 
#                       generics.GenericAPIView):

#     queryset = Stream.objects.all()
#     serializer_class = StreamSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)       
    
    
# class ReviewAV(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    
# class ReviewDetailAV(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
    
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
    
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

# class WatchListAV(APIView):

#     def get(self, request):
#         movie = WatchList.objects.all()
#         serializer = WatchListSerializer(movie, many = True, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = WatchListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class WatchDetailAV(APIView):

#     def get(self, request, pk):
#         try:
#             movie = WatchList.objects.get(pk = pk)
#             serializer = WatchListSerializer(movie, context={'request': request})
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except:
#             return Response(status=status.HTTP_404_NOT_FOUND)
    
#     def put(self, request, pk):
#         movie = WatchList.objects.get(pk=pk)
#         serializer = WatchListSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
#         else:
#             return Response(serializer.errors, status=status.HTTP_502_BAD_GATEWAY)
    
#     def delete(self, request,pk):
#         movie = WatchList.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
# class StreamAV(APIView):
#     def get(self, request):
#         stream = Stream.objects.all()
#         serializer = StreamSerializer(stream, many = True, context={'request': request})
#         return Response(serializer.data, status= status.HTTP_200_OK)
    
#     def post(self, request):
#         serializer = StreamSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status= status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


# class StreamDetailsAV(APIView):
#     def get(self, request, pk):
#         stream = Stream.objects.get(pk=pk)
#         serializer = StreamSerializer(stream, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def put(self, request, pk):
#         stream = Stream.objects.get(pk=pk)
#         serializer = StreamSerializer(stream, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#    def delete(self, request, pk):
#        stream = Stream.objects.get(pk=pk)
#        stream.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)


# class ReviewAV(APIView):
#     def get(self, request, pk):
#         stream = Review.objects.get(pk=pk)
#         serializer = ReviewSerializer(stream, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def put(self, request, pk):
#         stream = Review.objects.get(pk=pk)
#         serializer = ReviewSerializer(stream, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         stream = Review.objects.get(pk=pk)
#         stream.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    





    
    
# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data, status = status.HTTP_201_CREATED)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
# @api_view(["GET", "PUT", "DELETE"])
# def movie_detail(request, pk):
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk = pk)
#         except Movie.DoesNotExist:
#             return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk = pk)
#         serializer = MovieSerializer(movie, data=request.data, status= status.HTTP_202_ACCEPTED)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk = pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)