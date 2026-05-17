from django.db import models


class Proprietario(models.Model):
    nome_completo = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    aceita_troca = models.BooleanField(default=False)
    descricao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_completo





class Imovel(models.Model):
    STATUS_CHOICES = [
        ('a_venda', 'À Venda'),
        ('suspenso', 'Suspenso'),
        ('vendido', 'Vendido'),
    ]

    nome = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits=12, decimal_places=2)
    metros_quadrados = models.DecimalField(max_digits=8, decimal_places=2)
    proprietario = models.ForeignKey(
        Proprietario,
        on_delete=models.PROTECT,
        related_name='imoveis'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='a_venda'
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome




class FotoImovel(models.Model):
    imovel = models.ForeignKey(
        Imovel,
        on_delete=models.CASCADE,
        related_name='fotos'
    )
    foto = models.URLField(max_length=500)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return f"Foto {self.ordem} - {self.imovel.nome}"




