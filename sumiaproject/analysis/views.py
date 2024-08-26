import os
import nltk
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import chardet

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']

        # Validate file size
        if uploaded_file.size > 10 * 1024 * 1024:  # 10MB
            return JsonResponse({'error': 'Archivo demasiado grande'}, status=400)

        # Read file contents and detect encoding
        file_contents = uploaded_file.read()
        encoding = chardet.detect(file_contents)['encoding']

        # Analyze file contents using NLTK
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')

        stop_words = set(stopwords.words('spanish'))
        tokens = word_tokenize(file_contents.decode(encoding))
        filtered_text = ' '.join([word for word in tokens if word.casefold() not in stop_words])

        # Create analysis result
        analysis_result = f"Análisis del archivo:\n{filtered_text}"

        # Return JSON response
        response_data = {
            'analysis_result': analysis_result,
            'debug': 'Received request: ' + str(request)
        }
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)