import tabula
import pandas as pd
import csv
import zipfile

# Lendo todas as páginas do PDF
print("Extraindo dados do PDF... Aguarde.")
lista_tabelas = tabula.read_pdf("Anexo_I_Rol_2021RN_465.2021_RN654.2025L.pdf", pages="all", lattice=True)

# Unindo todas as tabelas em uma só
df = pd.concat(lista_tabelas, ignore_index=True)

# Remove as quebras de linha (\r ou \n) dos nomes das colunas
df.columns = [col.replace('\r', ' ').replace('\n', ' ').strip() for col in df.columns]

# Remove as linhas que repetem o título (Indexação booleana)
nome_coluna = df.columns[0]
df = df[df[nome_coluna] != nome_coluna]

# Substitui as quebras de linha dentro das células por um espaço
df = df.replace(r'[\r\n]+', ' ', regex=True)

# Substituição das siglas (uso do \b para garantir a palavra exata)
siglas = {r'\bOD\b': 'Odontologia',
          r'\bAMB\b': 'Ambulatorial'
          }
df = df.replace(siglas, regex=True)

# Gerando o CSV
print("Salvando arquivos finais...")
nome_csv = "Teste_Jefferson_Anexo_I.csv"

df.to_csv(nome_csv,
          index=False,
          sep=',',
          encoding='utf-8-sig',
          quoting=csv.QUOTE_ALL
          )

# Gerando o ZIP
with zipfile.ZipFile("Teste_Jefferson.zip", "w") as z:
    z.write(nome_csv)

print("✅ Processo concluído!")