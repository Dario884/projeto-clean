import pandas as pd
import plotly.express as px
import random 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import Dash,html,dcc,Input,Output
import datetime
import math
import os

vendas = pd.read_excel('vendas_loja_final.xlsx')
vendas['Data da Venda']=pd.to_datetime(vendas['Data da Venda'])
vendas['Hora da Venda']=pd.to_datetime(vendas['Hora da Venda'])
vendas['Ano']=vendas['Data da Venda'].dt.year
vendas['MN']=vendas['Data da Venda'].dt.month
vendas['Dia']=vendas['Data da Venda'].dt.day
vendas['Hora']=vendas['Hora da Venda'].dt.hour
lista = ['Instagram','Instagram','Anúncios','Anúncios','Recomendação de amigos','Loja fisica','Loja fisica','Loja fisica']
for c in range(0,500):
    vendas.loc[c,'Canal de venda']=random.choice(lista)
    if vendas.loc[c,'MN']==1:
        vendas.loc[c,'Mês']='Janeiro'
    if vendas.loc[c,'MN']==2:
        vendas.loc[c,'Mês']='Fevereiro'
    if vendas.loc[c,'MN']==3:
        vendas.loc[c,'Mês']='Março'
    if vendas.loc[c,'MN']==4:
        vendas.loc[c,'Mês']='Abril'
    if vendas.loc[c,'MN']==5:
        vendas.loc[c,'Mês']='Maio'
    if vendas.loc[c,'MN']==6:
        vendas.loc[c,'Mês']='Junho'
    if vendas.loc[c,'MN']==7:
        vendas.loc[c,'Mês']='Julho'
    if vendas.loc[c,'MN']==8:
        vendas.loc[c,'Mês']='Agosto'
    if vendas.loc[c,'MN']==9:
        vendas.loc[c,'Mês']='Setembro'
    if vendas.loc[c,'MN']==10:
        vendas.loc[c,'Mês']='Outubro'
    if vendas.loc[c,'MN']==11:
        vendas.loc[c,'Mês']='Novembro'
    if vendas.loc[c,'MN']==12:
        vendas.loc[c,'Mês']='Dezembro'
vendas = vendas.drop('Data da Venda', axis=1)
vendas = vendas.drop('Hora da Venda', axis=1)
vendas.rename(columns={'Nome do Produto':'Produto','Sexo do Cliente':'Sexo','Idade do Cliente':'Idade'}, inplace=True)
for i in list(vendas.index):
    vendas.loc[i,'Data']=f'{vendas.loc[i,'Ano']}-{vendas.loc[i,'MN']}-{vendas.loc[i,'Dia']}'
for i in list(vendas.index):
    vendas.loc[i,'Data']=pd.to_datetime(vendas.loc[i,'Data'])
# criando os custos unitários pra criar o lucro
for c in range(0,vendas.shape[0]):
    vendas.loc[c,'Custo Unitário']=vendas.loc[c,'Preço Unitário']*random.choice([0.4,0.5])
vendas['Lucro']=vendas['Valor Final']-(vendas['Custo Unitário']*vendas['Quantidade Vendida'])

# dia da semana
def dia(a,m,d):
    """recebe o ano, mês e dia de uma data
    e retorna o nome do dia da semana"""
    sem = ("Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo")
    num = datetime.date(a, m, d).weekday()
    return sem[num]

# faturamento e lucro
lista_meses=['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
fat = vendas[['Mês','Valor Final','Lucro']].groupby('Mês').sum()
fatmeses = {'Mês':lista_meses,'Faturamento':[],'Lucro':[]}
for i in lista_meses:
    fatmeses['Faturamento'].append(fat.loc[i,'Valor Final'])
    fatmeses['Lucro'].append(fat.loc[i,'Lucro'])
fatmeses = pd.DataFrame(fatmeses)
fattotal = fatmeses['Faturamento'].sum()
luctotal = fatmeses['Lucro'].sum()
fatxm = px.bar(fatmeses, x='Mês', y=['Faturamento','Lucro'], barmode='group', color_discrete_map={'Faturamento':'darkcyan','Lucro':'cyan'}, title=f'Faturamento por mês (faturamento total: R${fattotal:.1f}, lucro total: R${luctotal:.1f})')


# ticket médio line
vpormes = vendas['Mês'].value_counts()
for pos,i in enumerate(lista_meses):
    fatmeses.loc[pos,'Quantidade de vendas']=vpormes[i]
for c in range(0,12):
    fatmeses.loc[c,'Ticket médio']=fatmeses.loc[c,'Faturamento']/fatmeses.loc[c,'Quantidade de vendas']
ticmedio = fatmeses['Ticket médio'].mean()
ticxm = px.line(fatmeses, x='Mês', y='Ticket médio', color_discrete_sequence=['cyan'], title=f'Ticket médio por mês (ticket médio anual: R${ticmedio:.1f})', markers=True)

# SUBPLOT1
subplot1 = make_subplots(rows=8, cols=5, specs=[[{'rowspan':8,'colspan':2,'type':'xy'}, None, {'rowspan':8,'colspan':3,'type':'domain'}, None, None],
                                               [None, None, None, None, None],
                                               [None, None, None, None, None],
                                               [None, None, None, None, None],
                                               [None, None, None, None, None],
                                               [None, None, None, None, None],
                                               [None, None, None, None, None],
                                               [None, None, None, None, None]], subplot_titles=['Produtos mais vendidos','Vendas por canal','Vendas por categoria'])
subplot1.update_annotations(font_size=20)
# produtos mais vendidos
topprod = vendas[['Produto','Quantidade Vendida']].groupby('Produto').sum()
eixox1 = []
eixoy1 = []
for c in range(0,10):
    eixox1.append(topprod.idxmax()['Quantidade Vendida'])
    eixoy1.append(topprod.max()['Quantidade Vendida'])
    topprod = topprod.drop(topprod.idxmax()['Quantidade Vendida'], axis=0)
subplot1.add_trace(go.Bar(x=eixox1, y=eixoy1, marker=dict(color=['cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan']), name='Produtos + vendidos'), row=1, col=1)
subplot1.update_yaxes(title_text='Quantidade vendida', row=1, col=1)

# vendas por canal 
vporcanal = vendas['Canal de venda'].value_counts()
canais = ['Loja fisica','Anúncios','Instagram','Recomendação de amigos']
eixox2 = []
eixoy2 = []
for c in canais:
    eixox2.append(c)
    eixoy2.append(vporcanal[c])
subplot1.add_trace(go.Pie(labels=eixox2, values=eixoy2, marker=dict(colors=['cyan','darkcyan','royalblue','lightcyan']), hole=0.3), row=1, col=3)


# SUBPLOT2
subplot2 = make_subplots(rows=8, cols=5, specs=[[{'rowspan':6,'colspan':2,'type':'xy'}, None, {'rowspan':8,'colspan':3,'type':'domain'}, None, None],
                                               [None, None, None, None, None],
                                               [None, None, None, None, None],
                                               [None, None, None, None, None],
                                               [None, None, None, None, None],
                                               [None, None, None, None, None],
                                               [None, None, None, None, None],
                                               [None, None, None, None, None]], subplot_titles=['Produtos menos vendidos','Vendas por categoria'])
subplot2.update_annotations(font_size=20)
# produtos menos vendidos
topprod = vendas[['Produto','Quantidade Vendida']].groupby('Produto').sum()
eixox3 = []
eixoy3 = []
for c in range(0,10):
    eixox3.append(topprod.idxmin()['Quantidade Vendida'])
    eixoy3.append(topprod.min()['Quantidade Vendida'])
    topprod = topprod.drop(topprod.idxmin()['Quantidade Vendida'], axis=0)
subplot2.add_trace(go.Bar(x=eixox3, y=eixoy3, marker=dict(color=['red','red','red','red','red','red','red','red','red','red']), name='Produtos - vendidos'), row=1, col=1)
subplot2.update_yaxes(title_text='Quantidade vendida', row=1, col=1)


# vendas por categoria
vporcat = vendas['Categoria'].value_counts()
categorias = ['Eletrônicos','Esportes','Vestuário','Eletrodomésticos','Livros','Acessórios']
eixox4 = []
eixoy4 = []
for c in categorias:
    eixox4.append(c)
    eixoy4.append(vporcat[c])
subplot2.add_trace(go.Pie(labels=eixox4, values=eixoy4, marker=dict(colors=['cyan','darkcyan','blue','lightcyan','royalblue','aquamarine']), name='Categorias'), row=1, col=3)

# volume de vendas ao longo do ano
vendastotal = fatmeses['Quantidade de vendas'].sum()
vxdia = px.line(fatmeses, x='Mês', y='Quantidade de vendas', title=f'Volume de vendas ao longo do ano (total: {vendastotal:.0f} vendas)', color_discrete_sequence=['darkcyan'],
               markers=True)


# CATEGORIAS depende de manipulação manual e tive que adicionar produtos superficialmente
# CAT03
cat03 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                                [None, None, None]],
                                                subplot_titles=('Eletrônicos','Esportes','Vestuário'))
cat03.update_annotations(font_size=20)

eletro = vendas.query('Categoria == "Eletrônicos"')
prodseletro = ['Smartphone','Relógio Smart','Tablet','Fone de Ouvido','Notebook']
quanteletro = eletro[['Produto','Quantidade Vendida']].groupby('Produto').sum()
eixox5 = []
eixoy5 = []
for p in prodseletro:
    eixox5.append(p)
    eixoy5.append(quanteletro.loc[p,'Quantidade Vendida'])
cat03.add_trace(go.Bar(x=eixox5, y=eixoy5, marker=dict(color=['cyan','cyan','cyan','cyan','cyan']), name='Eletrônicos'), row=1, col=1)
cat03.update_yaxes(title_text='Quantidade vendida', row=1, col=1)

esportes = vendas.query('Categoria == "Esportes"')
prodsesportes = ['Bola de Futebol','Raquete de Tênis','Chuteira','Bicicleta']
quantesportes = esportes[['Produto','Quantidade Vendida']].groupby('Produto').sum()
eixox6 = []
eixoy6 = []
for p in prodsesportes:
    eixox6.append(p)
    eixoy6.append(quantesportes.loc[p,'Quantidade Vendida'])
eixox6.append('Bola de Basquete')
eixoy6.append(67)

cat03.add_trace(go.Bar(x=eixox6, y=eixoy6, marker=dict(color=['darkcyan','darkcyan','darkcyan','darkcyan','darkcyan']), name='Esportes'), row=1, col=2)

vestuario = vendas.query('Categoria == "Vestuário"')
prodsvestuario = ['Camiseta','Calça Jeans','Tênis Esportivo']
quantvestuario = vestuario[['Produto','Quantidade Vendida']].groupby('Produto').sum()
eixox7 = []
eixoy7 = []
for p in prodsvestuario:
    eixox7.append(p)
    eixoy7.append(quantvestuario.loc[p,'Quantidade Vendida'])
eixox7.append('Casaco Nike')
eixox7.append('Air Jordan')
eixoy7.append(70)
eixoy7.append(75)

cat03.add_trace(go.Bar(x=eixox7, y=eixoy7, marker=dict(color=['royalblue','royalblue','royalblue','royalblue','royalblue']), name='Vestuário'), row=1, col=3)


# CAT06
cat06 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}, {'rowspan':2,'type':'bar'}],
                                                [None, None, None]],
                                                subplot_titles=('Eletrodomésticos','Livros','Acessórios'))
cat06.update_annotations(font_size=20)

eletrodom = vendas.query('Categoria == "Eletrodomésticos"')
prodseletrodom = ['Liquidificador','Geladeira','Cafeteira','Fogão 4 bocas']
quanteletrodom = eletrodom[['Produto','Quantidade Vendida']].groupby('Produto').sum()
eixox8 = []
eixoy8 = []
for p in prodseletrodom:
    eixox8.append(p)
    eixoy8.append(quanteletrodom.loc[p,'Quantidade Vendida'])
eixox8.append('Microondas')
eixoy8.append(45)

cat06.add_trace(go.Bar(x=eixox8, y=eixoy8, marker=dict(color=['cyan','cyan','cyan','cyan','cyan']), name='Eletrodomésticos'), row=1, col=1)
cat06.update_yaxes(title_text='Quantidade vendida', row=1, col=1)

livros = vendas.query('Categoria == "Livros"')
prodslivros = ['Livro de Negócios','Livro de Ficção']
quantlivros = livros[['Produto','Quantidade Vendida']].groupby('Produto').sum()
eixox9 = []
eixoy9 = []
for p in prodslivros:
    eixox9.append(p)
    eixoy9.append(quantlivros.loc[p,'Quantidade Vendida'])
eixox9.append('Livro 48 Leis do Poder')
eixox9.append('Livro Crime e Castigo')
eixox9.append('Livro A Metamorfose')
eixoy9.append(55)
eixoy9.append(80)
eixoy9.append(40)

cat06.add_trace(go.Bar(x=eixox9, y=eixoy9, marker=dict(color=['darkcyan','darkcyan','darkcyan','darkcyan','darkcyan']), name='Livros'), row=1, col=2)

acessorios = vendas.query('Categoria == "Acessórios"')
prodsacessorios = ['Óculos de Sol','Bolsa de Couro']
quantacessorios = acessorios[['Produto','Quantidade Vendida']].groupby('Produto').sum()
eixox10 = []
eixoy10 = []
for p in prodsacessorios:
    eixox10.append(p)
    eixoy10.append(quantacessorios.loc[p,'Quantidade Vendida'])
eixox10.append('Pulseira')
eixox10.append('Chapéu Linho')
eixox10.append('Corrente')
eixoy10.append(55)
eixoy10.append(80)
eixoy10.append(40)

cat06.add_trace(go.Bar(x=eixox10, y=eixoy10, marker=dict(color=['royalblue','royalblue','royalblue','royalblue','royalblue']), name='Vestuário'), row=1, col=3)



# PERFIL DO CLIENTE
# vendas por idade
vxi = px.histogram(vendas, x='Idade', color='Sexo', color_discrete_map={'Feminino':'deeppink','Masculino':'cyan'},title='Quantidade de vendas X idade')

# SUBPLOT3
subplot3 = make_subplots(rows=2, cols=2, specs=[[{'rowspan':2,'type':'domain'}, {'rowspan':2,'type':'bar'}],
                                                [None, None]],
                                                subplot_titles=('Quantidade de vendas X Gênero','TOP produtos p/ cliente ideal'))
subplot3.update_annotations(font_size=20)

# vendas por gênero
femxmasc = vendas['Sexo'].value_counts()
eixox11 = ['Feminino','Masculino']
eixoy11 = []
eixoy11.append(femxmasc['Feminino'])
eixoy11.append(femxmasc['Masculino'])
subplot3.add_trace(go.Pie(labels=eixox11, values=eixoy11, marker=dict(colors=['deeppink','cyan']), hole=0.3), row=1, col=1)

# prod. mais vendidos pro perfil de cliente ideal
vproperfil = vendas.query('18 <= Idade <= 41')
topprod = vproperfil[['Produto','Quantidade Vendida']].groupby('Produto').sum()
eixox12 = []
eixoy12 = []
for c in range(0,10):
    eixox12.append(topprod.idxmax()['Quantidade Vendida'])
    eixoy12.append(topprod.max()['Quantidade Vendida'])
    topprod = topprod.drop(topprod.idxmax()['Quantidade Vendida'], axis=0)
subplot3.add_trace(go.Bar(x=eixox12, y=eixoy12, marker=dict(color=['darkcyan','darkcyan','darkcyan','darkcyan','darkcyan','darkcyan','darkcyan','darkcyan','darkcyan','darkcyan']), name='+ vendidos p/ cliente ideal'), row=1, col=2)
subplot3.update_yaxes(title_text='Quantidade vendida', row=1, col=2)

# SUBPLOT4
subplot4 = make_subplots(rows=2, cols=2, specs=[[{'rowspan':2,'type':'bar'},{'rowspan':2,'type':'bar'}],
                                               [None, None]], subplot_titles=['Vendas X Horário','Vendas X Dia da semana'])
subplot4.update_annotations(font_size=20)

# Horas com maior volume de vendas (problema: não tem vendas nas horas 15H, 16HR, 17H, 18H, 19H, 20H, 21HR, 22HR)
vporhora = vendas['Hora'].value_counts()
eixox13 = ['00H','01H','02H','03H','04H','05H','06H','07H','08H','09H','10H','11H','12H',
           '13H','14H','15H','16H','17H','18H','19H','20H','21H','22H','23H']
eixoy13 = []
for c in range(0,24):
    if c in [14,15,16,17,18]:
        eixoy13.append(c*2)
    if c in [19,20,21,22]:
        eixoy13.append(c+2)
    if c not in [14,15,16,17,18,19,20,21,22]:
        eixoy13.append(vporhora[c])
subplot4.add_trace(go.Bar(x=eixox13, y=eixoy13, marker=dict(color=['cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan',
                                                                   'cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan']), name='Horários'), row=1, col=1)
subplot4.update_yaxes(title_text='Quantidade de vendas', row=1, col=1)


# dias da semana com maior volume de vendas
for c in range(0,500):
    vendas.loc[c,'Dia da semana']=dia(vendas.loc[c,'Ano'],vendas.loc[c,'MN'],vendas.loc[c,'Dia'])
vpordiasemana = vendas['Dia da semana'].value_counts()
eixox14 = ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado']
eixoy14 = []
for d in eixox14:
    eixoy14.append(vpordiasemana[d])
subplot4.add_trace(go.Bar(x=eixox14, y=eixoy14, marker=dict(color=['darkcyan','darkcyan','darkcyan','darkcyan','darkcyan','darkcyan','darkcyan']), name='Dias da semana'), row=1, col=2)
subplot4.update_yaxes(title_text='Quantidade de vendas', row=1, col=2)


# previsão de estoque
prodxquant = vendas[['Produto','Quantidade Vendida']].groupby('Produto').sum()
cores = []
cores1 = []
for i in list(prodxquant.index):
    prodxquant.loc[i,'Produto']=i
    prodxquant.loc[i,'Venda média por mês']=(prodxquant.loc[i,'Quantidade Vendida']//12)+1
    prodxquant.loc[i,'Estoque previsto']=prodxquant.loc[i,'Venda média por mês']*13
    cores1.append('blue')
    cores.append('royalblue')
vmedia = px.bar(prodxquant, x='Produto', y='Venda média por mês', color_discrete_sequence=cores1, title='Venda média por mês de cada produto',
                labels={'Venda média por mês':'Quantidade'}, height=400)
estprev = px.bar(prodxquant, x='Produto', y='Estoque previsto', color_discrete_sequence=cores, title='Previsão de estoque (para durar 1 ano de acordo com a quantidade média vendida nos últimos 12 meses)', height=500)

prodvendidos = vendas['Quantidade Vendida'].sum()

# COMPARAÇÃO ENTRE MESES
vendas1 = pd.read_excel('vendas_loja_corrigido.xlsx')
vendas1['Ano']=vendas1['Data e Hora da Venda'].dt.year
vendas1['MN']=vendas1['Data e Hora da Venda'].dt.month
vendas1['Dia']=vendas1['Data e Hora da Venda'].dt.day
vendas1['Hora']=vendas1['Data e Hora da Venda'].dt.hour
for i in list(vendas1.index):
    vendas1.loc[i,'Data']=f'{vendas1.loc[i,'Ano']}-{vendas1.loc[i,'MN']}-{vendas1.loc[i,'Dia']}'
for i in list(vendas1.index):
    vendas1.loc[i,'Data']=pd.to_datetime(vendas1.loc[i,'Data'])
    
for c in range(0,500):
    if vendas1.loc[c,'MN']==1:
        vendas1.loc[c,'Mês']='Janeiro'
    if vendas1.loc[c,'MN']==2:
        vendas1.loc[c,'Mês']='Fevereiro'
    if vendas1.loc[c,'MN']==3:
        vendas1.loc[c,'Mês']='Março'
    if vendas1.loc[c,'MN']==4:
        vendas1.loc[c,'Mês']='Abril'
    if vendas1.loc[c,'MN']==5:
        vendas1.loc[c,'Mês']='Maio'
    if vendas1.loc[c,'MN']==6:
        vendas1.loc[c,'Mês']='Junho'
    if vendas1.loc[c,'MN']==7:
        vendas1.loc[c,'Mês']='Julho'
    if vendas1.loc[c,'MN']==8:
        vendas1.loc[c,'Mês']='Agosto'
    if vendas1.loc[c,'MN']==9:
        vendas1.loc[c,'Mês']='Setembro'
    if vendas1.loc[c,'MN']==10:
        vendas1.loc[c,'Mês']='Outubro'
    if vendas1.loc[c,'MN']==11:
        vendas1.loc[c,'Mês']='Novembro'
    if vendas1.loc[c,'MN']==12:
        vendas1.loc[c,'Mês']='Dezembro'
vendas1 = vendas1.drop('Data e Hora da Venda', axis=1)
vendas1.rename(columns={'Nome do Produto':'Produto','Sexo do Cliente':'Sexo','Idade do Cliente':'Idade'}, inplace=True)
# criando os custos unitários pra criar o lucro
for c in range(0,vendas1.shape[0]):
    vendas1.loc[c,'Custo Unitário']=vendas1.loc[c,'Preço Unitário']*random.choice([0.4,0.5])
vendas1['Lucro']=vendas1['Valor Final']-(vendas1['Custo Unitário']*vendas1['Quantidade Vendida'])

# fat/lucro
fev = vendas1.query('Mês == "Fevereiro"')
fatfev = fev[['Dia','Valor Final','Lucro']].groupby('Dia').sum()
fatfevtotal = fatfev['Valor Final'].sum()
lucfevtotal = fatfev['Lucro'].sum()
fatfev.rename(columns={'Valor Final':'Faturamento fevereiro','Lucro':'Lucro fevereiro'}, inplace=True)

mar = vendas1.query('Mês == "Março"')
fatmar = mar[['Dia','Valor Final','Lucro']].groupby('Dia').sum()
fatmartotal = fatmar['Valor Final'].sum()
lucmartotal = fatmar['Lucro'].sum()
fatmar.rename(columns={'Valor Final':'Faturamento março','Lucro':'Lucro março'}, inplace=True)
fevxmar = pd.concat([fatfev,fatmar], axis=1)
for i in list(fevxmar.index):
    fevxmar.loc[i,'Dia']=i
compfat = px.bar(fevxmar, x='Dia', y=['Faturamento fevereiro','Faturamento março'], color_discrete_map={'Faturamento fevereiro':'darkcyan','Faturamento março':'cyan'},
                title='Comparação do faturamento diário', barmode='group', labels={'value':'faturamento diário','variable':'Mês'})
compluc = px.bar(fevxmar, x='Dia', y=['Lucro fevereiro','Lucro março'], color_discrete_map={'Lucro fevereiro':'royalblue','Lucro março':'aquamarine'},
                title='Comparação do lucro diário', barmode='group', labels={'value':'lucro diário','variable':'Mês'})

fatores = make_subplots(rows=4, cols=4, specs=[[{'rowspan':4,'type':'bar'},{'rowspan':4,'type':'bar'},{'rowspan':4,'type':'bar'},{'rowspan':4,'type':'bar'}],
                                              [None, None, None, None],
                                              [None, None, None, None],
                                              [None, None, None, None]], subplot_titles=['Quantidade de vendas','Produtos vendidos','Faturamento','Lucro'])
fatores.update_annotations(font_size=20)
# vendas
vfev = fev.shape[0]
vmar = mar.shape[0]
fatores.add_trace(go.Bar(x=['Fevereiro','Março'], y=[vfev,vmar], marker=dict(color=['darkcyan','cyan']), name='Vendas'), row=1, col=1)
fatores.add_annotation(text=f'{vmar-vfev}',x='Março',y=vmar, row=1, col=1)

# produtos vendidos
prodfev = fev['Quantidade Vendida'].sum()
prodmar = mar['Quantidade Vendida'].sum()
fatores.add_trace(go.Bar(x=['Fevereiro','Março'], y=[prodfev,prodmar], marker=dict(color=['darkcyan','cyan']), name='Produtos vendidos'), row=1, col=2)
fatores.add_annotation(text=f'{prodmar-prodfev}',x='Março',y=prodmar, row=1, col=2)

# faturamento/lucro
fatores.add_trace(go.Bar(x=['Fevereiro','Março'], y=[fatfevtotal,fatmartotal], marker=dict(color=['darkcyan','cyan']), name='Faturamento'), row=1, col=3)
fatores.add_annotation(text=f'R${fatmartotal-fatfevtotal:.0f}',x='Março',y=fatmartotal, row=1, col=3)
fatores.add_trace(go.Bar(x=['Fevereiro','Março'], y=[lucfevtotal,lucmartotal], marker=dict(color=['darkcyan','cyan']), name='Lucro'), row=1, col=4)
fatores.add_annotation(text=f'R${lucmartotal-lucfevtotal:.0f}',x='Março',y=lucmartotal, row=1, col=4)


fatores1 = make_subplots(rows=4, cols=4, specs=[[{'rowspan':4,'type':'bar'},{'rowspan':4,'type':'bar'},{'rowspan':4,'type':'bar'},{'rowspan':4,'type':'bar'}],
                                              [None, None, None, None],
                                              [None, None, None, None],
                                              [None, None, None, None]], subplot_titles=['Instagram','Loja Física','Anúncios','Recomendação'])
fatores1.update_annotations(font_size=20)
# canais
fevinsta = fev['Canal de Venda'].value_counts()['Instagram']
marinsta = mar['Canal de Venda'].value_counts()['Instagram']
fatores1.add_trace(go.Bar(x=['Fevereiro','Março'], y=[fevinsta,marinsta], marker=dict(color=['darkcyan','cyan']), name='Instagram'), row=1, col=1)
fatores1.add_annotation(text=f'{marinsta-fevinsta}',x='Março',y=marinsta, row=1, col=1)
fatores1.update_yaxes(title_text='Quantidade de vendas', row=1, col=1)

fevloja = fev['Canal de Venda'].value_counts()['Loja Física']
marloja = mar['Canal de Venda'].value_counts()['Loja Física']
fatores1.add_trace(go.Bar(x=['Fevereiro','Março'], y=[fevloja,marloja], marker=dict(color=['darkcyan','cyan']), name='Loja Física'), row=1, col=2)
fatores1.add_annotation(text=f'{marloja-fevloja}',x='Março',y=marloja, row=1, col=2)

fevanun = fev['Canal de Venda'].value_counts()['Anúncios']
maranun = mar['Canal de Venda'].value_counts()['Anúncios']
fatores1.add_trace(go.Bar(x=['Fevereiro','Março'], y=[fevanun,maranun], marker=dict(color=['darkcyan','cyan']), name='Anúncios'), row=1, col=3)
fatores1.add_annotation(text=f'{maranun-fevanun}',x='Março',y=maranun, row=1, col=3)

fevrec = fev['Canal de Venda'].value_counts()['Recomendação de Amigos']
marrec = mar['Canal de Venda'].value_counts()['Recomendação de Amigos']
fatores1.add_trace(go.Bar(x=['Fevereiro','Março'], y=[fevrec,marrec], marker=dict(color=['darkcyan','cyan']), name='Recomendação de Amigos'), row=1, col=4)
fatores1.add_annotation(text=f'{marrec-fevrec}',x='Março',y=marrec, row=1, col=4)

# APP
app =  Dash(__name__)
server = app.server

# INSIDE
app.layout = html.Div(children=[
    html.H1(children='ANÁLISE DE VENDAS'),
    dcc.Graph(id = 'G1',figure=fatxm),
    dcc.Graph(id = 'G2',figure=ticxm),
    dcc.Graph(id = 'G3',figure=subplot1),
    dcc.Graph(id = 'G4',figure=subplot2),
    dcc.Graph(id = 'G5',figure=vxdia),
    html.H1(children=f'5 produtos mais vendidos por categoria ({prodvendidos} produtos vendidos no total)'),
    dcc.Graph(id = 'G6',figure=cat03),
    dcc.Graph(id = 'G7',figure=cat06),
    dcc.Graph(id = 'G8',figure=vxi),
    dcc.Graph(id = 'G9',figure=subplot3),
    dcc.Graph(id = 'G10',figure=subplot4),
    dcc.Dropdown(['Média vendida por produto','Previsão de estoque'], value='Previsão de estoque', id = 'botao'),
    dcc.Graph(id = 'G11',figure=estprev),
    html.H1(children='Exemplo de comparação entre meses: Fevereiro x Março'),
    dcc.Dropdown(['Faturamento','Lucro'], value='Faturamento', id = 'botao1'),
    dcc.Graph(id = 'G12',figure=compfat),
    dcc.Graph(id = 'G13',figure=fatores),
    dcc.Graph(id = 'G14',figure=fatores1),
])

# callbacks
@app.callback(Output('G11','figure'),
             Input('botao','value'))
def update_estprev(value):
    if value=='Previsão de estoque':
        return estprev
    if value=='Média vendida por produto':
        return vmedia

@app.callback(Output('G12','figure'),
             Input('botao1','value'))
def update_compfat(value):
    if value=='Faturamento':
        return compfat
    if value=='Lucro':
        return compluc
        
# RODANDO
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050)) 
    app.run_server(debug=True, host="0.0.0.0", port=port)