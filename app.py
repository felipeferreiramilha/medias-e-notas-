import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Sistema de Gestão Escolar",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Sistema de Gestão Escolar - Notas, Professores e Disciplinas")
st.markdown("Gerencie turmas, professores, disciplinas, cadastre notas e acompanhe o desempenho em tempo real.")

# Inicializando o estado da sessão (Session State)
if "dados_escolares" not in st.session_state:
    st.session_state.dados_escolares = [
        {"Turma": "1º Ano A", "Disciplina": "Física", "Professor": "Prof. Carlos", "Nome": "Ana Silva", "Nota1": 8.0, "Nota2": 7.5, "Nota3": 9.0},
        {"Turma": "1º Ano A", "Disciplina": "Física", "Professor": "Prof. Carlos", "Nome": "Carlos Souza", "Nota1": 5.0, "Nota2": 6.0, "Nota3": 4.5},
        {"Turma": "2º Ano B", "Disciplina": "Matemática", "Professor": "Profª Maria", "Nome": "Mariana Lima", "Nota1": 9.5, "Nota2": 8.0, "Nota3": 9.0},
    ]

if "turmas_cadastradas" not in st.session_state:
    st.session_state.turmas_cadastradas = ["1º Ano A", "1º Ano B", "2º Ano A", "2º Ano B", "3º Ano A"]

if "disciplinas_cadastradas" not in st.session_state:
    st.session_state.disciplinas_cadastradas = ["Física", "Matemática", "Química", "Biologia", "Português", "História"]

if "professores_cadastrados" not in st.session_state:
    st.session_state.professores_cadastrados = ["Prof. Carlos", "Profª Maria", "Prof. João", "Profª Ana"]

# Criando as Abas de Navegação do Sistema
aba1, aba2, aba3, aba4 = st.tabs([
    "📝 Lançar Notas / Alunos", 
    "📊 Relatório e Médias", 
    "✏️ Editar / Excluir Alunos", 
    "⚙️ Gerenciar Turmas, Profs e Disciplinas"
])

# --- ABA 1: LANÇAR NOTAS E ALUNOS ---
with aba1:
    st.header("Cadastro de Alunos e Lançamento de Notas")
    
    with st.form("form_aluno", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            turma_escolhida = st.selectbox("Selecione a Turma", st.session_state.turmas_cadastradas)
            disciplina_escolhida = st.selectbox("Selecione a Disciplina", st.session_state.disciplinas_cadastradas)
            professor_escolhido = st.selectbox("Professor Responsável", st.session_state.professores_cadastrados)
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
                    "Disciplina": disciplina_escolhida,
                    "Professor": professor_escolhido,
                    "Nome": nome_aluno,
                    "Nota1": nota_1,
                    "Nota2": nota_2,
                    "Nota3": nota_3
                })
                st.success(f"Notas do(a) aluno(a) {nome_aluno} lançadas com sucesso em {disciplina_escolhida}!")
            else:
                st.error("Por favor, digite o nome do aluno.")

# --- ABA 2: RELATÓRIO DE TURMAS E MÉDIAS ---
with aba2:
    st.header("Relatório de Desempenho e Médias")
    
    if len(st.session_state.dados_escolares) > 0:
        df = pd.DataFrame(st.session_state.dados_escolares)
        
        # Calculando a média das 3 notas
        df["Média"] = (df["Nota1"] + df["Nota2"] + df["Nota3"]) / 3
        df["Média"] = df["Média"].round(2)
        
        def definir_situacao(media):
            if media >= 7.0:
                return "✅ Aprovado"
            elif media >= 4.0:
                return "⚠️ Recuperação"
            else:
                return "❌ Reprovado"
                
        df["Situação"] = df["Média"].apply(definir_situacao)
        
        # Filtros na tela
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            filtro_turma = st.selectbox("Filtrar por Turma:", ["Todas as Turmas"] + list(st.session_state.turmas_cadastradas))
        with col_f2:
            filtro_disc = st.selectbox("Filtrar por Disciplina:", ["Todas as Disciplinas"] + list(st.session_state.disciplinas_cadastradas))
        
        df_filtrado = df.copy()
        if filtro_turma != "Todas as Turmas":
            df_filtrado = df_filtrado[df_filtrado["Turma"] == filtro_turma]
        if filtro_disc != "Todas as Disciplinas":
            df_filtrado = df_filtrado[df_filtrado["Disciplina"] == filtro_disc]
            
        st.dataframe(df_filtrado, use_container_width=True)
        
        st.markdown("### 📈 Estatísticas Rápidas")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Total de Registros Exibidos", len(df_filtrado))
        with col_m2:
            if len(df_filtrado) > 0:
                media_geral = df_filtrado["Média"].mean()
                st.metric("Média Geral do Filtro", f"{media_geral:.2f}")
    else:
        st.info("Nenhum aluno cadastrado ainda.")

# --- ABA 3: EDITAR OU EXCLUIR ALUNOS ---
with aba3:
    st.header("Editar Notas ou Excluir Alunos")
    st.markdown("Selecione um registro de aluno para alterar as notas, disciplina ou removê-lo.")
    
    if len(st.session_state.dados_escolares) > 0:
        lista_nomes = [f"{item['Nome']} - {item['Turma']} ({item['Disciplina']})" for item in st.session_state.dados_escolares]
        aluno_selecionado_str = st.selectbox("Selecione o Aluno/Registro", lista_nomes)
        
        indice_selecionado = lista_nomes.index(aluno_selecionado_str)
        aluno_atual = st.session_state.dados_escolares[indice_selecionado]
        
        with st.form("form_edicao"):
            st.subheader(f"Editando: {aluno_atual['Nome']}")
            
            nova_turma = st.selectbox(
                "Alterar Turma", 
                st.session_state.turmas_cadastradas, 
                index=st.session_state.turmas_cadastradas.index(aluno_atual["Turma"]) if aluno_atual["Turma"] in st.session_state.turmas_cadastradas else 0
            )
            nova_disc = st.selectbox(
                "Alterar Disciplina", 
                st.session_state.disciplinas_cadastradas, 
                index=st.session_state.disciplinas_cadastradas.index(aluno_atual["Disciplina"]) if aluno_atual["Disciplina"] in st.session_state.disciplinas_cadastradas else 0
            )
            novo_prof = st.selectbox(
                "Alterar Professor", 
                st.session_state.professores_cadastrados, 
                index=st.session_state.professores_cadastrados.index(aluno_atual["Professor"]) if aluno_atual["Professor"] in st.session_state.professores_cadastrados else 0
            )
            novo_nome = st.text_input("Alterar Nome do Aluno", value=aluno_atual["Nome"])
            
            col_e1, col_e2, col_e3 = st.columns(3)
            with col_e1:
                nova_n1 = st.number_input("Nota 1", min_value=0.0, max_value=10.0, step=0.1, value=float(aluno_atual["Nota1"]))
            with col_e2:
                nova_n2 = st.number_input("Nota 2", min_value=0.0, max_value=10.0, step=0.1, value=float(aluno_atual["Nota2"]))
            with col_e3:
                nova_n3 = st.number_input("Nota 3", min_value=0.0, max_value=10.0, step=0.1, value=float(aluno_atual["Nota3"]))
            
            atualizar_btn = st.form_submit_button("Salvar Alterações")
            
            if atualizar_btn:
                st.session_state.dados_escolares[indice_selecionado] = {
                    "Turma": nova_turma,
                    "Disciplina": nova_disc,
                    "Professor": novo_prof,
                    "Nome": novo_nome,
                    "Nota1": nova_n1,
                    "Nota2": nova_n2,
                    "Nota3": nova_n3
                }
                st.success("Dados atualizados com sucesso!")
        
        st.markdown("---")
        if st.button("❌ Excluir Este Registro", type="primary"):
            removido = st.session_state.dados_escolares.pop(indice_selecionado)
            st.success(f"Registro de {removido['Nome']} removido com sucesso!")
            st.rerun()
    else:
        st.info("Não há registros para editar.")

# --- ABA 4: GERENCIAR TURMAS, PROFESSORES E DISCIPLINAS ---
with aba4:
    st.header("Gerenciamento Geral")
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.subheader("🏫 Turmas")
        nova_turma = st.text_input("Nova Turma (ex: 3º Ano B)")
        if st.button("Adicionar Turma"):
            if nova_turma and nova_turma not in st.session_state.turmas_cadastradas:
                st.session_state.turmas_cadastradas.append(nova_turma)
                st.success(f"Turma '{nova_turma}' adicionada!")
            else:
                st.error("Nome inválido ou já cadastrado.")
        st.write("**Ativas:**", ", ".join(st.session_state.turmas_cadastradas))
        
        st.markdown("---")
        st.subheader("📚 Disciplinas")
        nova_disc = st.text_input("Nova Disciplina (ex: Filosofia)")
        if st.button("Adicionar Disciplina"):
            if nova_disc and nova_disc not in st.session_state.disciplinas_cadastradas:
                st.session_state.disciplinas_cadastradas.append(nova_disc)
                st.success(f"Disciplina '{nova_disc}' adicionada!")
            else:
                st.error("Nome inválido ou já cadastrado.")
        st.write("**Ativas:**", ", ".join(st.session_state.disciplinas_cadastradas))

    with col_g2:
        st.subheader("👨‍🏫 Professores")
        novo_prof = st.text_input("Nome do Professor (ex: Prof. Marcos)")
        if st.button("Adicionar Professor"):
            if novo_prof and novo_prof not in st.session_state.professores_cadastradas:
                st.session_state.professores_cadastrados.append(novo_prof)
                st.success(f"Professor '{novo_prof}' adicionado!")
            else:
                st.error("Nome inválido ou já cadastrado.")
        st.write("**Cadastrados:**", ", ".join(st.session_state.professores_cadastrados))

    st.markdown("---")
    st.subheader("⚠️ Zona de Perigo (Reset Total)")
    if st.button("🗑️ Limpar Todos os Dados do Sistema"):
        st.session_state.dados_escolares = []
        st.success("Dados limpos com sucesso!")
        st.rerun()

# Rodapé
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Sistema Escolar Automatizado 📚</p>", unsafe_allow_html=True)
    
