import streamlit as st
import pandas as pd
from datetime import date
import io

# Importação da biblioteca ReportLab para geração de PDFs
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
st.markdown("Gerencie turmas, controle frequências para o ano letivo de 2027, gere boletins em PDF e autorize o acesso de professores.")

# --- INICIALIZAÇÃO DE DADOS NA SESSÃO (SESSION STATE) ---
if "dados_escolares" not in st.session_state:
    st.session_state.dados_escolares = [
        {"Turma": "1º Ano A", "Disciplina": "Física", "Professor": "Prof. Carlos", "Nome": "Ana Silva", "Nota1": 8.0, "Nota2": 7.5, "Nota3": 9.0},
        {"Turma": "1º Ano A", "Disciplina": "Física", "Professor": "Prof. Carlos", "Nome": "Carlos Souza", "Nota1": 5.0, "Nota2": 6.0, "Nota3": 4.5},
        {"Turma": "2º Ano B", "Disciplina": "Matemática", "Professor": "Profª Maria", "Nome": "Mariana Lima", "Nota1": 9.5, "Nota2": 8.0, "Nota3": 9.0},
    ]

if "registro_chamada" not in st.session_state:
    st.session_state.registro_chamada = [
        {"Data": "2027-02-10", "Turma": "1º Ano A", "Nome": "Ana Silva", "Status": "Presente"},
        {"Data": "2027-02-10", "Turma": "1º Ano A", "Nome": "Carlos Souza", "Status": "Falta"},
    ]

if "turmas_cadastradas" not in st.session_state:
    st.session_state.turmas_cadastradas = ["1º Ano A", "1º Ano B", "2º Ano A", "2º Ano B", "3º Ano A"]

if "disciplinas_cadastradas" not in st.session_state:
    st.session_state.disciplinas_cadastradas = ["Física", "Matemática", "Química", "Biologia", "Português", "História"]

# Professores com status de autorização ("Autorizado" ou "Pendente")
if "professores_cadastrados" not in st.session_state:
    st.session_state.professores_cadastrados = [
        {"Nome": "Prof. Carlos", "Status": "Autorizado"},
        {"Nome": "Profª Maria", "Status": "Autorizado"},
        {"Nome": "Prof. João", "Status": "Autorizado"},
        {"Nome": "Profª Ana", "Status": "Autorizado"}
    ]


# --- FUNÇÃO PARA GERAR BOLETIM EM PDF ---
def gerar_boletim_pdf(nome_aluno, turma_aluno, df_aluno_notas, faltas_aluno):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=1,
        spaceAfter=15,
        textColor=colors.HexColor('#1E3A8A')
    )
    story.append(Paragraph("<b>BOLETIM ESCOLAR - ANO LETIVO 2027</b>", title_style))
    story.append(Spacer(1, 10))

    info_text = f"<b>Aluno(a):</b> {nome_aluno}<br/><b>Turma/Série:</b> {turma_aluno}<br/><b>Total de Faltas Registradas (2027):</b> {faltas_aluno}"
    story.append(Paragraph(info_text, styles['Normal']))
    story.append(Spacer(1, 15))

    data_tabela = [["Disciplina", "Professor", "Nota 1", "Nota 2", "Nota 3", "Média", "Situação"]]
    
    for _, row in df_aluno_notas.iterrows():
        data_tabela.append([
            str(row["Disciplina"]),
            str(row["Professor"]),
            str(row["Nota1"]),
            str(row["Nota2"]),
            str(row["Nota3"]),
            str(row["Média"]),
            str(row["Situação"])
        ])

    tabela = Table(data_tabela, colWidths=[100, 100, 55, 55, 55, 55, 100])
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
    story.append(Spacer(1, 40))
    story.append(Paragraph("____________________________________________", ParagraphStyle('Sign', alignment=1)))
    story.append(Paragraph("Assinatura da Direção / Coordenação", ParagraphStyle('SignSub', alignment=1, fontSize=9)))

    doc.build(story)
    buffer.seek(0)
    return buffer


# --- ABAS DE NAVEGAÇÃO DO SISTEMA ---
aba1, aba2, aba3, aba4, aba5, aba6 = st.tabs([
    "📝 Lançar Notas", 
    "📅 Chamada (Ano 2027)", 
    "📄 Boletim & Relatórios PDF", 
    "✏️ Editar / Excluir Registros", 
    "👨‍🏫 Cadastro de Professor",
    "⚙️ Gerenciamento Geral"
])


# --- ABA 1: LANÇAR NOTAS E ALUNOS ---
with aba1:
    st.header("Cadastro de Alunos e Lançamento de Notas")
    
    profs_autorizados = [p["Nome"] for p in st.session_state.professores_cadastrados if p["Status"] == "Autorizado"]

    if len(st.session_state.turmas_cadastradas) == 0 or len(st.session_state.disciplinas_cadastradas) == 0:
        st.warning("⚠️ Cadastre ao menos uma Turma e uma Disciplina nas Configurações.")
    elif len(profs_autorizados) == 0:
        st.warning("⚠️ Não há professores autorizados no momento. Vá até a aba 'Cadastro de Professor' para solicitar ou autorizar um.")
    else:
        with st.form("form_aluno", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                turma_escolhida = st.selectbox("Selecione a Turma", st.session_state.turmas_cadastradas)
                disciplina_escolhida = st.selectbox("Selecione a Disciplina", st.session_state.disciplinas_cadastradas)
                professor_escolhido = st.selectbox("Professor Responsável (Autorizado)", profs_autorizados)
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
                    st.success(f"Notas do(a) aluno(a) {nome_aluno.strip()} salvas com sucesso!")
                else:
                    st.error("Por favor, digite o nome do aluno.")


# --- ABA 2: DIÁRIO DE FREQUÊNCIA / CHAMADA 2027 ---
with aba2:
    st.header("📅 Diário de Classe - Chamada e Frequência (2027)")
    
    if len(st.session_state.turmas_cadastradas) > 0:
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            turma_chamada = st.selectbox("Selecione a Turma para Fazer a Chamada:", st.session_state.turmas_cadastradas, key="chamada_turma")
        with col_c2:
            data_chamada = st.date_input("Data da Aula (Ano 2027):", value=date(2027, 2, 1))

        alunos_na_turma = sorted(list(set([a["Nome"] for a in st.session_state.dados_escolares if a["Turma"] == turma_chamada])))

        if len(alunos_na_turma) > 0:
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
                    st.success("Chamada registrada com sucesso para o ano de 2027!")
        else:
            st.info("Nenhum aluno cadastrado nesta turma.")

        st.markdown("---")
        st.subheader("📊 Histórico de Chamadas")
        if len(st.session_state.registro_chamada) > 0:
            df_chamada = pd.DataFrame(st.session_state.registro_chamada)
            st.dataframe(df_chamada[df_chamada["Turma"] == turma_chamada], use_container_width=True)
    else:
        st.warning("Nenhuma turma cadastrada.")


# --- ABA 3: RELATÓRIO E BOLETIM PDF ---
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
            
            df_chamada_all = pd.DataFrame(st.session_state.registro_chamada) if len(st.session_state.registro_chamada) > 0 else pd.DataFrame(columns=["Nome", "Status"])
            faltas_totais = len(df_chamada_all[(df_chamada_all["Nome"] == aluno_boletim) & (df_chamada_all["Status"] == "Falta")])
            
            pdf_bytes = gerar_boletim_pdf(aluno_boletim, turma_aluno, df_aluno, faltas_totais)
            
            st.download_button(
                label=f"📄 Baixar Boletim em PDF ({aluno_boletim})",
                data=pdf_bytes,
                file_name=f"Boletim_2027_{aluno_boletim.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
    else:
        st.info("Nenhum dado cadastrado.")


# --- ABA 4: EDITAR OU EXCLUIR REGISTROS ---
with aba4:
    st.header("✏️ Editar Notas ou Excluir Registros de Alunos")
    
    if len(st.session_state.dados_escolares) > 0:
        lista_nomes = [f"{item['Nome']} - {item['Turma']} ({item['Disciplina']})" for item in st.session_state.dados_escolares]
        aluno_selecionado_str = st.selectbox("Selecione o Registro", lista_nomes)
        
        indice_selecionado = lista_nomes.index(aluno_selecionado_str)
        aluno_atual = st.session_state.dados_escolares[indice_selecionado]
        
        with st.form("form_edicao"):
            novo_nome = st.text_input("Alterar Nome do Aluno", value=aluno_atual["Nome"])
            nova_n1 = st.number_input("Nota 1", min_value=0.0, max_value=10.0, step=0.1, value=float(aluno_atual["Nota1"]))
            nova_n2 = st.number_input("Nota 2", min_value=0.0, max_value=10.0, step=0.1, value=float(aluno_atual["Nota2"]))
            nova_n3 = st.number_input("Nota 3", min_value=0.0, max_value=10.0, step=0.1, value=float(aluno_atual["Nota3"]))
            
            if st.form_submit_button("Salvar Alterações"):
                st.session_state.dados_escolares[indice_selecionado]["Nome"] = novo_nome.strip()
                st.session_state.dados_escolares[indice_selecionado]["Nota1"] = nova_n1
                st.session_state.dados_escolares[indice_selecionado]["Nota2"] = nova_n2
                st.session_state.dados_escolares[indice_selecionado]["Nota3"] = nova_n3
                st.success("Atualizado com sucesso!")
                st.rerun()

        if st.button("❌ Excluir Este Registro", type="primary"):
            st.session_state.dados_escolares.pop(indice_selecionado)
            st.success("Removido!")
            st.rerun()
    else:
        st.info("Não há registros para editar.")


# --- ABA 5: CADASTRO DE PROFESSOR (SOLICITAÇÃO DE ACESSO) ---
with aba5:
    st.header("👨‍🏫 Solicitação de Cadastro de Professor")
    st.markdown("Cadastre seu nome para solicitar acesso ao sistema. O acesso passará por autorização da coordenação.")

    with st.form("form_solicitacao_prof"):
        nome_novo_prof = st.text_input("Nome Completo do Professor (ex: Prof. Marcos Silva)")
        solicitar_btn = st.form_submit_button("Solicitar Cadastro")

        if solicitar_btn:
            if nome_novo_prof.strip():
                # Verificar se já existe
                nomes_existentes = [p["Nome"] for p in st.session_state.professores_cadastrados]
                if nome_novo_prof.strip() not in nomes_existentes:
                    st.session_state.professores_cadastrados.append({
                        "Nome": nome_novo_prof.strip(),
                        "Status": "Pendente"
                    })
                    st.success(f"Solicitação enviada com sucesso para '{nome_novo_prof.strip()}'! Aguarde a autorização na aba de Gerenciamento.")
                else:
                    st.error("Este nome já está cadastrado ou pendente no sistema.")
            else:
                st.error("Por favor, digite um nome válido.")


# --- ABA 6: GERENCIAMENTO GERAL E AUTORIZAÇÃO DE PROFESSORES ---
with aba6:
    st.header("⚙️ Gerenciamento e Autorização de Acessos")
    
    # Seção de Autorização de Professores
    st.subheader("🛡️ Autorização de Professores (Pendentes)")
    pendentes = [p for p in st.session_state.professores_cadastrados if p["Status"] == "Pendente"]
    
    if len(pendentes) > 0:
        for p in pendentes:
            col_p1, col_p2, col_p3 = st.columns([3, 1, 1])
            with col_p1:
                st.write(f"⏳ **{p['Nome']}** (Aguardando Autorização)")
            with col_p2:
                if st.button("✅ Autorizar", key=f"auth_{p['Nome']}"):
                    for item in st.session_state.professores_cadastrados:
                        if item["Nome"] == p["Nome"]:
                            item["Status"] = "Autorizado"
                    st.success(f"Professor {p['Nome']} autorizado com sucesso!")
                    st.rerun()
            with col_p3:
                if st.button("❌ Rejeitar", key=f"rej_{p['Nome']}"):
                    st.session_state.professores_cadastrados = [item for item in st.session_state.professores_cadastrados if item["Nome"] != p["Nome"]]
                    st.success(f"Solicitação de {p['Nome']} rejeitada.")
                    st.rerun()
    else:
        st.info("Nenhuma solicitação de professor pendente no momento.")

    st.markdown("---")
    
    # Lista de Professores Atuais e Remoção
    st.subheader("👥 Professores Cadastrados no Sistema")
    for p in list(st.session_state.professores_cadastrados):
        col_cad1, col_cad2 = st.columns([3, 1])
        with col_cad1:
            badge = "🟢 Autorizado" if p["Status"] == "Autorizado" else "🟡 Pendente"
            st.write(f"- {p['Nome']} ({badge})")
        with col_cad2:
            if st.button("Remover", key=f"del_prof_geral_{p['Nome']}"):
                st.session_state.professores_cadastrados = [item for item in st.session_state.professores_cadastrados if item["Nome"] != p["Nome"]]
                st.success(f"Professor {p['Nome']} removido.")
                st.rerun()

    st.markdown("---")
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.subheader("🏫 Gerenciar Turmas / Séries")
        nova_turma = st.text_input("Nova Série/Turma (ex: 6º Ano B)")
        if st.button("Adicionar Turma"):
            if nova_turma.strip() and nova_turma.strip() not in st.session_state.turmas_cadastradas:
                st.session_state.turmas_cadastradas.append(nova_turma.strip())
                st.rerun()
        
        for t in list(st.session_state.turmas_cadastradas):
            c1, c2 = st.columns([3, 1])
            c1.write(f"- {t}")
            if c2.button("Remover", key=f"del_t_{t}"):
                st.session_state.turmas_cadastradas.remove(t)
                st.rerun()

    with col_g2:
        st.subheader("📚 Gerenciar Disciplinas")
        nova_disc = st.text_input("Nova Disciplina (ex: Filosofia)")
        if st.button("Adicionar Disciplina"):
            if nova_disc.strip() and nova_disc.strip() not in st.session_state.disciplinas_cadastradas:
                st.session_state.disciplinas_cadastradas.append(nova_disc.strip())
                st.rerun()
        
        for d in list(st.session_state.disciplinas_cadastradas):
            c1, c2 = st.columns([3, 1])
            c1.write(f"- {d}")
            if c2.button("Remover", key=f"del_d_{d}"):
                st.session_state.disciplinas_cadastradas.remove(d)
                st.rerun()

    st.markdown("---")
    st.subheader("⚠️ Zona de Perigo (Reset Total)")
    if st.button("🗑️ Limpar Todos os Dados do Sistema", type="primary"):
        st.session_state.dados_escolares = []
        st.session_state.registro_chamada = []
        st.success("Dados limpos!")
        st.rerun()

# Rodapé
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Sistema Escolar Automatizado 2027 📚</p>", unsafe_allow_html=True)
    
