import warnings
warnings.filterwarnings("ignore") # Silencia alertas de versão do FPDF

from fpdf import FPDF
import os

def texto_blindado(txt):
    """Filtra caracteres que travam a compilação do PDF"""
    if not isinstance(txt, str):
        return txt
    txt = txt.replace('—', '-').replace('–', '-').replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'")
    return txt.encode('latin-1', 'replace').decode('latin-1')

class PDF(FPDF):
    def header(self):
        # Cabeçalho com os brasões e a tarja de identificação
        if os.path.exists('brasao_pmcm.png'):
            self.image('brasao_pmcm.png', 10, 8, 25)
        if os.path.exists('sec_obras.png'):
            self.image('sec_obras.png', 170, 8, 30)
            
        self.set_y(15)
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(17, 43, 60) # Azul escuro institucional
        self.cell(0, 5, texto_blindado('Secretaria de Obras, Saneamento, Urbanismo e Conservação'), new_x="LMARGIN", new_y="NEXT", align='C')
        self.set_font('Helvetica', '', 10)
        self.cell(0, 5, texto_blindado('Município de Cachoeiras de Macacu - RJ'), new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(15)

    def footer(self):
        # Rodapé com paginação
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
            self.cell(0, 10, texto_blindado(f'[Erro: Imagem {image_name} não encontrada na pasta]'), new_x="LMARGIN", new_y="NEXT", align='C')
            self.ln(5)

# Instanciando o PDF
pdf = PDF()
pdf.add_page()

# --- CAPA E TÍTULO PRINCIPAL ---
pdf.set_font('Helvetica', 'B', 16)
pdf.set_text_color(17, 43, 60)
pdf.multi_cell(0, 8, texto_blindado('RELATÓRIO TÉCNICO CONSOLIDADO E DEFINITIVO\nAUDITORIA, EVOLUÇÃO, MANUTENÇÃO E EFICIÊNCIA DA ILUMINAÇÃO PÚBLICA'), align='C', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('Helvetica', '', 12)
pdf.multi_cell(0, 6, texto_blindado('ANÁLISE HISTÓRICA E OPERACIONAL - PARQUE GLOBAL (pG = pE + pC) - 2020-2026\nDocumento Técnico Consolidado - Junho de 2026'), align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(10)

# --- SUMÁRIO EXECUTIVO E TABELA ---
pdf.chapter_title('SUMÁRIO EXECUTIVO')
texto_sumario = (
    "O presente documento constitui a consolidação técnica definitiva da "
    "infraestrutura e da dinâmica operacional da iluminação pública do "
    "Município de Cachoeiras de Macacu, integrando os dados das duas "
    "concessionárias que operam no território: Enel (pE) e Cerci (pC). "
    "O conjunto resultante, denominado Parque Global (pG), representa a "
    "totalidade dos pontos sob responsabilidade da municipalidade.\n\n"
    "A notação adotada segue a convenção: pG = pE(Pe') + pC, onde Pe' "
    "representa a proporção de expansão da Enel. Por ausência de balizadores "
    "históricos de expansão exclusivos da Cerci no mesmo período, sua base "
    "volumétrica foi mantida como constante (4.341 pts), isolando a variável "
    "tecnológica para mensurar a eficiência energética pura."
)
pdf.chapter_body(texto_sumario)
pdf.insert_image('tabela_pg_atualizada.png', width=190)

# --- EXPANSÃO DO PARQUE (GRÁFICO DE BARRAS) ---
pdf.add_page()
pdf.chapter_title('CAPÍTULO 1 - EXPANSÃO DO PARQUE GLOBAL (2020-2026)')
texto_expansao = (
    "Com o crescimento orgânico e a regularização de novos loteamentos "
    "tracionados pela concessionária Enel, o Parque Global passa de 9.087 "
    "para 10.582 pontos físicos, consolidando a incorporação de 1.495 "
    "novos pontos homologados à rede municipal."
)
pdf.chapter_body(texto_expansao)
pdf.insert_image('barras_expansao_pg.png', width=150)

# --- MUDANÇA TECNOLÓGICA (GRÁFICO DE PIZZA) ---
pdf.chapter_title('CAPÍTULO 2 - O PANORAMA LEGADO E A TRANSIÇÃO TECNOLÓGICA')
texto_tecnologia = (
    "A consolidação dos dados de 2020 revelou um legado severo: 73,8% do "
    "Parque Global dependia de Vapor de Mercúrio, puxado pelo inventário da "
    "Cerci (que operava 86,6% nesta tecnologia obsoleta). O índice global de "
    "LED no início da década era de meros 3,1%.\n\n"
    "Aplicando o modelo de substituição exponencial para 2026, com a meta "
    "estipulada em 53,1% de eficiência, a matriz tecnológica do município "
    "sofre uma reconfiguração radical."
)
pdf.chapter_body(texto_tecnologia)
pdf.insert_image('pizza_absoluta_pg_large_fonts.png', width=190)

# --- EFEITO TESOURA (GRÁFICO DE CARGA/CONSUMO) ---
pdf.add_page()
pdf.chapter_title('CAPÍTULO 3 - IMPACTO TARIFÁRIO E O EFEITO TESOURA (pG)')
texto_consumo = (
    "O fenômeno administrativo mais notável desta gestão encontra-se no "
    "faturamento energético e na otimização da arrecadação (CIP/COSIP). A "
    "carga elétrica instalada do parque global em 2020 somava brutais "
    "1.076,8 kW.\n\n"
    "Com a substituição projetada para 5.622 luminárias LED, o município "
    "provoca um 'efeito tesoura' logístico e financeiro: o número físico "
    "de postes nas ruas cresce (+16,4%), mas a exigência sobre a rede "
    "elétrica recua para 899,0 kW e o consumo despenca de 368.737 para "
    "307.846 kWh/mês.\n\n"
    "Houve uma supressão absoluta de carga da ordem de -16,5%. Em suma, a "
    "Secretaria de Obras expandiu o parque e financiou essa expansão "
    "puramente através do ganho de eficiência técnica."
)
pdf.chapter_body(texto_consumo)
pdf.insert_image('carga_consumo_pg_corrigido.png', width=170)

# --- ESCALABILIDADE LOGÍSTICA ---
pdf.chapter_title('CAPÍTULO 4 - ESCALABILIDADE LOGÍSTICA E OPERACIONAL')
texto_logistica = (
    "A principal ruptura histórica reside na mudança do paradigma de zeladoria. "
    "A transição de um modelo essencialmente corretivo (onde o fluxo dependia "
    "exclusivamente da reclamação reativa do munícipe) para um sistema "
    "híbrido e preventivo (varreduras noturnas), gerou um crescimento de "
    "+174,6% na capacidade de manutenção de rede, saltando de 1.591 para "
    "4.368 intervenções operacionais anuais estimadas."
)
pdf.chapter_body(texto_logistica)

# =====================================================================
# CAPÍTULOS ADICIONADOS (CENSO, FGC E VICTOR HUGO)
# =====================================================================

pdf.add_page()
pdf.chapter_title('CAPÍTULO 5 - O CENSO DA CERCI (02/06) E A TAUTOLOGIA DE DADOS')
texto_tautologia = (
    "A análise do recém-chegado Censo Oficial da Cerci (02/06/2026) indica "
    "uma carga instalada contratual equivalente a 328.630 kWh/mês. Ao cruzar "
    "este dado com a fatura de consumo real da cooperativa (129.408 kWh), "
    "obteve-se uma precisão matemática com margem de erro inferior a 1%. "
    "Contudo, conforme manifestação técnica formal do Engenheiro Eletricista "
    "Victor Hugo Queiroz, esta convergência milimétrica não representa a eficiência "
    "real instalada nas ruas, mas sim uma tautologia burocrática: a Cerci "
    "emite suas faturas por estimativa de carga baseando-se estritamente "
    "neste banco de dados comercial, omitindo a modernização física já "
    "realizada em campo."
)
pdf.chapter_body(texto_tautologia)

pdf.chapter_title('CAPÍTULO 6 - A FGC ENGENHARIA E O FATURAMENTO PASSIVO RETIDO')
texto_fgc = (
    "A modernização do parque não é um mérito orgânico das concessionárias, "
    "mas uma política pública ativa custeada pelo município. A centralização "
    "da execução logística na FGC Engenharia, sob a batuta da Secretaria "
    "de Obras, Saneamento, Urbanismo e Conservação, determinou o uso majoritário "
    "de luminárias LED nas trocas e expansões.\n\n"
    "Sempre que a equipe da FGC atende a uma ocorrência, o equipamento "
    "obsoleto é removido e substituído por LED. Como a concessionária não "
    "atualiza essa alteração em seu banco de dados na velocidade necessária, "
    "o município absorve um 'Faturamento Passivo Retido', pagando por "
    "tecnologias obsoletas estimadas que já foram fisicamente substituídas "
    "nas ruas. Para dimensionar o impacto financeiro dessa inércia cadastral, "
    "as faturas de energia consolidadas totalizam R$ 264.589,67 (compostas "
    "pela fatura da Enel no valor de R$ 162.847,29 e Cerci em R$ 101.742,38)."
)
pdf.chapter_body(texto_fgc)

pdf.chapter_title('CAPÍTULO 7 - RECOMENDAÇÕES REGULATÓRIAS E DIRETRIZES')
texto_diretrizes = (
    "O relatório projetado (Meta Real de Campo: 307.846 kWh/mês) "
    "consolida-se como o Balanço Patrimonial Real do município, refletindo "
    "as ordens de serviço executadas pela FGC Engenharia. A diferença de "
    "consumo retida representa a 'gordura tarifária' a ser expurgada.\n\n"
    "Recomenda-se utilizar o diário de obras e as planilhas de instalação da "
    "FGC Engenharia como prova de campo para notificação das "
    "concessionárias, exigindo a atualização do inventário e a revisão do "
    "faturamento estimado, para que a fatura real convirja estruturalmente "
    "para os 307.846 kWh/mês já planejados."
)
pdf.chapter_body(texto_diretrizes)

# =====================================================================
# CONCLUSÃO E ASSINATURA
# =====================================================================

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
    print(f"\n=======================================================")
    print(f" SUCESSO! O relatorio foi gerado limpo e sem erros.")
    print(f" Arquivo salvo como: {pdf_filename}")
    print(f"=======================================================\n")
except PermissionError:
    print(f"\n[!] ERRO DE PERMISSAO: O arquivo '{pdf_filename}' ja esta aberto no seu computador.")
    print(f"[!] Feche o PDF no Adobe Acrobat/Navegador e rode o script novamente.\n")
except Exception as e:
    print(f"\n[!] Erro fatal ao gerar o PDF: {e}\n")

