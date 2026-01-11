# F:\AIMovieRecommendation\recommender\views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json

# Home page
def home(request):
    """Home page with all movies"""
    return render(request, 'index.html')

# Login View
def login_view(request):
    """User login page"""
    if request.method == 'POST':
        try:
            # Check if it's JSON or form data
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                email = data.get('email')
                password = data.get('password')
            else:
                email = request.POST.get('email')
                password = request.POST.get('password')
            
            # Authenticate user
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'status': 'success',
                    'message': 'Login successful!',
                    'redirect': '/'
                })
            else:
                # Check demo credentials
                if email == 'demo@cinematch.com' and password == 'demo123':
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Demo login successful!',
                        'user': 'Demo User'
                    })
                
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid email or password'
                })
        
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    # GET request - render login page
    return render(request, 'login.html')

# Signup View
def signup_view(request):
    """User registration page"""
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                name = data.get('name')
                email = data.get('email')
                password = data.get('password')
            else:
                name = request.POST.get('name')
                email = request.POST.get('email')
                password = request.POST.get('password')
            
            # Check if user exists
            if User.objects.filter(username=email).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'Email already exists'
                })
            
            # Create user
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name
            )
            user.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Account created successfully!'
            })
        
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return render(request, 'login.html')

# Logout View
def logout_view(request):
    """User logout"""
    logout(request)
    return redirect('login')

# Get Recommendations
@csrf_exempt
def get_recommendations(request):
    """Get movie recommendations"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            filter_type = data.get('filter_type', 'hybrid')
            genre_filter = data.get('genre_filter', 'all')
            
            # Sample recommendations
            recommendations = [
                {'id': 1, 'title': 'Maleficent', 'genres': ['Fantasy', 'Adventure'], 'rating': 4.2},
                {'id': 2, 'title': 'Inception', 'genres': ['Sci-Fi', 'Action'], 'rating': 4.8},
                {'id': 3, 'title': 'The Dark Knight', 'genres': ['Action', 'Drama'], 'rating': 4.9},
            ]
            
            return JsonResponse({
                'status': 'success',
                'recommendations': recommendations
            })
        
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

# Wishlist functions
@csrf_exempt
def add_to_wishlist(request):
    """Add to wishlist"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            movie_id = data.get('movie_id')
            
            if 'wishlist' not in request.session:
                request.session['wishlist'] = []
            
            if movie_id not in request.session['wishlist']:
                request.session['wishlist'].append(movie_id)
                request.session.modified = True
            
            return JsonResponse({'status': 'success', 'message': 'Added to wishlist'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@csrf_exempt
def get_wishlist(request):
    """Get wishlist"""
    wishlist = request.session.get('wishlist', [])
    return JsonResponse({'status': 'success', 'wishlist': wishlist})

# Search movies
def search_movies(request):
    """Search movies"""
    query = request.GET.get('q', '')
    
    results = [
        {'id': 1, 'title': 'Maleficent', 'genres': ['Fantasy']},
        {'id': 2, 'title': 'Inception', 'genres': ['Sci-Fi']},
    ]
    
    if query:
        results = [m for m in results if query.lower() in m['title'].lower()]
    
    return JsonResponse({'status': 'success', 'results': results})