from django.shortcuts import render
from .recommend import get_recommendations

def home(request):
    return render(request, 'home.html')





def recommend(request):
    song = request.GET.get('song', '')
    artist = request.GET.get('artist', '')

    # Process the recommendation logic here

    return render(request, 'recommendation_result.html', {'song': song, 'artist': artist})
