from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Proprietario, Imovel, FotoImovel
from .serializers import ProprietarioSerializer, ImovelSerializer, FotoImovelSerializer
from .sheets import append_imovel_to_sheet, remove_imovel_from_sheet


class ProprietarioViewSet(viewsets.ModelViewSet):
    queryset = Proprietario.objects.all()
    serializer_class = ProprietarioSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nome_completo', 'telefone']
    ordering_fields = ['nome_completo', 'criado_em']


class ImovelViewSet(viewsets.ModelViewSet):
    queryset = Imovel.objects.all()
    serializer_class = ImovelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'proprietario']
    search_fields = ['nome', 'endereco']
    ordering_fields = ['preco', 'criado_em', 'metros_quadrados']

    def perform_create(self, serializer):
        imovel = serializer.save()
        append_imovel_to_sheet(imovel)


    def perform_destroy(self, instance):
        imovel_id = instance.id  
        instance.delete()         # Deleta do banco de dados local 
        remove_imovel_from_sheet(imovel_id)  # Remove da planilha do Google


class FotoImovelViewSet(viewsets.ModelViewSet):
    serializer_class = FotoImovelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FotoImovel.objects.filter(imovel=self.kwargs['imovel_pk'])

    def perform_create(self, serializer):
        imovel = Imovel.objects.get(pk=self.kwargs['imovel_pk'])
        serializer.save(imovel=imovel)