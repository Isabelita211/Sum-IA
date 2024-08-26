import os
import nltk
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from corsheaders.defaults import default_headers
import chardet

nltk.download('punkt')

@csrf_exempt
def upload_file(request):
    try:
        if request.method == 'POST':
            uploaded_file = request.FILES['file']

            # Validate file size
            if uploaded_file.size > 30 * 1024 * 1024:  # 30MB
                return JsonResponse({'error': 'Archivo demasiado grande'}, status=400)

            # Read file contents and detect encoding
            file_contents = uploaded_file.read()
            encoding = chardet.detect(file_contents)['encoding']

            # Analyze file contents using NLTK
            try:
                nltk.data.find('tokenizers/punkt')
                nltk.data.find('corpora/stopwords')
            except LookupError as e:
                print(f"Error downloading NLTK resources: {e}")
                nltk.download('punkt')
                nltk.download('stopwords')

            stop_words = set(stopwords.words('spanish'))
            try:
                tokens = word_tokenize(file_contents.decode(encoding))
            except UnicodeDecodeError as e:
                print(f"Error decoding file contents: {e}")
                return JsonResponse({'error': 'Error decoding file contents'}, status=400)

            filtered_text = ' '.join([word for word in tokens if word.casefold() not in stop_words])

            # Create analysis result
            analysis_result = f"Análisis del archivo:\n{filtered_text}"

            # Return JSON response
            response_data = {
                'analysis_result': analysis_result,
                'debug': 'Received request: ' + str(request)
            }
            response = JsonResponse(response_data, safe=False)
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Headers'] = ', '.join(default_headers)
            return response
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)
    except Exception as e:
        print(f"Error occurred: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=500)