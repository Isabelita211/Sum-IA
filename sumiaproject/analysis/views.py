import os
import nltk
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from corsheaders.defaults import default_headers
import chardet
import logging

# Configuración del logger
logger = logging.getLogger(__name__)

nltk.download('punkt')

@csrf_exempt
@require_http_methods(['POST'])
def upload_file(request):
    try:
        uploaded_file = request.FILES.get('file')
        print(request.FILES)
        if uploaded_file:
            # Configura la codificación del archivo
            uploaded_file.charset = 'utf-8'

            # Valida el tamaño del archivo
            if uploaded_file.size > 30 * 1024 * 1024:  # 30MB
                return JsonResponse({'error': 'Archivo demasiado grande'}, status=400)

            # Lee el contenido del archivo en chunks
            chunk_size = 1024 * 1024  # 1MB
            file_contents = bytearray()
            while True:
                chunk = uploaded_file.read(chunk_size)
                if not chunk:
                    break
                file_contents.extend(chunk)

            # Detecta la codificación del archivo
            encoding = chardet.detect(file_contents)['encoding']
            if encoding is None:
                logger.error("No se pudo detectar la codificación del archivo")
                return JsonResponse({'error': 'No se pudo detectar la codificación del archivo'}, status=400)

            # Analiza el contenido del archivo utilizando NLTK
            try:
                nltk.data.find('tokenizers/punkt')
                nltk.data.find('corpora/stopwords')
            except LookupError as e:
                logger.error(f"Error al descargar los recursos de NLTK: {e}")
                nltk.download('punkt')
                nltk.download('stopwords')

            stop_words = set(stopwords.words('spanish'))
            try:
                tokens = word_tokenize(file_contents.decode(encoding))
            except UnicodeDecodeError as e:
                logger.error(f"Error al decodificar el contenido del archivo: {e}")
                return JsonResponse({'error': 'Error al decodificar el contenido del archivo'}, status=400)

            filtered_text = ' '.join([word for word in tokens if word.casefold() not in stop_words])

            # Crea el análisis del archivo
            analysis_result = f"Análisis del archivo:\n{filtered_text}"

            # Retorna JSON response
            response_data = {
                'analysis_result': analysis_result,
                'debug': 'Received request: ' + str(request)
            }
            response = JsonResponse(response_data, safe=False)
            print(type(response))  # Debería imprimir <class 'django.http.JsonResponse'>
            print(response.content)  # Debería imprimir el contenido de la respuesta en formato JSON
            print(response.status_code)  # Debería imprimir 200
            print(response.headers)  # Debería imprimir las cabeceras de la respuesta
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Headers'] = ', '.join(default_headers)
            return response
        else:
            # Devolver un error si no se proporcionó un archivo
            return JsonResponse({'error': 'No file uploaded'}, status=400)
    except Exception as e:
        logger.error(f"Error ocurrido: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=500)