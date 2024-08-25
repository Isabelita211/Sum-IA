import os
from google.oauth2 import service_account
from google.cloud import language_v1
from google.cloud import documentai
from google.api_core.client_options import ClientOptions
from django.db import models
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

# Ruta al archivo de credenciales
credentials_path = 'path/to/credentials.json'

# Autenticar con la API
credentials = service_account.Credentials.from_service_account_file(
    credentials_path, scopes=['https://www.googleapis.com/auth/cloud-language', 'https://www.googleapis.com/auth/cloud-documentai']
)

# Crear clientes para Language y Document AI
language_client = language_v1.LanguageServiceClient(credentials=credentials)
documentai_client = documentai.DocumentUnderstandingServiceClient(credentials=credentials)

# Modelo para almacenar los mensajes
class Mensaje(models.Model):
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

# Vista para procesar el texto
@require_http_methods(["POST"])
def process_text(request):
    texto = request.POST.get("texto")
    document = language_v1.Document(content=texto, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = language_client.analyze_sentiment(request={'document': document})
    sentiment = response.document_sentiment

    # Almacenar el mensaje en la base de datos
    mensaje = Mensaje(texto=texto)
    mensaje.save()

    # Devolver la respuesta en formato JSON
    return JsonResponse({
        "sentiment": sentiment.score,
        "magnitude": sentiment.magnitude
    })

# Vista para conversar
@require_http_methods(["POST"])
def converse(request):
    texto = request.POST.get("texto")
    archivo = request.FILES.get("archivo")

    if archivo:
        # Analizar el archivo con la API de Document AI
        document = documentai.Document.from_json(
            {"content": archivo.read(), "mime_type": archivo.content_type}
        )
        response = documentai_client.annotate_document(request={"document": document})
        entities = response.annotations

        # Procesar las entidades extraídas del archivo
        respuesta = []
        for entity in entities:
            respuesta.append({"texto": entity.text, "tipo": entity.type_})

        return JsonResponse({"respuesta": respuesta})
    else:
        # Si no se envió un archivo, analizar el texto con la API de Language
        document = language_v1.Document(content=texto, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = language_client.analyze_sentiment(request={'document': document})
        sentiment = response.document_sentiment

        return JsonResponse({"respuesta": {"sentiment": sentiment.score, "magnitude": sentiment.magnitude}})

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('converse/', views.converse, name='converse'),
    path('process_text/', views.process_text, name='process_text'),
]