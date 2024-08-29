import os
import pytesseract
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from corsheaders.defaults import default_headers
import docx
import logging
import mimetypes

# Configuración del logger
logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(['POST'])
def upload_file(request):
    try:
        # Obtiene el archivo subido
        uploaded_file = request.FILES.get('file')

        if uploaded_file:
            # Valida el tipo de archivo
            file_type, _ = mimetypes.guess_type(uploaded_file.name)
            if file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                # Lee el contenido del archivo de Word
                doc = docx.Document(uploaded_file)
                text = []
                for para in doc.paragraphs:
                    text.append(para.text)
                text = '\n'.join(text)
            else:
                # Retorna un error si el archivo no es de tipo Word o PDF
                return JsonResponse({'error': 'Archivo no soportado'}, status=400)

            # Extrae el resumen del documento
            summary = ''
            sentences = text.split('. ')
            for sentence in sentences:
                if len(sentence) > 20:  # Filtra oraciones cortas
                    summary += sentence + '. '
            summary = summary.strip()

            # Valida el tamaño del archivo
            if uploaded_file.size > 30 * 1024 * 1024:  # 30MB
                # Retorna un error si el archivo es demasiado grande
                return JsonResponse({'error': 'Archivo demasiado grande'}, status=400)

            # Crea el análisis del archivo
            analysis_result = f"Resumen del archivo:\n{summary}"

            # Retorna la respuesta JSON
            response_data = {
                'analysis_result': analysis_result,
                'debug': 'Solicitud recibida: ' + str(request)
            }
            response = JsonResponse(response_data, safe=False)
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Headers'] = ', '.join(default_headers)
            return response
        else:
            # Retorna un error si no se proporcionó un archivo
            return JsonResponse({'error': 'No se ha subido ningún archivo'}, status=400)
    except Exception as e:
        # Registra el error y retorna un error interno del servidor
        logger.error(f"Error ocurrido: {e}")
        return JsonResponse({'error': 'Error interno del servidor'}, status=500)