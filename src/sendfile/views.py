from rest_framework import generics, mixins, status, viewsets
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import pagination
from django.conf import settings
from datetime import datetime

from django.shortcuts import render
from django.http import FileResponse
from .serializers import UploadSerializer
from .models import UploadFileAnalisador
import pickle
import os
import io
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def trasnforma_em_binario(file):
    binaryFile = pickle.dumps(file)

    return binaryFile


def send_image(response):
    path = os.path.join(BASE_DIR, 'files/images/image1.jpg')
    img = open(path, 'rb')

    response = FileResponse(img)

    return response


def send_pdf(response):
    path = os.path.join(BASE_DIR, 'files/docs/exemplo1.pdf')
    file = open(path, 'rb')

    response = FileResponse(file)

    return response


def send_scaler(response):
    path = os.path.join(BASE_DIR, 'files/analisadores/testeAIC/scaler_data')
    file = open(path, 'rb')

    response = FileResponse(file)

    return response


def send_modelo(response):
    path = os.path.join(BASE_DIR, 'files/analisadores/testeAIC/modelo.hdf5')
    file = open(path, 'rb')

    response = FileResponse(file)

    return response


class UploadAnalisadoresViewset(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):

    queryset = UploadFileAnalisador.objects.all()
   #  permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = UploadSerializer

    def create(self, request):
        serializer_context = {
            'request': request
        }

        context = {}

        nome = request.data['nome']
        modeloFile = request.data['modelo'].file
        modelodata = modeloFile.read()
        modelo = trasnforma_em_binario(modelodata)
        # modelo = modelodata

        scalerFile = request.data['scaler_data'].file
        scalerdata = scalerFile.read()
        scaler_data = trasnforma_em_binario(scalerdata)
        # scaler_data = scalerdata
        # modelo = ler_arquivo(data['modelo'])
        serializer_data = ({
            'analisador_name': nome,
            'modelo': modelo,
            'scaler_data': scaler_data
        })

        serializer = self.serializer_class(
            data=serializer_data,
            context=serializer_context
        )

        analisador_name = request.data['nome']

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk):
        requestedFile = self.request.query_params.get('file', None)
        requestedTag = self.request.query_params.get('tag', None)
        serializer_context = {'request': request}

        try:
            serializer_instance = self.queryset.get(analisador_name=pk)
            # serializer_instance = self.queryset.get(pk=pk)
        except UploadFileAnalisador.DoesNotExist:
            raise NotFound('UploadFile não existe na Base de Dados.')

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context
        )

        responseFile = None
        filename = None
        if requestedFile is not None:
            if requestedFile == 'scaler':
                file = pickle.loads(serializer_instance.scaler_data)
                responseFile = io.BufferedReader(io.BytesIO(file))
                filename = 'scaler_data'
            if requestedFile == 'modelo':
                file = pickle.loads(serializer_instance.modelo)
                responseFile = io.BufferedReader(io.BytesIO(file))
                filename = 'modelo.hdf5'

        if responseFile is not None and filename is not None:
            response = FileResponse(responseFile)
            response.as_attachment = False
            response.filename = filename
            response.set_headers({'content_type':'application/octet-stream'})
            return response
        else:
            return NotFound()    
 
        # return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        serializer_context = {'request': request}

        arquivos_atualizados = []

        try:
            serializer_instance = self.queryset.get(pk=pk)
        except AnalisadorConfiguracao.DoesNotExist:
            raise NotFound('Analisador não existe na Base de Dados.')

        if request.data['modelo'] is not '':
            modelo = trasnforma_em_binario(request.data['modelo'])
        else:
            modelo = serializer_instance.modelo

        if request.data['scaler_data'] is not '':
            scaler_data = trasnforma_em_binario(request.data['scaler_data'])
        else:
            scaler_data = serializer_instance.scaler_data

        serializer_data = ({
            'analisador_name': serializer_instance.analisador_name,
            'modelo': modelo,
            'scaler_data': scaler_data
        })

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context,
            data=serializer_data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(f"O analisador {serializer.data['analisador_name']} foi atualizado.", status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            serializer_instance = self.queryset.get(pk=pk)
        except:
            return Response('O id do analisador informado não existe.', status=status.HTTP_404_NOT_FOUND)

        serializer_instance.delete()

        return Response('Os arquivos do analisador foram deletados com sucesso.', status=status.HTTP_200_OK)
