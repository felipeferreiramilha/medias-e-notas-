import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Sistema de Gestão Escolar - Notas",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Sistema de Gestão Escolar e Lançamento de Notas")
st.markdown("Gerencie turmas, cadastre alunos, lance três notas e acompanhe as médias e situações escolares em tempo real.")

# Inicializando a base de dados no estado da sessão do Streamlit
if "dados_escolares" not in st.session_state:
    # Exemplo inicial de dados
    st.session_state.dados_escolares = [
        {"Turma": "1º Ano A", "Nome": "Ana Silva", "Nota1": 8.0, "Nota2": 7.5, "Nota3": 9.0},
        {"Turma": "1º Ano A", "Nome": "Carlos Souza", "Nota1": 5.0, "Nota2": 6.0, "Nota3": 4.5},
        {"Turma": "2º Ano B", "Nome": "Mariana Lima", "Nota1": 9.5, "Nota2": 8.0, "Nota3": 9.0},
    ]

# Criando as Abas de Navegação do Sistema
aba1, aba2, aba3 = st.tabs(["📝 Lançar Notas / Alunos", "📊 Relatório de Turmas", "⚙️ Gerenciar Turmas"])

# --- ABA 1: LANÇAR NOTAS E ALUNOS ---
with aba1:
    st.header("Cadastro de Alunos e Lançamento de Notas")
    
    # Lista de turmas cadastradas (padrão ou criadas)
    if "turmas_cadastradas" not in st.session_state:
        st.session_state.turmas_cadastradas = ["1º Ano A", "1º Ano B", "2º Ano A", "2º Ano B", "3º Ano A"]

    with st.form("form_aluno", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            turma_escolhida = st.selectbox("Selecione a Turma", st.session_state.turmas_cadastradas)
            nome_aluno = st.text_input("Nome Completo do Aluno")
        with col2:
            nota_1 = st.number_input("Nota 1 (0 a 10)", min_value=0.0, max_value=10.0, step=0.1)
            nota_2 = st.number_input("Nota 2 (0 a 10)", min_value=0.0, max_value=10.0, step=0.1)
            nota_3 = st.number_input("Nota 3 (0 a 10)", min_value=0.0, max_value=10.0, step=0.1)
            
        salvar_btn = st.form_submit_button("Salvar Aluno e Notas")
        
        if salvar_btn:
            if nome_aluno.strip() != "":
                st.session_state.dados_escolares.append({
                    "Turma": turma_escolhida,
                    "Nome": nome_aluno,
                    "Nota1": nota_1,
                    "Nota2": nota_2,
                    "Nota3": nota_3
                })
                st.success(f"Aluno {nome_aluno} cadastrado com sucesso na turma {turma_escolhida}!")
            else:
                st.error("Por favor, digite o nome do aluno.")

# --- ABA 2: RELATÓRIO DE TURMAS E MÉDIAS ---
with aba2:
    st.header("Relatório de Desempenho e Médias")
    
    if len(st.session_state.dados_escolares) > 0:
        # Convertendo para DataFrame do Pandas para calcular as médias
        df = pd.DataFrame(st.session_state.dados_escolares)
        
        # Calculando a média das 3 notas
        df["Média"] = (df["Nota1"] + df["Nota2"] + df["Nota3"]) / 3
        df["Média"] = df["Média"].round(2)
        
        # Definindo a situação do aluno (Média >= 7.0 Aprovado, 4 a 6.9 Recuperação, < 4 Reprovado)
        def definir_situacao(media):
            if media >= 7.0:
                return "✅ Aprovado"
            elif media >= 4.0:
                return "⚠️ Recuperação"
            else:
                return "❌ Reprovado"
                
        df["Situação"] = df["Média"].apply(definir_situacao)
        
        # Filtro por Turma na tela
        filtro_turma = st.selectbox("Filtrar visualização por Turma:", ["Todas as Turmas"] + list(st.session_state.turmas_cadastradas))
        
        if filtro_turma != "Todas as Turmas":
            df_filtrado = df[df["Turma"] == filtro_turma]
        else:
            df_filtrado = df
            
        # Exibindo a tabela formatada
        st.dataframe(df_filtrado, use_container_width=True)
        
        # Estatísticas rápidas da turma selecionada
        st.markdown("### 📈 Estatísticas Rápidas")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Total de Alunos Exibidos", len(df_filtrado))
        with col_m2:
            if len(df_filtrado) > 0:
                media_geral = df_filtrado["Média"].mean()
                st.metric("Média Geral da Turma", f"{media_geral:.2f}")
    else:
        st.info("Nenhum aluno cadastrado ainda. Utilize a aba 'Lançar Notas / Alunos' para começar.")

# --- ABA 3: GERENCIAR TURMAS ---
with aba3:
    st.header("Gerenciamento de Turmas")
    st.markdown("Adicione novas turmas ao sistema caso precise.")
    
    nova_turma = st.text_input("Nome da Nova Turma (ex: 3º Ano B)")
    if st.button("Adicionar Turma"):
        if nova_turma and nova_turma not in st.session_state.turmas_cadastradas:
            st.session_state.turmas_cadastradas.append(nova_turma)
            st.success(f"Turma '{nova_turma}' adicionada com sucesso!")
        else:
            st.error("Digite um nome válido ou uma turma que já não exista.")
            
    st.write("### Turmas Ativas no Sistema:")
    for t in st.session_state.turmas_cadastradas:
        st.write(f"- 🏫 {t}")

# Rodapé
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Sistema Escolar Automatizado 📚</p>", unsafe_allow_html=True)
