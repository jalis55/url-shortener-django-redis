from rest_framework.views import APIView
from rest_framework import status
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.response import Response
import redis
from .utils import generate_short_code
from .serializers import URLSerializer


redis_client = redis.Redis(host='localhost', port=6379, db=1)


class ShortenerAPIView(APIView):
       
    def get(self, request):
        # Check if API docs are cached
        cached_docs = cache.get('api_docs')
        if cached_docs:
            return Response(cached_docs)

        # API documentation
        docs = {
            'message': 'Welcome to the URL Shortener API',
            'endpoints': {
                'POST /api/shorten/': 'Submit a URL to get a shortened version',
                'GET /<short_code>/': 'Redirect to the original URL'
            }
        }
        # Cache for 5 minutes (300 seconds)
        cache.set('api_docs', docs, timeout=300)
        return Response(docs)

    def post(self, request):
        serializer = URLSerializer(data=request.data)
        if serializer.is_valid():
            original_url = serializer.validated_data['original_url']
            short_code = generate_short_code()

            # Ensure short_code is unique
            while redis_client.exists(short_code):
                short_code = generate_short_code()

            # Store in Redis with 24-hour expiration (86,400 seconds)
            try:
                redis_client.setex(short_code, 86400, original_url)
            except redis.RedisError:
                return Response({'error': 'Redis error, please try again'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Generate short URL
            short_url = request.build_absolute_uri('/') + short_code
            return Response({'short_url': short_url}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
def redirect_url(request, short_code):
    # Get original URL from Redis
    try:
        original_url = redis_client.get(short_code)
        if original_url:
            return redirect(original_url.decode('utf-8'))
        return HttpResponse("URL not found or expired", status=404)
    except redis.RedisError:
        return HttpResponse("Redis error, please try again", status=500)
