from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Proprietario


# ─────────────────────────────────────────
# TESTES DO MODEL
# ─────────────────────────────────────────

class ProprietarioModelTest(TestCase):

    def setUp(self):
        self.proprietario = Proprietario.objects.create(
            nome_completo="Nicolas Renck",
            telefone="51999999999",
            aceita_troca=False,
            descricao="Proprietário de teste"
        )

    def test_criacao_proprietario(self):
        """Verifica se o proprietário foi criado corretamente"""
        self.assertEqual(self.proprietario.nome_completo, "Nicolas Renck")
        self.assertEqual(self.proprietario.telefone, "51999999999")
        self.assertFalse(self.proprietario.aceita_troca)

    def test_str_retorna_nome(self):
        """Verifica se o __str__ retorna o nome completo"""
        self.assertEqual(str(self.proprietario), "Nicolas Renck")

    def test_descricao_opcional(self):
        """Verifica se proprietário pode ser criado sem descrição"""
        proprietario = Proprietario.objects.create(
            nome_completo="Sem Descricao",
            telefone="51988888888"
        )
        self.assertIsNone(proprietario.descricao)

    def test_aceita_troca_default_false(self):
        """Verifica se aceita_troca começa como False por padrão"""
        proprietario = Proprietario.objects.create(
            nome_completo="Teste Default",
            telefone="51977777777"
        )
        self.assertFalse(proprietario.aceita_troca)

    def test_criado_em_preenchido_automaticamente(self):
        """Verifica se criado_em é preenchido automaticamente"""
        self.assertIsNotNone(self.proprietario.criado_em)


# ─────────────────────────────────────────
# TESTES DA API (ViewSet)
# ─────────────────────────────────────────

class ProprietarioAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Cria usuário e autentica
        self.user = User.objects.create_user(
            username="nicolas",
            password="senha123"
        )
        self.client.force_authenticate(user=self.user)

        # Cria proprietário base pra usar nos testes
        self.proprietario = Proprietario.objects.create(
            nome_completo="Nicolas Renck",
            telefone="51999999999",
            aceita_troca=True
        )

    def test_listar_proprietarios(self):
        """GET /proprietarios/ deve retornar 200"""
        response = self.client.get("/api/proprietarios/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_criar_proprietario(self):
        """POST /proprietarios/ deve criar e retornar 201"""
        data = {
            "nome_completo": "Novo Proprietario",
            "telefone": "51911111111",
            "aceita_troca": False
        }
        response = self.client.post("/api/proprietarios/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["nome_completo"], "Novo Proprietario")

    def test_buscar_proprietario_por_id(self):
        """GET /proprietarios/{id}/ deve retornar o proprietário correto"""
        response = self.client.get(f"/api/proprietarios/{self.proprietario.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nome_completo"], "Nicolas Renck")

    def test_atualizar_proprietario(self):
        """PATCH /proprietarios/{id}/ deve atualizar parcialmente"""
        response = self.client.patch(
            f"/api/proprietarios/{self.proprietario.id}/",
            {"aceita_troca": False}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["aceita_troca"])

    def test_deletar_proprietario(self):
        """DELETE /proprietarios/{id}/ deve retornar 204"""
        response = self.client.delete(f"/api/proprietarios/{self.proprietario.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Proprietario.objects.filter(id=self.proprietario.id).exists())

    def test_acesso_sem_autenticacao(self):
        """Requisição sem token deve retornar 401"""
        client_sem_auth = APIClient()
        response = client_sem_auth.get("/api/proprietarios/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)