from rest_framework import serializers
from watchlist_app.models import Stream, WatchList, Review

class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    review_user =serializers.StringRelatedField(read_only=True)

    class Meta:
        model =  Review
        exclude = ('watchlist',)
        # fields = "__all__"    

class WatchListSerializer(serializers.HyperlinkedModelSerializer):
    reviews = ReviewSerializer(many = True, read_only = True)
    class Meta:
        model = WatchList
        fields = "__all__"
    

class StreamSerializer(serializers.HyperlinkedModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = Stream
        fields = "__all__"
   

# def name_length(name):
#     if len(name) < 2:
#         raise serializers.ValidationError("Name length must be at least 2 characters")

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance

#     def validate_name(self, value):
#         if len(value) < 2:
#             raise serializers.ValidationError("Name is too short")
#         else:
#             return value
        
    # def validate(self, data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError("Name and description cannot be same")
    #     else:
    #         return data