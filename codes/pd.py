import pandas as pd

# Carregar o arquivo Excel
arquivo_excel = 'docs/grade_curricular.xlsx'  # substitua pelo nome do seu arquivo
df = pd.read_excel(arquivo_excel)

# Filtrar as linhas que queremos manter
df_filtrado = df[~df['periodo_ideal'].isin(['disciplinas optativas', 'extensão']) & df['periodo_ideal'].notna()]

# Salvar o novo DataFrame em um novo arquivo Excel
df_filtrado.to_excel('docs/grade_curricular_filtrada.xlsx', index=False)
