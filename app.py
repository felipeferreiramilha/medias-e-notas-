import streamlit as st
import pandas as pd
from datetime import date
import io

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

st.set_page_config(
    page_title="Sistema de Gestão Escolar 2027",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Sistema de Gestão Escolar - 2027")
st.markdown("Gerenciamento escolar completo: Cadastro de turmas, alunos, professores por disciplina, controle de chamadas, notas e boletins em PDF.")

if "turmas_cadastradas" not in st.session_state:
    st.session_state.turmas_cadastradas = []

if "disciplinas_cadastradas" not in st.session_state:
    st.session_state.disciplinas_cadastradas = []

if "professores_cadastrados" not in st.session_state:
    st.session_state.professores_cadastrados = []

if "alunos_cadastrados" not in st.session_state:
    st.session_state.alunos_cadastrados = []

if "dados_escolares" not in st.session_state:
    st.session_state.dados_escolares = []

if "registro_chamada" not in st.session_state:
    st.session_state.registro_chamada = []

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

aba1, aba2, aba3, aba4, aba5, aba6, aba7 = st.tabs([
    "⚙️ Configurações / Cadastros", 
    "👨‍🏫 Solicitação Professor", 
    "📝 Matrícula de Alunos",
    "📊 Lançamento de Notas (3 Notas)", 
    "📅 Chamada & Frequência", 
    "📄 Relatórios & Boletim PDF",
    "🔒 Acesso Restrito do Professor"
])

with aba1:
    st.header("⚙️ Cadastro de Turmas e Disciplinas")
    st.markdown("Cadastre as turmas (séries) e as disciplinas iniciais do ano letivo de 2027.")

    col_cfg1, col_cfg2 = st.columns(2)

    with col_cfg1:
        st.subheader("🏫 Turmas / Séries")
        nova_turma = st.text_input("Nome da Turma (ex: 1º Ano A, 6º Ano B)")
        if st.button("Adicionar Turma"):
            if nova_turma.strip() and nova_turma.strip() not in st.session_state.turmas_cadastradas:
                st.session_state.turmas_cadastradas.append(nova_turma.strip())
                st.success(f"Turma '{nova_turma.strip()}' cadastrada!")
                st.rerun()
            else:
                st.error("Digite um nome válido ou uma turma já existente.")

        st.write("**Turmas Ativas:**")
        if len(st.session_state.turmas_cadastradas) > 0:
            for t in list(st.session_state.turmas_cadastradas):
                c_t1, c_t2 = st.columns([3, 1])
                c_t1.write(f"- 📌 {t}")
                if c_t2.button("Remover", key=f"del_turma_{t}"):
                    st.session_state.turmas_cadastradas.remove(t)
                    st.rerun()
        else:
            st.info("Nenhuma turma cadastrada.")

    with col_cfg2:
        st.subheader("📚 Disciplinas")
        nova_disc = st.text_input("Nome da Disciplina (ex: Física, Matemática)")
        if st.button("Adicionar Disciplina"):
            if nova_disc.strip() and nova_disc.strip() not in st.session_state.disciplinas_cadastradas:
                st.session_state.disciplinas_cadastradas.append(nova_disc.strip())
                st.success(f"Disciplina '{nova_disc.strip()}' cadastrada!")
                st.rerun()
            else:
                st.error("Digite um nome válido ou disciplina já existente.")

        st.write("**Disciplinas Ativas:**")
        if len(st.session_state.disciplinas_cadastradas) > 0:
            for d in list(st.session_state.disciplinas_cadastradas):
                c_d1, c_d2 = st.columns([3, 1])
                c_d1.write(f"- 📖 {d}")
                if c_d2.button("Remover", key=f"del_disc_{d}"):
                    st.session_state.disciplinas_cadastradas.remove(d)
                    st.rerun()
        else:
            st.info("Nenhuma disciplina cadastrada.")

    st.markdown("---")
    st.subheader("⚠️ Reset Total do Sistema")
    if st.button("🗑️ Apagar Todos os Dados", type="primary"):
        st.session_state.turmas_cadastradas = []
        st.session_state.disciplinas_cadastradas = []
        st.session_state.professores_cadastrados = []
        st.session_state.alunos_cadastrados = []
        st.session_state.dados_escolares = []
        st.session_state.registro_chamada = []
        st.success("Sistema limpo com sucesso!")
        st.rerun()

with aba2:
    st.header("👨‍🏫 Cadastro e Vinculação de Professor por Disciplina")
    st.markdown("O professor se cadastra informando seu nome e qual disciplina irá lecionar. O acesso só é liberado após a autorização.")

    if len(st.session_state.disciplinas_cadastradas) == 0:
        st.warning("⚠️ Cadastre ao menos uma disciplina na aba 'Configurações' primeiro.")
    else:
        with st.form("form_prof"):
            nome_prof = st.text_input("Nome Completo do Professor (ex: Prof. Carlos)")
            disc_prof = st.selectbox("Disciplina Lecionada", st.session_state.disciplinas_cadastradas)
            solicitar_prof = st.form_submit_button("Solicitar Acesso")

            if solicitar_prof:
                if nome_prof.strip():
                    ja_existe = any(p["Nome"] == nome_prof.strip() and p["Disciplina"] == disc_prof for p in st.session_state.professores_cadastrados)
                    if not ja_existe:
                        st.session_state.professores_cadastrados.append({
                            "Nome": nome_prof.strip(),
                            "Disciplina": disc_prof,
                            "Status": "Pendente"
                        })
                        st.success(f"Solicitação enviada para {nome_prof.strip()} na disciplina {disc_prof}! Aguarde liberação.")
                    else:
                        st.error("Este professor já está cadastrado para esta disciplina.")
                else:
                    st.error("Digite o nome do professor.")

    st.markdown("---")
    st.subheader("🛡️ Painel de Autorização da Coordenação")
    pendentes = [p for p in st.session_state.professores_cadastrados if p["Status"] == "Pendente"]

    if len(pendentes) > 0:
        for p in pendentes:
            col_p1, col_p2, col_p3 = st.columns([3, 1, 1])
            col_p1.write(f"⏳ **{p['Nome']}** - Disciplina: *{p['Disciplina']}*")
            if col_p2.button("✅ Autorizar", key=f"auth_{p['Nome']}_{p['Disciplina']}"):
                for item in st.session_state.professores_cadastrados:
                    if item["Nome"] == p["Nome"] and item["Disciplina"] == p["Disciplina"]:
                        item["Status"] = "Autorizado"
                st.success(f"Professor {p['Nome']} autorizado!")
                st.rerun()
            if col_p3.button("❌ Rejeitar", key=f"rej_{p['Nome']}_{p['Disciplina']}"):
                st.session_state.professores_cadastrados = [
                    item for item in st.session_state.professores_cadastrados 
                    if not (item["Nome"] == p["Nome"] and item["Disciplina"] == p["Disciplina"])
                ]
                st.success("Rejeitado.")
                st.rerun()
    else:
        st.info("Nenhum professor aguardando autorização.")

    st.write("### 👥 Todos os Professores Registrados:")
    for p in st.session_state.professores_cadastrados:
        badge = "🟢 Autorizado" if p["Status"] == "Autorizado" else "🟡 Pendente"
        col_lg1, col_lg2 = st.columns([3, 1])
        col_lg1.write(f"- {p['Nome']} ({p['Disciplina']}) - {badge}")
        if col_lg2.button("Remover", key=f"del_p_{p['Nome']}_{p['Disciplina']}"):
            st.session_state.professores_cadastrados = [
                item for item in st.session_state.professores_cadastrados 
                if not (item["Nome"] == p["Nome"] and item["Disciplina"] == p["Disciplina"])
            ]
            st.rerun()

with aba3:
    st.header("📝 Cadastro / Matrícula de Alunos")
    st.markdown("Cadastre os alunos e vincule-os diretamente às turmas cadastradas.")

    if len(st.session_state.turmas_cadastradas) == 0:
        st.warning("⚠️ Cadastre ao menos uma turma na aba 'Configurações' antes de matricular alunos.")
    else:
        with st.form("form_matricula", clear_on_submit=True):
            turma_aluno = st.selectbox("Selecione a Turma", st.session_state.turmas_cadastradas)
            nome_novo_aluno = st.text_input("Nome Completo do Aluno")
            cadastrar_aluno_btn = st.form_submit_button("Matricular Aluno")

            if cadastrar_aluno_btn:
                if nome_novo_aluno.strip():
                    st.session_state.alunos_cadastrados.append({
                        "Turma": turma_aluno,
                        "Nome": nome_novo_aluno.strip()
                    })
                    st.success(f"Aluno(a) {nome_novo_aluno.strip()} matriculado(a) na turma {turma_aluno}!")
                else:
                    st.error("Digite o nome do aluno.")

    st.markdown("---")
    st.subheader("📋 Lista Geral de Alunos Matriculados")
    if len(st.session_state.alunos_cadastrados) > 0:
        df_alunos_geral = pd.DataFrame(st.session_state.alunos_cadastrados)
        st.dataframe(df_alunos_geral, use_container_width=True)
    else:
        st.info("Nenhum aluno matriculado ainda.")

with aba4:
    st.header("📊 Lançamento de Notas (3 Avaliações)")
    st.markdown("Selecione a Turma, a Disciplina, o Professor Autorizado e lance as três notas do aluno.")

    profs_autorizados = [p for p in st.session_state.professores_cadastrados if p["Status"] == "Autorizado"]

    if len(st.session_state.turmas_cadastradas) == 0 or len(st.session_state.alunos_cadastrados) == 0 or len(profs_autorizados) == 0:
        st.warning("⚠️ Certifique-se de que existem Turmas, Alunos matriculados e Professores Autorizados.")
    else:
        with st.form("form_notas", clear_on_submit=True):
            col_n1, col_n2 = st.columns(2)
            with col_n1:
                t_escolhida = st.selectbox("Turma", st.session_state.turmas_cadastradas)
                alunos_da_turma = [a["Nome"] for a in st.session_state.alunos_cadastrados if a["Turma"] == t_escolhida]
                if len(alunos_da_turma) > 0:
                    aluno_escolhido = st.selectbox("Aluno", alunos_da_turma)
                else:
                    aluno_escolhido = None
                    st.warning("Não há alunos nesta turma.")

                disc_escolhida = st.selectbox("Disciplina", st.session_state.disciplinas_cadastradas)
                profs_da_disc = [p["Nome"] for p in profs_autorizados if p["Disciplina"] == disc_escolhida]
                if len(profs_da_disc) > 0:
                    prof_resp = st.selectbox("Professor Responsável", profs_da_disc)
                else:
                    prof_resp = "Nenhum professor autorizado para esta disciplina"
                    st.warning(f"Nenhum professor autorizado para {disc_escolhida}.")

            with col_n2:
                n1 = st.number_input("Nota 1 (0 a 10)", min_value=0.0, max_value=10.0, step=0.1)
                n2 = st.number_input("Nota 2 (0 a 10)", min_value=0.0, max_value=10.0, step=0.1)
                n3 = st.number_input("Nota 3 (0 a 10)", min_value=0.0, max_value=10.0, step=0.1)

            salvar_notas_btn = st.form_submit_button("Salvar Notas do Aluno")

            if salvar_notas_btn:
                if aluno_escolhido and prof_resp != "Nenhum professor autorizado para esta disciplina":
                    registros_existentes = st.session_state.dados_escolares
                    atualizado = False
                    for reg in registros_existentes:
                        if reg["Turma"] == t_escolhida and reg["Nome"] == aluno_escolhido and reg["Disciplina"] == disc_escolhida:
                            reg["Nota1"] = n1
                            reg["Nota2"] = n2
                            reg["Nota3"] = n3
                            reg["Professor"] = prof_resp
                            atualizado = True
                            break
                    
                    if not atualizado:
                        st.session_state.dados_escolares.append({
                            "Turma": t_escolhida,
                            "Disciplina": disc_escolhida,
                            "Professor": prof_resp,
                            "Nome": aluno_escolhido,
                            "Nota1": n1,
                            "Nota2": n2,
                            "Nota3": n3
                        })
                    st.success(f"Notas de {aluno_escolhido} salvas com sucesso em {disc_escolhida}!")
                else:
                    st.error("Verifique se o aluno e o professor foram selecionados corretamente.")

with aba5:
    st.header("📅 Diário de Classe - Chamada e Frequência (2027)")
    st.markdown("Informe o **dia da aula**, o **número/nome da aula** (ex: Aula 1, Aula 2) e registre a presença ou falta dos alunos.")

    if len(st.session_state.turmas_cadastradas) == 0 or len(st.session_state.alunos_cadastrados) == 0:
        st.warning("⚠️ Cadastre turmas e alunos para realizar a chamada.")
    else:
        col_ch1, col_ch2, col_ch3 = st.columns(3)
        with col_ch1:
            turma_chamada = st.selectbox("Turma", st.session_state.turmas_cadastradas, key="ch_turma")
        with col_ch2:
            data_aula = st.date_input("Data da Aula (2027)", value=date(2027, 2, 1))
        with col_ch3:
            nome_aula = st.text_input("Identificação da Aula", value="Aula 1")

        alunos_turma_ch = [a["Nome"] for a in st.session_state.alunos_cadastrados if a["Turma"] == turma_chamada]

        if len(alunos_turma_ch) > 0:
            st.subheader(f"Chamada - {turma_chamada} | Data: {data_aula.strftime('%d/%m/%Y')} | {nome_aula}")
            with st.form("form_chamada"):
                status_presenca = {}
                for al in alunos_turma_ch:
                    c_a1, c_a2 = st.columns([3, 2])
                    c_a1.write(f"👤 {al}")
                    status_presenca[al] = c_a2.radio("Status", ["Presente", "Falta"], key=f"st_{al}_{data_aula}_{nome_aula}", horizontal=True)

                if st.form_submit_button("💾 Salvar Chamada"):
                    for al, st_val in status_presenca.items():
                        st.session_state.registro_chamada.append({
                            "Data": str(data_aula),
                            "Aula": nome_aula,
                            "Turma": turma_chamada,
                            "Nome": al,
                            "Status": st_val
                        })
                    st.success("Chamada registrada com sucesso!")
        else:
            st.info("Nenhum aluno matriculado nesta turma.")

        st.markdown("---")
        st.subheader("📊 Histórico de Frequência Registrada")
        if len(st.session_state.registro_chamada) > 0:
            df_ch = pd.DataFrame(st.session_state.registro_chamada)
            st.dataframe(df_ch[df_ch["Turma"] == turma_chamada], use_container_width=True)

with aba6:
    st.header("📄 Relatório Geral de Desempenho e Boletim em PDF")

    if len(st.session_state.dados_escolares) > 0:
        df_geral = pd.DataFrame(st.session_state.dados_escolares)
        df_geral["Média"] = ((df_geral["Nota1"] + df_geral["Nota2"] + df_geral["Nota3"]) / 3).round(2)

        def definir_situacao(media):
            if media >= 7.0:
                return "✅ Aprovado"
            elif media >= 4.0:
                return "⚠️ Recuperação"
            else:
                return "❌ Reprovado"

        df_geral["Situação"] = df_geral["Média"].apply(definir_situacao)

        filtro_t = st.selectbox("Filtrar por Turma:", ["Todas as Turmas"] + list(st.session_state.turmas_cadastradas), key="filtro_t_rel")
        df_ex = df_geral if filtro_t == "Todas as Turmas" else df_geral[df_geral["Turma"] == filtro_t]
        
        st.dataframe(df_ex, use_container_width=True)

        st.markdown("---")
        st.subheader("📥 Emitir Boletim Escolar Individual (PDF)")
        lista_todos_alunos = sorted(list(set(df_geral["Nome"].tolist())))
        aluno_escolhido_bol = st.selectbox("Selecione o Aluno", lista_todos_alunos)

        if aluno_escolhido_bol:
            df_al = df_geral[df_geral["Nome"] == aluno_escolhido_bol]
            t_al = df_al["Turma"].iloc[0]

            df_ch_all = pd.DataFrame(st.session_state.registro_chamada) if len(st.session_state.registro_chamada) > 0 else pd.DataFrame(columns=["Nome", "Status"])
            total_faltas = len(df_ch_all[(df_ch_all["Nome"] == aluno_escolhido_bol) & (df_ch_all["Status"] == "Falta")]) if not df_ch_all.empty else 0

            pdf_bytes = gerar_boletim_pdf(aluno_escolhido_bol, t_al, df_al, total_faltas)

            st.download_button(
                label=f"📄 Baixar Boletim em PDF ({aluno_escolhido_bol})",
                data=pdf_bytes,
                file_name=f"Boletim_2027_{aluno_escolhido_bol.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
    else:
        st.info("Nenhum lançamento de notas efetuado ainda.")

with aba7:
    st.header("🔒 Painel de Acesso Restrito por Professor e Disciplina")
    st.markdown("O professor seleciona seu nome e disciplina para visualizar apenas as notas e turmas da sua alçada.")

    profs_autorizados_7 = [p for p in st.session_state.professores_cadastrados if p["Status"] == "Autorizado"]

    if len(profs_autorizados_7) > 0:
        nomes_profs = sorted(list(set([p["Nome"] for p in profs_autorizados_7])))
        prof_login = st.selectbox("Selecione seu Nome (Professor)", nomes_profs)
        
        discs_prof = [p["Disciplina"] for p in profs_autorizados_7 if p["Nome"] == prof_login]
        disc_login = st.selectbox("Selecione sua Disciplina", discs_prof)

        st.markdown(f"### 🎯 Visão Exclusiva: {prof_login} - Disciplina: {disc_login}")

        if len(st.session_state.dados_escolares) > 0:
            df_all = pd.DataFrame(st.session_state.dados_escolares)
            df_prof_filtrado = df_all[(df_all["Disciplina"] == disc_login) & (df_all["Professor"] == prof_login)]

            if not df_prof_filtrado.empty:
                df_prof_filtrado["Média"] = ((df_prof_filtrado["Nota1"] + df_prof_filtrado["Nota2"] + df_prof_filtrado["Nota3"]) / 3).round(2)
                st.dataframe(df_prof_filtrado, use_container_width=True)
            else:
                st.info("Nenhum lançamento de notas encontrado para a sua disciplina.")
        else:
            st.info("Nenhum dado cadastrado no sistema.")
    else:
        st.warning("Não há professores autorizados no sistema no momento.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Sistema Escolar Automatizado 2027 📚</p>", unsafe_allow_html=True)

        
