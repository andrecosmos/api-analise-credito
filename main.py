from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import pandas as pd
import io

app = FastAPI(
    title="Sistema de Análise de Risco de Crédito - Corporativo",
    description="API para análise individual e processamento em lote via planilhas.",
    version="1.1.0"
)

# --- FUNÇÃO CENTRAL DE REGRAS (Reutilizável) ---
def calcular_risco_linha(renda, emprestimo, parcelas, inadimplencia):
    valor_parcela = round(emprestimo / parcelas, 2)
    comprometimento = round((valor_parcela / renda) * 100, 2)
    
    if inadimplencia == 1 and comprometimento > 30:
        status = 'Risco Alto (Recusado)'
    elif comprometimento > 30 or inadimplencia == 1:
        status = 'Risco Médio (Análise Manual)'
    else:
        status = 'Risco Baixo (Aprovado)'
        
    return valor_parcela, comprometimento, status


# --- ROTA 1: ANÁLISE INDIVIDUAL (App / Web) ---
class ClienteRequest(BaseModel):
    id_cliente: int = Field(..., example=1001)
    renda_mensal: float = Field(..., example=5500.00)
    valor_emprestimo: float = Field(..., example=25000.00)
    parcelas: int = Field(..., example=36)
    historico_inadimplencia: int = Field(..., example=0)

@app.post("/analizar-credito", tags=["Análise Individual"])
def analisar_credito(cliente: ClienteRequest):
    v_parcela, comp, status = calcular_risco_linha(
        cliente.renda_mensal, cliente.valor_emprestimo, cliente.parcelas, cliente.historico_inadimplencia
    )
    return {
        "id_cliente": cliente.id_cliente,
        "valor_parcela_calculada": v_parcela,
        "comprometimento_renda_percentual": comp,
        "decisao_sistema": status
    }


# --- ROTA 2: PROCESSAMENTO EM LOTE (Mesa de Crédito / Planilha) ---
@app.post("/analisar-lote-planilha", tags=["Processamento em Lote"])
async def analisar_lote_planilha(file: UploadFile = File(...)):
    # Valida a extensão do arquivo enviado
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Por favor, envie apenas arquivos Excel (.xlsx).")
    
    try:
        # Lê o arquivo Excel enviado direto da memória do FastAPI
        conteudo = await file.read()
        df = pd.read_excel(io.BytesIO(conteudo))
        
        # Colunas obrigatórias que a planilha do usuário deve ter
        colunas_esperadas = ['ID_Cliente', 'Renda_Mensal', 'Valor_Emprestimo', 'Parcelas', 'Historico_Inadimplencia']
        if not all(col in df.columns for col in colunas_esperadas):
            raise HTTPException(status_code=400, detail=f"A planilha precisa conter as colunas: {colunas_esperadas}")
        
        # Cria listas para armazenar os novos cálculos calculados linha por linha
        parcelas_calc = []
        comprometimentos = []
        decisoes = []
        
        # Loop processando a planilha do banco
        for _, row in df.iterrows():
            v_p, comp, stat = calcular_risco_linha(
                row['Renda_Mensal'], row['Valor_Emprestimo'], row['Parcelas'], row['Historico_Inadimplencia']
            )
            parcelas_calc.append(v_p)
            comprometimentos.append(comp)
            decisoes.append(stat)
            
        # Adiciona os resultados como novas colunas no DataFrame original
        df['Valor_Parcela_Calculada'] = parcelas_calc
        df['Comprometimento_Renda_%'] = comprometimentos
        df['Decisao_Sistema'] = decisoes
        
        # Prepara a planilha modificada de volta para a memória para fazer o download automático
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Resultados_Credito')
        output.seek(0)
        
        # Retorna o arquivo modificado diretamente pelo navegador
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=resultado_analise_lote.xlsx"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o arquivo: {str(e)}")



