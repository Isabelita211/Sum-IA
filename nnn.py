import os
import nltk
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES['file']
        message = request.POST['message']

        # Analiza el contenido del archivo utilizando NLTK
        nltk.download('punkt')
        nltk.download('stopwords')
        stop_words = set(stopwords.words('spanish'))

        tokens = word_tokenize(file.read().decode())

        filtered_text = ' '.join([word for word in tokens if word.casefold() not in stop_words])

        # Devuelve una respuesta JSON
        response_data = {
            'message': message,
            'analysis_result': 'Tu resultado de análisis'
        }
        return JsonResponse(response_data)
    
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    # ...
]