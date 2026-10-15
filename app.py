import streamlit as st
import pandas as pd
from datetime import date
import io

# Importando ReportLab para geração de PDFs
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Configuração da página
st.set_page_config(
    page_title="Sistema de Gestão Escolar 2027",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Sistema de Gestão Escolar - Notas, Chamada e Boletim PDF (2027)")
st.markdown("Gerencie turmas, professores, disciplinas, controle frequências para o ano letivo de 2027 e gere boletins em PDF.")

# --- INICIALIZAÇÃO DE DADOS NA SESSÃO ---
if "dados_escolares" not in st.session_state:
    st.session_state.dados_escolares = [
        {"Turma": "1º Ano A", "Disciplina": "Física", "Professor": "Prof. Carlos", "Nome": "Ana Silva", "Nota1": 8.0, "Nota2": 7.5, "Nota3": 9.0},
        {"Turma": "1º Ano A", "Disciplina": "Física", "Professor": "Prof. Carlos", "Nome": "Carlos Souza", "Nota1": 5.0, "Nota2": 6.0, "Nota3": 4.5},
        {"Turma": "2º Ano B", "Disciplina": "Matemática", "Professor": "Profª Maria", "Nome": "Mariana Lima", "Nota1": 9.5, "Nota2": 8.0, "Nota3": 9.0},
    ]

if "registro_chamada" not in st.session_state:
    # Exemplo inicial de registro de chamadas para 2027
    st.session_state.registro_chamada = [
        {"Data": "2027-02-10", "Turma": "1º Ano A", "Nome": "Ana Silva", "Status": "Presente"},
        {"Data": "2027-02-10", "Turma": "1º Ano A", "Nome": "Carlos Souza", "Status": "Falta"},
    ]

if "turmas_cadastradas" not in st.session_state:
    st.session_state.turmas_cadastradas = ["1º Ano A", "1º Ano B", "2º Ano A", "2º Ano B", "3º Ano A"]

if "disciplinas_cadastradas" not in st.session_state:
    st.session_state.disciplinas_cadastradas = ["Física", "Matemática", "Química", "Biologia", "Português", "História"]

if "professores_cadastrados" not in st.session_state:
    st.session_state.professores_cadastrados = ["Prof. Carlos", "Profª Maria", "Prof. João", "Profª Ana"]


# --- FUNÇÃO PARA GERAR BOLETIM EM PDF ---
def gerar_boletim_pdf(nome_aluno, turma_aluno, df_aluno_notas, faltas_aluno):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    styles = getSampleStyleSheet()

    # Título do Boletim
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=1, # Centralizado
        spaceAfter=15,
        textColor=colors.HexColor('#1E3A8A')
    )
    story.append(Paragraph("<b>BOLETIM ESCOLAR - ANO LETIVO 2027</b>", title_style))
    story.append(Spacer(1, 10))

    # Cabeçalho com Informações do Aluno
    info_text = f"<b>Aluno(a):</b> {nome_aluno}<br/><b>Turma:</b> {turma_aluno}<br/><b>Total de Faltas Registradas (2027):</b> {faltas_aluno}"
    story.append(Paragraph(info_text, styles['Normal']))
    story.append(Spacer(1, 15))

    # Tabela de Notas por Disciplina
    data_tabela = [["Disciplina", "Professor", "Nota 1", "Nota 2", "Nota 3", "Média", "Situação"]]
    
    for idx, row in df_aluno_notas.iterrows():
        data_tabela.append([
            row["Disciplina"],
            row["Professor"],
            str(row["Nota1"]),
            str(row["Nota2"]),
            str(row["Nota3"]),
            str(row["Média"]),
            row["Situação"]
        ])

    tabela = Table(data_tabela, colWidths=[110, 110, 50, 50, 50, 50, 100])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F3F4F6')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    
    story.append(tabela)
    story.append(Spacer(1, 30))
    story.append(Paragraph("____________________________________________", ParagraphStyle('Sign', alignment=1)))
    story.append(Paragraph("Assinatura da Direção / Coordenação", ParagraphStyle('SignSub', alignment=1, fontSize=9)))

    doc.build(story)
    buffer.seek(0)
    return buffer


# --- ABAS DE NAVEGAÇÃO ---
aba1, aba2, aba3, aba4, aba5 = st.tabs([
    "📝 Lançar Notas", 
    "📅 Chamada (Ano 2027)", 
    "📄 Boletim & Relatórios PDF", 
    "✏️ Editar / Excluir Alunos", 
    "⚙️ Gerenciar Turmas/Profs/Disciplinas"
])


# --- ABA 1: LANÇAR NOTAS ---
with aba1:
    st.header("Cadastro de Alunos e Lançamento de Notas")
    
    if len(st.session_state.turmas_cadastradas) == 0 or len(st.session_state.disciplinas_cadastradas) == 0:
        st.warning("⚠️ Cadastre ao menos uma Turma e uma Disciplina na aba de Configurações.")
    else:
        with st.form("form_aluno", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                turma_escolhida = st.selectbox("Selecione a Turma", st.session_state.turmas_cadastradas)
                disciplina_escolhida = st.selectbox("Selecione a Disciplina", st.session_state.disciplinas_cadastradas)
                lista_profs = st.session_state.professores_cadastrados if len(st.session_state.professores_cadastrados) > 0 else ["Nenhum Professor"]
                professor_escolhido = st.selectbox("Professor Responsável", lista_profs)
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
                        "Nome": nome_aluno.strip(),
                        "Nota1": nota_1,
                        "Nota2": nota_2,
                        "Nota3": nota_3
                    })
                    st.success(f"Notas do(a) aluno(a) {nome_aluno} salvas com sucesso!")
                else:
                    st.error("Por favor, digite o nome do aluno.")


# --- ABA 2: DIÁRIO DE FREQUÊNCIA / CHAMADA 2027 ---
with aba2:
    st.header("📅 Diário de Classe - Chamada e Frequência (2027)")
    st.markdown("Realize e acompanhe as chamadas de presença para todo o ano de **2027**.")

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        turma_chamada = st.selectbox("Selecione a Turma para Fazer a Chamada:", st.session_state.turmas_cadastradas, key="chamada_turma")
    with col_c2:
        data_chamada = st.date_input("Data da Aula (Ano 2027):", value=date(2027, 2, 1))

    # Buscar alunos cadastrados nessa turma
    alunos_na_turma = sorted(list(set([a["Nome"] for a in st.session_state.dados_escolares if a["Turma"] == turma_chamada])))

    if len(alunos_na_turma) > 0:
        st.subheader(f"Lista de Alunos - {turma_chamada} ({data_chamada.strftime('%d/%m/%Y')})")
        
        with st.form("form_chamada"):
            status_alunos = {}
            for aluno in alunos_na_turma:
                col_a1, col_a2 = st.columns([3, 2])
                with col_a1:
                    st.write(f"👤 **{aluno}**")
                with col_a2:
                    status_alunos[aluno] = st.radio(
                        "Presença", 
                        ["Presente", "Falta"], 
                        key=f"status_{aluno}_{data_chamada}", 
                        horizontal=True
                    )
            
            salvar_chamada_btn = st.form_submit_button("💾 Salvar Chamada do Dia")
            
            if salvar_chamada_btn:
                for aluno, status in status_alunos.items():
                    st.session_state.registro_chamada.append({
                        "Data": str(data_chamada),
                        "Turma": turma_chamada,
                        "Nome": aluno,
                        "Status": status
                    })
                st.success("Chamada salva com sucesso para o ano de 2027!")
    else:
        st.info("Nenhum aluno cadastrado nesta turma ainda.")

    st.markdown("---")
    st.subheader("📊 Histórico de Chamadas Lançadas")
    if len(st.session_state.registro_chamada) > 0:
        df_chamada = pd.DataFrame(st.session_state.registro_chamada)
        st.dataframe(df_chamada[df_chamada["Turma"] == turma_chamada], use_container_width=True)
    else:
        st.write("Nenhuma chamada registrada.")


# --- ABA 3: RELATÓRIOS E GERADOR DE BOLETIM PDF ---
with aba3:
    st.header("📄 Relatório de Desempenho e Emissão de Boletim em PDF")
    
    if len(st.session_state.dados_escolares) > 0:
        df = pd.DataFrame(st.session_state.dados_escolares)
        df["Média"] = ((df["Nota1"] + df["Nota2"] + df["Nota3"]) / 3).round(2)
        
        def definir_situacao(media):
            if media >= 7.0:
                return "✅ Aprovado"
            elif media >= 4.0:
                return "⚠️ Recuperação"
            else:
                return "❌ Reprovado"
                
        df["Situação"] = df["Média"].apply(definir_situacao)

        # Filtros
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            filtro_turma = st.selectbox("Filtrar Tabela por Turma:", ["Todas as Turmas"] + list(st.session_state.turmas_cadastradas))
        with col_f2:
            filtro_disc = st.selectbox("Filtrar Tabela por Disciplina:", ["Todas as Disciplinas"] + list(st.session_state.disciplinas_cadastradas))
        
        df_filtrado = df.copy()
        if filtro_turma != "Todas as Turmas":
            df_filtrado = df_filtrado[df_filtrado["Turma"] == filtro_turma]
        if filtro_disc != "Todas as Disciplinas":
            df_filtrado = df_filtrado[df_filtrado["Disciplina"] == filtro_disc]
            
        st.dataframe(df_filtrado, use_container_width=True)

        st.markdown("---")
        st.subheader("📥 Gerar e Baixar Boletim Individual (PDF)")
        
        todos_alunos = sorted(list(set(df["Nome"].tolist())))
        aluno_boletim = st.selectbox("Selecione o Aluno para Emitir o Boletim:", todos_alunos)
        
        if aluno_boletim:
            df_aluno = df[df["Nome"] == aluno_boletim]
            turma_aluno = df_aluno["Turma"].iloc[0]
            
            # Calcular Faltas do Aluno em 2027
            df_chamada_all = pd.DataFrame(st.session_state.registro_chamada) if len(st.session_state.registro_chamada) > 0 else pd.DataFrame(columns=["Nome", "Status"])
            faltas_totais = len(df_chamada_all[(df_chamada_all["Nome"] == aluno_boletim) & (df_chamada_all["Status"] == "Falta")])
            
            pdf_bytes = gerar_boletim_pdf(aluno_boletim, turma_aluno, df_aluno, faltas_totais)
            
            st.download_button(
                label=f"📄 Baixar Boletim de {aluno_boletim} (PDF)",
                data=pdf_bytes,
                file_name=f"Boletim_2027_{aluno_boletim.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
    else:
        st.info("Nenhum dado cadastrado para gerar relatórios.")


# --- ABA 4: EDITAR OU EXCLUIR ALUNOS ---
with aba3:
    pass # Reuso da estrutura já embutida nas abas


# --- ABA 4 (EDITAR E EXCLUIR REGISTROS) ---
with aba4:
    st.header("Editar Notas ou Excluir Alunos")
    
    if len(st.session_state.dados_escolares) > 0:
        lista_nomes = [f"{item['Nome']} - {item['Turma']} ({item['Disciplina']})" for item in st.session_state.dados_escolares]
        aluno_selecionado_str = st.selectbox("Selecione o Registro", lista_nomes)
        
        indice_selecionado = lista_nomes.index(aluno_selecionado_str)
        aluno_atual = st.session_state.dados_escolares[indice_selecionado]
        
        with st.form("form_edicao"):
            st.subheader(f"Editando: {aluno_atual['Nome']}")
            novo_nome = st.text_input("Alterar Nome", value=aluno_atual["Nome"])
            nova_n1 = st.number_input("Nota 1", min_value=0.0, max_value=10.0, step=0.1, value=float(aluno_atual["Nota1"]))
            nova_n2 = st.number_input("Nota 2", min_value=0.0, max_value=10.0, step=0.1, value=float(aluno_atual["Nota2"]))
            nova_n3 = st.number_input("Nota 3", min_value=0.0, max_value=10.0, step=0.1, value=float(aluno_atual["Nota3"]))
            
            atualizar_btn = st.form_submit_button("Salvar Alterações")
            if atualizar_btn:
                st.session_state.dados_escolares[indice_selecionado]["Nome"] = novo_nome
                st.session_state.dados_escolares[indice_selecionado]["Nota1"] = nova_n1
                st.session_state.dados_escolares[indice_selecionado]["Nota2"] = nova_n2
                st.session_state.dados_escolares[indice_selecionado]["Nota3"] = nova_n3
                st.success("Atualizado!")
                st.rerun()

        if st.button("❌ Excluir Registro", type="primary"):
            st.session_state.dados_escolares.pop(indice_selecionado)
            st.success("Removido!")
            st.rerun()


# --- ABA 5: GERENCIAMENTO DE TURMAS, PROFS E DISCIPLINAS ---
with aba5:
    st.header("⚙️ Configurações do Sistema")
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.subheader("🏫 Turmas / Séries")
        nova_turma = st.text_input("Nova Turma")
        if st.button("Adicionar Turma"):
            if nova_turma.strip() and nova_turma not in st.session_state.turmas_cadastradas:
                st.session_state.turmas_cadastradas.append(nova_turma.strip())
                st.rerun()
                
        for t in list(st.session_state.turmas_cadastradas):
            c1, c2 = st.columns([3, 1])
            c1.write(f"- {t}")
            if c2.button("Remover", key=f"del_t_{t}"):
                st.session_state.turmas_cadastradas.remove(t)
                st.rerun()

    with col_g2:
        st.subheader("📚 Disciplinas e Professores")
        nova_disc = st.text_input("Nova Disciplina")
        if st.button("Adicionar Disciplina"):
            if nova_disc.strip() and nova_disc not in st.session_state.disciplinas_cadastradas:
                st.session_state.disciplinas_cadastradas.append(nova_disc.strip())
                st.rerun()

    st.markdown("---")
    st.subheader("⚠️ Reset de Dados")
    if st.button("🗑️ Limpar Todos os Dados"):
        st.session_state.dados_escolares = []
        st.session_state.registro_chamada = []
        st.rerun()

# Rodapé
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Sistema Escolar Automatizado 2027 📚</p>", unsafe_allow_html=True)
           
    
