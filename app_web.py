import streamlit as st
import requests
import pandas as pd
import io
import os


# Configuração da página do painel bancário
st.set_page_config(page_title="Portal de Crédito - Banco Digital", page_icon="🏦", layout="wide")

st.title("🏦 Portal Interno de Concessão de Crédito")
st.markdown("Interface corporativa para simulação individual e processamento de propostas em lote.")

# URL da nossa API FastAPI rodando em segundo plano

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")

# Criação de duas abas na tela para organizar a apresentação
aba_individual, aba_lote = st.tabs(["📄 Análise Individual", "📊 Processamento em Lote (Planilha)"])

# --- ABA 1: ANÁLISE INDIVIDUAL ---
with aba_individual:
    st.subheader("Simulação de Crédito em Tempo Real")
    
    # Formulário estruturado com os dados de entrada
    with st.form("form_cliente"):
        col1, col2 = st.columns(2)
        with col1:
            id_cliente = st.number_input("ID do Cliente", min_value=1000, max_value=9999, value=1001)
            renda = st.number_input("Renda Mensal (R$)", min_value=1000.0, value=5500.0, step=500.0)
            inadimplente = st.selectbox("Histórico de Inadimplência", options=[0, 1], format_func=lambda x: "Bom Pagador" if x == 0 else "Histórico Ruim / Restrição")
        with col2:
            valor_emprestimo = st.number_input("Valor do Empréstimo Solicitado (R$)", min_value=1000.0, value=25000.0, step=1000.0)
            parcelas = st.selectbox("Quantidade de Parcelas", options=[12, 24, 36, 48, 60], index=2)
            
        botao_enviar = st.form_submit_button("Avaliar Crédito")
        
    if botao_enviar:
        # Monta o payload exatamente como o FastAPI espera
        payload = {
            "id_cliente": id_cliente,
            "renda_mensal": renda,
            "valor_emprestimo": valor_emprestimo,
            "parcelas": parcelas,
            "historico_inadimplencia": inadimplente
        }
        
        try:
            # Consome o endpoint individual da API
            resposta = requests.post(f"{API_URL}/analizar-credito", json=payload)
            if resposta.status_code == 200:
                res_dados = resposta.json()
                
                # Exibe caixas de destaque coloridas com base na decisão do motor
                status = res_dados["decisao_sistema"]
                if "Aprovado" in status:
                    st.success(f"🎉 **{status}**")
                elif "Manual" in status:
                    st.warning(f"⚠️ **{status}**")
                else:
                    st.error(f"❌ **{status}**")
                    
                # Exibe métricas financeiras na tela
                m1, m2 = st.columns(2)
                m1.metric("Valor da Parcela", f"R$ {res_dados['valor_parcela_calculada']:.2f}")
                m2.metric("Comprometimento de Renda", f"{res_dados['comprometimento_renda_percentual']}%")
            else:
                st.error("Erro na comunicação com o motor de crédito.")
        except Exception as e:
            st.error(f"Certifique-se de que a API FastAPI está ligada! Erro: {e}")

# --- ABA 2: PROCESSAMENTO EM LOTE ---
with aba_lote:
    st.subheader("Mesa de Análise - Upload de Propostas")
    st.markdown("Arraste a planilha de simulação de clientes gerada pelo sistema para processar as decisões em lote.")
    
    # Campo para upload do arquivo excel
    arquivo_enviado = st.file_saver = st.file_uploader("Selecione a planilha (.xlsx)", type=["xlsx"])
    
    if arquivo_enviado is not None:
        if st.button("Processar Carteira de Clientes"):
            try:
                # Prepara o arquivo para envio via requisição multipart/form-data
                arquivos = {"file": (arquivo_enviado.name, arquivo_enviado.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
                
                with st.spinner("O motor de crédito está processando o lote..."):
                    resposta_lote = requests.post(f"{API_URL}/analisar-lote-planilha", files=arquivos)
                    
                if resposta_lote.status_code == 200:
                    st.success("Planilha processada com sucesso pelo robô financeiro!")
                    
                    # Carrega os bytes retornados para exibição e download direto na tela
                    df_resultado = pd.read_excel(io.BytesIO(resposta_lote.content))
                    
                    # Exibe uma prévia dos dados calculados diretamente na interface gráfica
                    st.dataframe(df_resultado.head(10), use_container_width=True)
                    
                    # Botão para baixar o resultado final modificado
                    st.download_button(
                        label="📥 Baixar Planilha Processada (Resultados)",
                        data=resposta_lote.content,
                        file_name="resultado_bancario_lote.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.error("A API retornou um erro ao processar o arquivo. Verifique a formatação das colunas.")
            except Exception as e:
                st.error(f"Erro ao conectar ao servidor back-end: {e}")
