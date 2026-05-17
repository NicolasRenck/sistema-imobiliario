import gspread
from google.oauth2.service_account import Credentials
from django.conf import settings

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def get_sheets_client():
    creds = Credentials.from_service_account_file(
        settings.GOOGLE_CREDENTIALS_PATH,
        scopes=SCOPES
    )
    return gspread.authorize(creds)

def append_imovel_to_sheet(imovel):
    client = get_sheets_client()
    sheet = client.open_by_key(settings.GOOGLE_SHEET_ID).sheet1
    
    # Adicionamos o str(imovel.id) como o primeiro elemento da lista
    sheet.append_row([
        str(imovel.id),  # <-- ID único salvo na Coluna A
        imovel.nome,
        imovel.endereco,
        str(imovel.preco),
        str(imovel.metros_quadrados),
        imovel.proprietario.nome_completo,
        imovel.get_status_display(),
        imovel.criado_em.strftime('%d/%m/%Y %H:%M')
    ])

def remove_imovel_from_sheet(imovel_id):
    """
    Busca o ID do imóvel estritamente na primeira coluna (A) 
    e remove a linha inteira correspondente.
    """
    client = get_sheets_client()
    sheet = client.open_by_key(settings.GOOGLE_SHEET_ID).sheet1
    
    try:
        # Procuramos o ID do imóvel apenas na coluna 1 (Coluna A)
        # Isso evita que um preço ou metragem idêntica ao ID quebre a lógica
        celula = sheet.find(str(imovel_id), in_column=1)
        
        if celula:
            # gspread deleta a linha física e sobe as de baixo automaticamente
            sheet.delete_rows(celula.row)
            print(f"Imóvel {imovel_id} removido com sucesso da linha {celula.row}.")
            
    except gspread.exceptions.CellNotFound:
        # Caso o imóvel não esteja na planilha por algum motivo, o sistema não quebra
        print(f"Imóvel {imovel_id} não foi localizado na planilha do Google.")