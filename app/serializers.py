from rest_framework import serializers
from .models import Proprietario, Imovel, FotoImovel


class ProprietarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proprietario
        fields = '__all__'


class FotoImovelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotoImovel
        fields = ['id', 'foto', 'ordem']


class ImovelSerializer(serializers.ModelSerializer):
    fotos = FotoImovelSerializer(many=True, read_only=True)
    proprietario_nome = serializers.CharField(
        source='proprietario.nome_completo',
        read_only=True
    )

    class Meta:
        model = Imovel
        fields = [
            'id',
            'nome',
            'endereco',
            'preco',
            'metros_quadrados',
            'proprietario',
            'proprietario_nome',
            'status',
            'fotos',
            'criado_em'
        ]