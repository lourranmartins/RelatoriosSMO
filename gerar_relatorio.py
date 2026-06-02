import warnings
warnings.filterwarnings("ignore")

from fpdf import FPDF
import os

def texto_blindado(txt):
    """Filtra caracteres que travam a compilação do PDF e garante codificação limpa"""
    if not isinstance(txt, str):
        return txt
    txt = txt.replace('—', '-').replace('–', '-').replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'")
    return txt.encode('latin-1', 'replace').decode('latin-1')

class PDF(FPDF):
    def header(self):
        if os.path.exists('brasao_pmcm.png'):
            self.image('brasao_pmcm.png', 10, 8, 25)
        if os.path.exists('sec_obras.png'):
            self.image('sec_obras.png', 170, 8, 30)
            
        self.set_y(15)
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(17, 43, 60)
        self.cell(0, 5, texto_blindado('Secretaria de Obras, Saneamento, Urbanismo e Conservação'), new_x="LMARGIN", new_y="NEXT", align='C')
        self.set_font('Helvetica', '', 10)
        self.cell(0, 5, texto_blindado('Município de Cachoeiras de Macacu - RJ'), new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, texto_blindado(f'Página {self.page_no()}'), new_x="LMARGIN", new_y="NEXT", align='C')

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(17, 43, 60)
        self.cell(0, 10, texto_blindado(title), new_x="LMARGIN", new_y="NEXT", align='L')
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Helvetica', '', 11)
        self.set_text_color(0)
        self.multi_cell(0, 6, texto_blindado(body), align='J', new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def insert_image(self, image_name, width=170):
        if os.path.exists(image_name):
            self.image(image_name, x='C', w=width)
            self.ln(5)
        else:
            self.set_text_color(255, 0, 0)
            self.cell(0, 10, texto_blindado(f'[Aviso: Imagem {image_name} não anexada no documento]'), new_x="LMARGIN", new_y="NEXT", align='C')
            self.ln(5)

# Iniciando o Documento
pdf = PDF()
pdf.add_page()

# --- CAPA E TÍTULO PRINCIPAL ---
pdf.set_font('Helvetica', 'B', 16)
pdf.set_text_color(17, 43, 60)
pdf.multi_cell(0, 8, texto_blindado('RELATÓRIO TÉCNICO CONSOLIDADO E DEFINITIVO\nAUDITORIA, EVOLUÇÃO E EFICIÊNCIA LOGÍSTICA DA ILUMINAÇÃO PÚBLICA'), align='C', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('Helvetica', '', 12)
pdf.multi_cell(0, 6, texto_blindado('ANÁLISE DE DADOS - PARQUE GLOBAL (pG = pE + pC) - 2020-2026\nDocumento Técnico Consolidado - Junho de 2026'), align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(10)

# --- SUMÁRIO EXECUTIVO ---
pdf.chapter_title('SUMÁRIO EXECUTIVO')
texto_sumario = (
    "O presente documento constitui a consolidação técnica definitiva da "
    "infraestrutura e da dinâmica operacional da iluminação pública do "
    "Município de Cachoeiras de Macacu, integrando os dados das duas "
    "concessionárias locais: Enel (pE) e Cerci (pC). "
    "A notação pG = pE(Pe') + pC foi adotada mantendo a base volumétrica da "
    "Cerci constante (4.341 pts) para isolar rigorosamente a variável "
    "tecnológica e mensurar a eficiência energética e logística pura da gestão."
)
pdf.chapter_body(texto_sumario)
pdf.insert_image('tabela_pg_atualizada.png', width=190)

# --- CAP 1 e 2: EXPANSÃO E TRANSIÇÃO ---
pdf.chapter_title('CAPÍTULO 1 - EXPANSÃO DO PARQUE GLOBAL (2020-2026)')
texto_expansao = (
    "Tracionado pelo crescimento orgânico e pela regularização de loteamentos via Enel, "
    "o Parque Global expandiu de 9.087 para 10.582 pontos físicos (+1.495 novos "
    "pontos homologados à rede municipal)."
)
pdf.chapter_body(texto_expansao)
pdf.insert_image('barras_expansao_pg.png', width=130)

pdf.add_page()
pdf.chapter_title('CAPÍTULO 2 - O PANORAMA LEGADO E A TRANSIÇÃO TECNOLÓGICA')
texto_tecnologia = (
    "Os dados de 2020 revelavam um legado crítico: 73,8% do Parque Global dependia "
    "de Vapor de Mercúrio obsoleto, com um índice de LED de meros 3,1%. "
    "A atual estratégia impôs um modelo de substituição exponencial, visando o "
    "redimensionamento de 53,1% do município em tecnologia LED."
)
pdf.chapter_body(texto_tecnologia)
pdf.insert_image('pizza_absoluta_pg_large_fonts.png', width=170)

# --- CAP 3: GESTÃO ANTERIOR (NOVOS DADOS) ---
pdf.chapter_title('CAPÍTULO 3 - PERFIL OPERACIONAL DA GESTÃO ANTERIOR')
texto_cap3 = (
    "A amostragem operacional auditada em janeiro de 2020 (03/01 a 09/01) evidencia "
    "um padrão puramente corretivo. Na época, em bairros como Tuim, Japuíba, Papucaia e "
    "Castália, executaram-se apenas 51 trocas de lâmpadas em 5 dias úteis (média de "
    "10,2 manutenções/dia). O inventário refletia o passivo energético: 20 unidades "
    "de Mercúrio 250W, 16 de Mercúrio 80W, 10 de Sódio 70W e 5 de Sódio 150W. "
    "Sob esse modelo reativo, a projeção anual (156 dias úteis produtivos) estagnava "
    "em irrisórias 1.591 manutenções por ano."
)
pdf.chapter_body(texto_cap3)

# --- CAP 4: EFEITO TESOURA ---
pdf.add_page()
pdf.chapter_title('CAPÍTULO 4 - IMPACTO TARIFÁRIO E O EFEITO TESOURA')
texto_consumo = (
    "Com a inserção de luminárias LED, o município deflagrou o 'efeito tesoura'. "
    "Embora o número de postes nas ruas tenha crescido (+16,4%), a carga "
    "exigida recuou de 1.076,8 kW para 899,0 kW. O consumo global planejado "
    "despenca de 368.737 para 307.846 kWh/mês (supressão absoluta de -16,5%). "
    "A Secretaria de Obras financiou a expansão territorial exclusivamente "
    "através do ganho de eficiência energética."
)
pdf.chapter_body(texto_consumo)
pdf.insert_image('carga_consumo_pg_corrigido.png', width=160)

# --- CAP 5 e 6: LOGÍSTICA E DESEMPENHO (NOVOS DADOS PROFUNDOS) ---
pdf.chapter_title('CAPÍTULO 5 - ESCALABILIDADE LOGÍSTICA E COBERTURA')
texto_cap5 = (
    "Gerenciar mais de 5.500 pontos de iluminação requer força-tarefa logística. "
    "Entre 2021 e julho de 2024, a gestão registrou colossais 37.840 inserções logísticas "
    "e atendimentos territoriais. Ruas e loteamentos foram revisitados sucessivamente "
    "para a execução de ordens preventivas. A iluminação pública transcendeu a "
    "troca de componentes, consolidando-se como zeladoria infraestrutural permanente."
)
pdf.chapter_body(texto_cap5)

pdf.add_page()
pdf.chapter_title('CAPÍTULO 6 - DESEMPENHO OPERACIONAL E PREVENÇÃO (2026)')
texto_cap6 = (
    "O balanço do 1.º trimestre de 2026 atesta a dupla frente de atuação. Em relação "
    "aos chamados reativos, dos 208 novos pedidos, 93 foram resolvidos diretamente "
    "(44,7% de eficiência), totalizando 129 ordens executadas focadas na amortização "
    "de acúmulos históricos. Contudo, o grande vetor operacional é a manutenção "
    "autônoma: via rondas técnicas e sem chamados prévios, 924 lâmpadas foram "
    "recuperadas preventivamente em 33 dias úteis efetivos (média de 28 manutenções/dia). "
    "Expandindo essa métrica, o município eleva seu teto logístico para 4.368 manutenções "
    "anuais — um ganho formidável de +174,6% (ou 2,75x mais produtividade) frente à gestão anterior."
)
pdf.chapter_body(texto_cap6)

# --- CAP 7: O GARGALO CLIMÁTICO (NOVO DADO NR10) ---
pdf.chapter_title('CAPÍTULO 7 - O FATOR CLIMÁTICO COMO PRINCIPAL GARGALO')
texto_cap7 = (
    "A auditoria de fluxos demonstra que o fator limitante de campo não é a defasagem "
    "técnica, mas a rigidez meteorológica face às normas de segurança (NR-10 e NR-35). "
    "Intervenções em rede energizada são terminantemente proibidas sob chuva. "
    "Dos 72 dias monitorados no início de 2026, 21 apresentaram precipitações de risco, "
    "resultando em 29% do calendário impactado por fatores climáticos. "
    "Nos 71% de dias produtivos restantes, o ritmo preventivo acelerado compensa "
    "as perdas, garantindo uma produtividade de 1,61 ordens liquidadas por dia útil seco."
)
pdf.chapter_body(texto_cap7)

# --- CAP 8 e 9: FATURAMENTO PASSIVO (V. HUGO) ---
pdf.add_page()
pdf.chapter_title('CAPÍTULO 8 - O CENSO DA CERCI E A TAUTOLOGIA DE DADOS')
texto_tautologia = (
    "O censo da Cerci (02/06/2026) fixou a carga em 328.630 kWh/mês, o que corrobora "
    "exatamente a fatura da cooperativa (129.408 kWh faturados). Segundo manifestação "
    "técnica do Engenheiro Eletricista Victor Hugo Queiroz, trata-se de uma tautologia "
    "burocrática: a conta e o censo batem porque a concessionária baseia sua cobrança "
    "em estimativas de banco de dados caducos, ignorando a eficientização real "
    "já implementada nos postes pela municipalidade."
)
pdf.chapter_body(texto_tautologia)

pdf.chapter_title('CAPÍTULO 9 - A FGC ENGENHARIA E O FATURAMENTO RETIDO')
texto_fgc = (
    "Atuando sob a matriz de fiscalização da SMO, a FGC Engenharia vem convertendo "
    "massivamente vapor de mercúrio e sódio para LED. Como as concessionárias demoram "
    "a refletir essas trocas sistêmicas em seus inventários, a Prefeitura sofre o "
    "'Faturamento Passivo Retido'. O município despende hoje cerca de R$ 264.589,67 mensais "
    "(Fatura Enel de R$ 162.847,29 somada à fatura Cerci de R$ 101.742,38), pagando um prêmio "
    "tributário temporário por tecnologias gastadoras que, no plano físico, sequer "
    "existem mais nas ruas."
)
pdf.chapter_body(texto_fgc)

# --- CAP 10: CONCLUSÃO ---
pdf.chapter_title('CAPÍTULO 10 - RECOMENDAÇÕES REGULATÓRIAS')
texto_diretrizes = (
    "O alvo técnico final (Meta de Campo: 307.846 kWh/mês) é o verdadeiro Balanço "
    "Patrimonial da iluminação municipal. Recomenda-se notificar as operadoras de rede "
    "com os Diários de Obra emitidos pela FGC Engenharia, exigindo a liquidação e o "
    "expurgo da gordura tarifária acumulada, visando a convergência matemática "
    "entre o faturado pela concessionária e o efetivamente executado pelas equipes de campo."
)
pdf.chapter_body(texto_diretrizes)

# --- ASSINATURA ---
pdf.ln(10)
pdf.set_font('Helvetica', 'B', 11)
pdf.cell(0, 6, texto_blindado('Lourran Martins Fonseca'), new_x="LMARGIN", new_y="NEXT", align='C')
pdf.set_font('Helvetica', '', 11)
pdf.cell(0, 6, texto_blindado('Agente Administrativo - Mat. 19736'), new_x="LMARGIN", new_y="NEXT", align='C')
pdf.cell(0, 6, texto_blindado('Secretaria de Obras, Saneamento, Urbanismo e Conservação - PMCM'), new_x="LMARGIN", new_y="NEXT", align='C')
pdf.cell(0, 6, texto_blindado('Junho de 2026'), new_x="LMARGIN", new_y="NEXT", align='C')

# Exportar PDF
pdf_filename = "Relatorio_Iluminacao_Publica_Atualizado_Definitivo.pdf"
try:
    pdf.output(pdf_filename)
except Exception as e:
    print(f"Erro: {e}")
