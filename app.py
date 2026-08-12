from deep_translator import GoogleTranslator
import pyperclip

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


# DADOS GLOBAIS (simulação da base de dados em listas)

# Biblioteca de materiais digitalizados
# Estrutura: [id, titulo, materia, tipo, conteudo_texto, idioma]
materiais = [
    [1, "Brasil Colônia", "História", "lousa",
     "Período Pré-Colonial, O Governo Geral, A formação social do Brasil Colônia, A crise do sistema colonial.",
     "Português"],
    [2, "Filosofia Grega", "Filosofia", "slide",
     "Período Pré-Socrático, Período Clássico, Período Helenístico.",
     "Português"],
    [3, "Números complexos", "Matemática", "caderno",
     "Forma algébrica de um número complexo, Operações com números complexos, Plano de Argand-Gauss.",
     "Português"],
]

# Histórico de traduções realizadas na sessão
historico_traducoes = []

# Contador de ID para novos materiais
proximo_id = 4

# Saída para menu principal
saida = 'sair'

# Matérias disponíveis para organização
MATERIAS_DISPONIVEIS = [
    "Matemática", "Física", "Química", "História", "Geografia", "Filosofia", "Outro"
]

# Tipos de material reconhecidos pelo modo Estudo
TIPOS_MATERIAL = ["lousa", "slide", "caderno"]


# UTILITÁRIOS

def linha(char="─", tam=58):
    """Imprime linha separadora."""
    console.print(char * tam, style="dim cyan")


def titulo(texto, subtexto=""):
    """Imprime cabeçalho de seção."""
    corpo = f"[dim]{subtexto}[/dim]" if subtexto else ""
    console.print(Panel(
        corpo if corpo else " ",
        title=f"[bold cyan]{texto}[/bold cyan]",
        border_style="cyan",
        expand=False,
        padding=(0, 2),
    ))


def pausar():
    """Aguarda o usuário antes de voltar ao menu."""
    console.input("\n  [bold yellow]↩[/bold yellow]  Pressione ENTER para voltar ao menu...")


def input_validado(msg, tipo="str", opcoes=None, min_val=None, max_val=None, permite_sair=True):
    """
    Lê e valida entrada do usuário.
    Suporta validação de tipo inteiro, lista de opções e faixa numérica.
    """
    while True:
        entrada = console.input(f"[bold cyan]{msg}[/bold cyan]").strip()

        if not entrada:
            console.print("  [bold red]!![/bold red]  Campo obrigatório. Tente novamente.")
            continue

        if permite_sair and entrada.lower() == "sair":
            return "sair"

        if tipo == "int":
            if not entrada.lstrip("-").isdigit():
                console.print("  [bold red]!![/bold red]  Digite apenas números inteiros.")
                continue
            valor = int(entrada)
            if min_val is not None and valor < min_val:
                console.print(f"  [bold red]!![/bold red]  Valor mínimo: {min_val}.")
                continue
            if max_val is not None and valor > max_val:
                console.print(f"  [bold red]!![/bold red]  Valor máximo: {max_val}.")
                continue
            return valor

        if opcoes:
            # Aceita número ou texto da opção
            if entrada.lower() not in [str(opcao).lower() for opcao in opcoes]:
                console.print(f"  [bold red]!![/bold red]  Opções válidas: {', '.join([str(opcao) for opcao in opcoes])}.")
                continue

        return entrada


def buscar_material_por_id(id_busca):
    """Retorna o material com o ID informado, ou None se não encontrado."""
    for material in materiais:
        if material[0] == id_busca:
            return material
    return None


def exibir_conteudo_material(material):
    """Exibe o conteúdo completo de um material (mesmo formato da leitura)."""
    linha()
    console.print(f"\n    [bold cyan]{material[1]}[/bold cyan]")
    console.print(f"    [dim]{material[2]}  |  {material[3].capitalize()}  |  {material[5]}[/dim]")
    linha("-")
    console.print(f"\n  {material[4]}\n")
    linha()


def perguntar_acesso_material(lista):
    """Após exibir uma lista, oferece acesso rápido ao conteúdo de um material.
    Busca apenas dentro da lista exibida (não em toda a biblioteca) e insiste
    com a mesma pergunta até receber um ID válido ou ENTER para voltar."""
    while True:
        console.print("\n  [dim](Digite o ID para ver o conteúdo completo, ou ENTER para voltar)[/dim]")
        escolha = console.input("  ➤ ID do material: ").strip()

        if not escolha:
            return

        if not escolha.isdigit():
            console.print("\n  [bold red]!![/bold red]  ID inválido.")
            continue

        id_escolhido = int(escolha)
        material = next((m for m in lista if m[0] == id_escolhido), None)
        if not material:
            console.print(f"\n  [bold red]!![/bold red]  ID {escolha} não está nesta lista.")
            continue

        exibir_conteudo_material(material)
        return


def aviso_sair():
    """Imprime o aviso padrão de como voltar ao menu."""
    console.print('  [bold red](Digite "sair" para voltar ao menu)[/bold red]')


# FUNCIONALIDADE 1 (Digitalizar Foto de Aula)

def digitalizar_foto():
    """
    Simula a digitalização de um material fotográfico (lousa, slide,
    caderno). O usuário informa o tipo de material, a matéria e o
    conteúdo capturado. O sistema organiza e salva na biblioteca.

    Regra de negócio: o material é salvo com matéria, tipo e título
    definidos pelo estudante, tornando-o pesquisável depois.
    """
    global proximo_id

    titulo("📷  DIGITALIZAR FOTO DE AULA",
           "Registre o conteúdo capturado pela câmera")

    console.print("\n  [bold]Tipo de material fotografado:[/bold]\n")
    for i, tipo in enumerate(TIPOS_MATERIAL, 1):
        console.print(f"  [bold cyan]\\[{i}][/bold cyan] {tipo.capitalize()}")

    console.print()
    aviso_sair()
    escolha_tipo = input_validado(
        "  ➤ Tipo do material (número): ",
        tipo="int", min_val=1, max_val=len(TIPOS_MATERIAL)
    )
    if escolha_tipo == 'sair':
        return
    tipo_material = TIPOS_MATERIAL[escolha_tipo - 1]

    # Título do material
    titulo_mat = input_validado(
       f"\n  Título para este {tipo_material} (ex: 'Aula 03'): "
    )
    if titulo_mat.lower() == 'sair':
        return

    # Seleção de matéria
    console.print("\n  [bold]Matérias disponíveis:[/bold]\n")
    for i, materia in enumerate(MATERIAS_DISPONIVEIS, 1):
        console.print(f"  [bold cyan]\\[{i}][/bold cyan] {materia}")

    aviso_sair()
    escolha_mat = input_validado(
        "\n  ➤ Matéria (número): ",
        tipo="int", min_val=1, max_val=len(MATERIAS_DISPONIVEIS)
    )
    if escolha_mat == 'sair':
        return
    materia = MATERIAS_DISPONIVEIS[escolha_mat - 1]

    # Conteúdo extraído (simula o OCR/texto digitalizado)
    console.print(f"\n  Cole ou digite o texto extraído da foto ({tipo_material}):")
    console.print("  [dim](Em uma versão real, o Google Lens extrairia automaticamente da imagem)[/dim]\n")
    aviso_sair()
    conteudo = input_validado("  Conteúdo: ")
    if conteudo.lower() == 'sair':
        return

    # Salva na biblioteca
    novo_material = [proximo_id, titulo_mat, materia, tipo_material, conteudo, "Português"]
    materiais.append(novo_material)
    proximo_id += 1

    linha()
    console.print("\n [bold green]✔ Material digitalizado com sucesso![/bold green]")
    console.print(f"\n [bold]ID       :[/bold] {novo_material[0]}")
    console.print(f" [bold]Matéria  :[/bold] {materia}")
    console.print(f" [bold]Tipo     :[/bold] {tipo_material.capitalize()}")
    console.print(f" [bold]Título   :[/bold] {titulo_mat}")
    console.print(f"\n [dim]Conteúdo salvo ({len(conteudo)} caracteres).[/dim]")
    linha()

    pausar()


# FUNCIONALIDADE 2 (Copiar Conteúdo da Foto)
def copiar_conteudo():
    """
    Simula a função de copiar o conteúdo diretamente de
    imagens capturadas, facilitando o uso e reaproveitamento do conteúdo.
    """
    titulo("COPIAR CONTEÚDO")
    exibir_lista_materiais(materiais)
    aviso_sair()
    id_mat = input_validado(
        "\n  ➤ Selecione o ID do material que deseja copiar o conteúdo ",
        tipo="int", min_val=1
    )
    if id_mat == 'sair':
        return

    material = buscar_material_por_id(id_mat)
    if not material:
        console.print(f"\n  [bold red]!![/bold red]  Material ID {id_mat} não encontrado.")
        pausar()
        return

    texto = material[4]
    pyperclip.copy(texto)
    conteudo = pyperclip.paste()
    console.print(f"[bold green]Conteúdo copiado:[/bold green] {conteudo}")

    pausar()


#  FUNCIONALIDADE 3 (Traduzir Conteúdo)

def traduzir_conteudo():
    """
    Simula a tradução de texto extraído de uma foto ou de material
    já salvo na biblioteca. Suporta Português → Inglês (simulado).

    Regra de negócio: tradução preserva o contexto acadêmico;
    o resultado é salvo no histórico de traduções da sessão e
    pode ser exportado como novo material.
    """
    titulo("TRADUZIR CONTEÚDO",
           "Português → Inglês  |  +50 idiomas na versão completa")

    aviso_sair()
    console.print("\n  [bold]Fonte do texto:[/bold]\n")
    console.print("  [bold cyan]\\[1][/bold cyan] Digitar texto manualmente")
    console.print("  [bold cyan]\\[2][/bold cyan] Traduzir material da biblioteca")
    console.print()

    fonte = input_validado("  ➤ Opção: ", opcoes=["1", "2"])
    if fonte == 'sair':
        return

    texto_original = ""
    origem_titulo = "Texto avulso"

    aviso_sair()
    if fonte == "1":
        console.print("\n  Digite o texto em Português para traduzir:\n")
        texto_original = input_validado("  Texto: ")
    if texto_original == 'sair':
        return

    elif fonte == "2":
        if not materiais:
            console.print("\n  [bold red]!![/bold red]  Biblioteca vazia. Digitalize um material primeiro.")
            pausar()
            return
        exibir_lista_materiais(materiais)
        aviso_sair()
        id_mat = input_validado(
            "\n  ➤ ID do material: ",
            tipo="int", min_val=1
        )
        if id_mat == 'sair':
            return
        material = buscar_material_por_id(id_mat)
        if not material:
            console.print(f"\n  [bold red]!![/bold red]  Material ID {id_mat} não encontrado.")
            pausar()
            return
        texto_original = material[4]
        origem_titulo = material[1]

    texto_traduzido = GoogleTranslator(source='pt', target='en').translate(texto_original)

    # Exibe resultado
    linha()
    console.print(f"\n [bold cyan]ORIGINAL:[/bold cyan]\n  {texto_original}\n")
    linha("-")
    console.print(f"\n [bold green]TRADUÇÃO (EN):[/bold green]\n  {texto_traduzido}\n")
    linha()

    # Salva no histórico
    registro = {
        "origem": origem_titulo,
        "original": texto_original[:60] + ("..." if len(texto_original) > 60 else ""),
        "traduzido": texto_traduzido[:60] + ("..." if len(texto_traduzido) > 60 else ""),
    }
    historico_traducoes.append(registro)
    console.print(f"    [dim]Tradução salva no histórico ({len(historico_traducoes)} total).[/dim]")

    # Opção de salvar como novo material
    console.print("\n  Deseja salvar a tradução como novo material na biblioteca?")
    salvar = input_validado("  (s/n): ", opcoes=["s", "n", "S", "N"])

    if salvar.lower() == "s":
        global proximo_id
        novo = [
            proximo_id,
            f"[EN] {origem_titulo}",
            "Tradução",
            "documento",
            texto_traduzido,
            "English"
        ]
        materiais.append(novo)
        proximo_id += 1
        console.print(f"    [bold green]✔ Salvo na biblioteca com ID {novo[0]}.[/bold green]")

    pausar()

# FUNCIONALIDADE 4 (Biblioteca de Materiais)

def minha_biblioteca():
    """
    Exibe, busca e lê os materiais digitalizados pelo estudante.
    Resolve a dor principal: fotos perdidas na galeria misturadas
    com selfies, aqui tudo fica organizado por matéria e tipo.
    """
    titulo("MINHA BIBLIOTECA",
           "Seus materiais de estudo organizados")

    if not materiais:
        console.print("\n    [dim]Biblioteca vazia. Digitalize uma foto primeiro.[/dim]\n")
        pausar()
        return

    console.print("\n  [bold cyan]\\[1][/bold cyan] Ver todos os materiais")
    console.print("  [bold cyan]\\[2][/bold cyan] Filtrar por matéria")
    console.print("  [bold cyan]\\[3][/bold cyan] Buscar por palavra-chave")
    console.print("  [bold cyan]\\[4][/bold cyan] Ler conteúdo de um material")
    console.print("  [bold cyan]\\[5][/bold cyan] Resumo de um material")
    console.print()

    aviso_sair()
    opc = input_validado("  ➤ Opção: ", opcoes=["1", "2", "3", "4", "5"])
    if opc == 'sair':
        return

    # Ver todos
    if opc == "1":
        exibir_lista_materiais(materiais)
        perguntar_acesso_material(materiais)
        return

    # Filtrar por matéria
    elif opc == "2":
        console.print("\n  [bold]Matérias disponíveis na biblioteca:[/bold]\n")
        # Coleta matérias únicas dos materiais salvos
        materias_salvas = list({material[2] for material in materiais})
        for i, material in enumerate(materias_salvas, 1):
            console.print(f"  [bold cyan]\\[{i}][/bold cyan] {material}")

        aviso_sair()
        escolha = input_validado(
            "\n  ➤ Número da matéria: ",
            tipo="int", min_val=1, max_val=len(materias_salvas)
        )
        if escolha == 'sair':
            return
        materia_filtro = materias_salvas[escolha - 1]
        filtrados = [material for material in materiais if material[2] == materia_filtro]
        console.print(f"\n  [bold]Materiais de '{materia_filtro}':[/bold]")
        exibir_lista_materiais(filtrados)
        perguntar_acesso_material(filtrados)
        return

    # Buscar por palavra-chave
    elif opc == "3":
        aviso_sair()
        termo = input_validado("\n  Palavra-chave para busca: ").lower()
        if termo == 'sair':
            return
        encontrados = [
            material for material in materiais
            if termo in material[1].lower() or termo in material[4].lower()
        ]
        if encontrados:
            console.print(f"\n  [bold]{len(encontrados)} resultado(s) para '{termo}':[/bold]")
            exibir_lista_materiais(encontrados)
            perguntar_acesso_material(encontrados)
        else:
            console.print(f"\n    [dim]Nenhum material encontrado com '{termo}'.[/dim]")
            pausar()
        return

    # Ler conteúdo
    elif opc == "4":
        exibir_lista_materiais(materiais)
        aviso_sair()
        id_leitura = input_validado(
            "\n  ➤ ID do material para ler: ",
            tipo="int", min_val=1
        )
        if id_leitura == 'sair':
            return
        material = buscar_material_por_id(id_leitura)
        if material:
            linha()
            console.print(f"\n    [bold cyan]{material[1]}[/bold cyan]")
            console.print(f"    [dim]{material[2]}  |  {material[3].capitalize()}  |  {material[5]}[/dim]")
            linha("-")
            console.print(f"\n  {material[4]}\n")
            linha()
        else:
            console.print(f"\n  [bold red]!![/bold red]  Material ID {id_leitura} não encontrado.")

    elif opc == "5":
        console.print("[dim]Para esse protótipo estão disponivéis apenas os resumos dos conteúdos de exemplo![/dim]")
        exibir_lista_materiais(materiais[:3])
        aviso_sair()
        id_leitura = input_validado(
            "\n  ➤ ID do material para resumir: ",
            tipo="int", min_val=1, max_val=3
        )
        if id_leitura == 'sair':
            return
        material = buscar_material_por_id(id_leitura)

        if material[0] == 1:
            console.print("    [bold]Brasil Colônia:[/bold] Período de exploração por Portugal (1500–1822), "
            "baseado na extração de recursos e trabalho escravizado.")

        elif material[0] == 2:
            console.print("    [bold]Filosofia grega:[/bold] Busca racional por explicações sobre o mundo, o conhecimento e a ética, "
            "com pensadores como Sócrates, Platão e Aristóteles.")

        elif material[0] == 3:
            console.print("    [bold]Números complexos:[/bold] Conjunto numérico que inclui a unidade imaginária (i), "
            "permitindo representar raízes de números negativos.")


    pausar()


def exibir_lista_materiais(lista):
    """Função auxiliar para exibir tabela de materiais."""
    tabela = Table(border_style="dim cyan", header_style="bold cyan", show_lines=False)
    tabela.add_column("ID", width=5)
    tabela.add_column("TÍTULO", width=32)
    tabela.add_column("MATÉRIA", width=22)
    tabela.add_column("TIPO")
    for m in lista:
        tabela.add_row(str(m[0]), m[1][:31], m[2][:21], m[3].capitalize())
    console.print(tabela)
    console.print(f"  Total: [bold]{len(lista)}[/bold] material(is).")


#  MENU PRINCIPAL

def exibir_menu():
    """Renderiza o menu principal com estatísticas da sessão."""
    titulo("📸  JOVI Study Lens",
           "Transforme imagens em conhecimento")
    console.print(f"  [bold]Biblioteca:[/bold] {len(materiais)} material(is)  |  "
          f"[bold]Traduções:[/bold] {len(historico_traducoes)}\n")
    console.print("  [bold cyan]\\[1][/bold cyan] Digitalizar")
    console.print("  [bold cyan]\\[2][/bold cyan] Copiar")
    console.print("  [bold cyan]\\[3][/bold cyan] Traduzir")
    console.print("  [bold cyan]\\[4][/bold cyan] Biblioteca de Conteúdos")
    console.print("  [bold red]\\[0][/bold red] Sair")
    linha()


def main():
    """Ponto de entrada, loop principal do programa."""
    console.print("\n[bold cyan]" + "═" * 58 + "[/bold cyan]")
    console.print("  [bold]JOVI Study Lens  📸  Transforme imagens em conhecimento[/bold]")
    console.print("  [dim]Challenge FIAP 2026 | Sprint 3 | Python[/dim]")
    console.print("[bold cyan]" + "═" * 58 + "[/bold cyan]")
    console.print("\n  Bem-vindo! 3 materiais de exemplo já estão na biblioteca.")

    while True:
        console.print()
        exibir_menu()

        opcao = input_validado(
            "  ➤ Escolha uma opção: ",
            tipo="int", min_val=0, max_val=5
        )

        match opcao:
            case 1:
                digitalizar_foto()
            case 2:
                copiar_conteudo()
            case 3:
                traduzir_conteudo()
            case 4:
                minha_biblioteca()
            case 0:
                linha("═")
                console.print("  [bold green]Até logo! Continue transformando fotos em aprendizado. 📸[/bold green]")
                linha("═")
                break


#  PONTO DE ENTRADA

if __name__ == "__main__":
    main()