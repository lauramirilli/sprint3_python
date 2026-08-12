# 📸 JOVI StudyLens

Protótipo em Python da JOVI StudyLens, funcionalidade desenvolvida para o smartphone JOVI voltada ao estudante em tempo integral. O sistema transforma registros fotográficos feitos em sala de aula (lousas, slides e cadernos) em material de estudo organizado, pesquisável e reutilizável, acessível pelo terminal.

> **Challenge FIAP 2026 | Sprint 3 | Python**

---

## 👥 Integrantes

| Nome | RM |
|------|----|
| Bruce Li | 569168 |
| Felipe Rorato | 570419 |
| Giovanna Andrade Parejas | 569041 |
| Laura Cardin Mirilli | 570841 |

---

## 🎯 Objetivo

Eliminar a dor do estudante que acumula fotos de aula na galeria do celular sem organização ou utilidade prática, oferecendo um fluxo estruturado de captura, armazenamento, tradução e acesso ao conteúdo.

**Fluxo:** Fotografia → IA processa → Aluno aprende

---

## ⚙️ Funcionalidades

- **Digitalizar** — registra o conteúdo de lousas, slides e cadernos com título e matéria
- **Copiar** — copia o texto de qualquer material direto para a área de transferência
- **Traduzir** — traduz conteúdos do Português para o Inglês via Google Translator, com opção de salvar na biblioteca
- **Biblioteca** — acessa, filtra por matéria, busca por palavra-chave e lê os materiais salvos

---

## 🛠️ Tecnologias utilizadas

- Python 3.12
- [deep-translator](https://pypi.org/project/deep-translator/) — tradução via Google Translator
- [pyperclip](https://pypi.org/project/pyperclip/) — copia para área de transferência
- [rich](https://pypi.org/project/rich/) - aprimora interface visual no terminal

---

## 🚀 Como instalar e rodar

**Pré-requisitos:** Python 3.10 ou superior instalado.

1. Clone o repositório:
```bash
git clone https://github.com/lauramirilli/sprint2_python.git
cd sprint2_python
```

2. Instale as dependências:

- Mac/Linux:
```bash
pip install -r requirements.txt
```
- Windows:
```bash
py -m pip install -r requirements.txt
```

3. Rode o projeto:

- Mac/Linux:
```bash
python app.py
```
- Windows:
```bash
py app.py
```

---

## 💡 Como usar

A interação é feita pelo terminal. Ao iniciar, o menu principal oferece as 4 funcionalidades. A biblioteca já conta com 3 materiais de exemplo (História, Filosofia e Matemática) para demonstração imediata.

---

## 📁 Estrutura do projeto

```
sprint2_python/
├── app.py            # Código principal
├── requirements.txt  # Dependências
└── README.md         # Documentação
```