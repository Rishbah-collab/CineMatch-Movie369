from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# ML recommender imports
from .recommender import (
    recommend_by_movie,
    top_rated_movies,
    collaborative_recommend
)

# DB model
from .models import Movie


# ================================
# HOME (Frontend Page)
# ================================
def home(request):
    return render(request, "index.html")

def login_view(request):
    return render(request, 'login.html')


# ================================
# ML BASED APIs
# ================================

# 1️⃣ Top Rated Movies (ML)
def top_movies(request):
    return JsonResponse({
        "movies": top_rated_movies(10)
    })


# 2️⃣ Content Based Recommendation
# /movies/recommend/movie/?title=Toy Story
def recommend_movie(request):
    title = request.GET.get("title")

    if not title:
        return JsonResponse({"error": "title parameter required"}, status=400)

    return JsonResponse({
        "recommendations": recommend_by_movie(title)
    })


# 3️⃣ Collaborative Filtering
# /movies/recommend/user/?user_id=1
def user_recommendation(request):
    user_id = request.GET.get("user_id")

    if not user_id:
        return JsonResponse({"error": "user_id required"}, status=400)

    return JsonResponse({
        "recommendations": collaborative_recommend(int(user_id))
    })


# ================================
# FRONTEND MOVIES API (DB → JS)
# ================================
# /movies/api/
def movies_api(request):
    movies = Movie.objects.all()
    data = []

    for movie in movies:
        data.append({
            "id": movie.id,
            "title": movie.title,
            "genres": movie.genre.split('|'),
            "rating": movie.rating,
            "image": movie.image
        })

    return JsonResponse({"movies": data})
