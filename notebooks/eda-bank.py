# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

# %%
bank = pd.read_csv('../data/bank-additional.csv')
bank

# %%
#visualizo brevemente formatos de las variables 
bank.info()

# %%
#visualizo los valores nulos en proporción al total de cada variable 
bank.isnull().sum() / len(bank)*100

# %%
#forma alternativa para lo ver valores nulos
bank.isna().sum() / (bank.shape[0])*100

# %%
#chequeo que no haya duplicados 
bank.duplicated().sum()

# %%
#importo el otro archivo a trabajar (un xlsx complementario a mi base de datos csv)
customer = pd.read_excel('../data/unified-customer-details.xlsx')
customer 

# %%
#creo una copia del dataframe original para trabajar en ella
bank_df = bank.copy()

# %%
#renombro la columna 'id_' para que coincida con la columna 'ID' del dataframe 'customer' y así poder unificar ambos dataframe en uno solo 
bank_df.rename(columns={'id_': 'ID'}, inplace='True')
bank_df.head(3)

# %%
#unifico los dos dataframes 'bank_df' y 'customer' para tener toda la información de ambas bases de datos 
df = bank_df.merge(customer, how='left', on= 'ID')

# %%
df.sample(5)

# %%
#creo un diccionario para renombrar las etiquetas de columnas en español
nuevos_nombres = {
    'Unnamed: 0_x':'ref_x',
    'age':'edad',
    'job':'empleo',
    'marital':'estado_civil',
    'education':'nivel_educativo',
    'default':'morosidad',
    'housing':'hipoteca',
    'loan':'prestamos',
    'contact':'via_contacto',
    'duration':'duracion_llam',
    'campaign':'num_llam',
    'pdays':'dias_ult.llam',
    'previous':'num_llam.camp.previa',
    'poutcome':'result_camp.previa',
    'emp.var.rate':'variacion_empleo',
    'cons.price.idx':'id_precio.cons',
    'cons.conf.idx':'id_confza.cons',
    'euribor3m':'tasa_interes.3m',
    'nr.employed':'id_empleado',
    'y':'prod.serv_susc',
    'date':'fecha_llam',
    'latitude':'latitud',
    'longitude':'longitud',
    'contact_month':'mes_llam',
    'contact_year':'año_llam',
    'ID':'id_ref',
    'Unnamed: 0_y':'ref_y',
    'Income':'ingreso_anual',
    'Kidhome':'num_niños.hogar',
    'Teenhome':'num_joven.hogar',
    'Dt_Customer':'fecha_incio.cliente',
    'NumWebVisitsMonth':'num.visitas.web_mes'
}

# %%
#aplico el diccionario creado 
df.rename(columns= nuevos_nombres, inplace= True)

# %%
print(df.columns)

# %%
#visualizo mi dataframe ahora
df.head(5)

# %%
#creo otro diccionario para modificar los datos de la columna 'empleo' a español
empleos_espanol = {
    'housemaid':'emp.doméstica',
    'services':'servicios',
    'admin.':'administrativo',
    'blue-collar':'obrero',
    'entrepreneur':'emprendedor',
    'management':'directivo',
    'retired':'jubilado',
    'self-employed':'autónomo',
    'student':'estudiante',
    'technician':'técnico',
    'unemployed':'desempleado'
    }

# %%
#ejecuto el diccionario
df['empleo'] = df['empleo'].replace(empleos_espanol)

# %%
#cambio el contenido de 'estado_civil' a español 
df['estado_civil'] = df['estado_civil'].replace({'SINGLE':'soltero/a', 'MARRIED':'casado/a', 'DIVORCED':'divorciado/a'}, regex=True)

# %%
#creo otro diccionario para cambiar y aclarar la información de la columna 'nivel_educativo' 
clasifico_educativo = {
    'basic.4y':'basico.(4años)',
    'basic.6y':'basico.(6años)',
    'basic.9y':'basico.(9años)',
    'high.school':'secundaria',
    'illiterate':'analfabeto/a',
    'professional.course':'form_profesional',
    'university.degree':'universitario'
}

# %%
#ejecuto el diccionario 
df['nivel_educativo'] = df['nivel_educativo'].replace((clasifico_educativo), regex=True)

# %%
#Ídem para la columna 'via_contacto'
df['via_contacto'] = df['via_contacto'].replace({'telephone':'telefono', 'cellular':'móvil'}, regex=True)

# %%
#ídem para la columna 'resultado de campaña previa'
df['result_camp.previa'] = df['result_camp.previa'].replace({'NONEXISTENT':'inexistente', 'FAILURE':'sin_exito', 'SUCCESS':'exitosa'}, regex=True)

# %%
#otro vistazo a mi dataframe hasta aquí
df.sample(5)

# %%
#observo los estadísticos principales de mi dataframe
df.describe()

# %%
#observo los formatos de las variables
df.info()

# %%
#observo la cantidad de nulos en proporción a cada varibale y luego comienzo el tratamiento (imputación) de los mismo
df.isnull().sum() / len(df)*100

# %%
#comienzo con la variable 'morosidad', para ello visualizo sus valores
print(df['morosidad'].value_counts())

# %%
#dado que observo solo 3 clientes morosos, adopto la no morosidad como Status-Quo y completo los nulos con ceros
df['morosidad'] = df['morosidad'].fillna(0)

# %%
#para la varibale edad, visualizo moda, mediana y media y luego procedo a completar los nulos
media_edad = df['edad'].mean()
mediana_edad = df['edad'].median()
moda_edad = df['edad'].mode()[0]

print(f'Media: {media_edad}')
print(f'Mediana: {mediana_edad}')
print(f'Moda: {moda_edad}')

# %%
#completo los nulos con la mediana (que es más robusta) y no se ve afectada por valores extremos (como algunos pocos clientes de +90 años)
df['edad'] = df['edad'].fillna(mediana_edad)

# %%
#chequeo que no hayan nulos para 'edad' 
df['edad'].isnull().sum()

# %%
#limpio y adapto la columna 'tasa_interes.3m' para trabajar correctamente con pandas
df['tasa_interes.3m'] = df['tasa_interes.3m'].astype(str).str.replace(',', '.')

# %%
#convierto a formato float manteniendo los nulos ('coerce' asegura que los nulos sigan siendo NaN)
df['tasa_interes.3m'] = pd.to_numeric(df['tasa_interes.3m'], errors='coerce')

# %%
df.info()

# %%
#para 'tasa_interes.3m' decido hacer una imputación aplicando el método de "interpolación lineal" con los valores adyacentes. Pero para esto, los valores deben estar ordenados por fecha.
#entonces procedo a formatear la fecha al inglés y luego ordernar por esa varibale
meses_es_en = { 
    'enero': 'Jan',
    'febrero': 'Feb',
    'marzo': 'Mar', 
    'abril': 'Apr',
    'mayo': 'May',
    'junio': 'Jun',
    'julio': 'Jul',
    'agosto': 'Aug',
    'septiembre': 'Sep',
    'octubre': 'Oct',
    'noviembre': 'Nov',
    'diciembre': 'Dec'
}

# %%
#aplico el diccionario a la columna 'fecha_llam'
df['fecha_llam'] = df['fecha_llam'].replace(meses_es_en, regex = True)

# %%
#convierto a formato 'datetime' (formato: Dia-Mes-Año)
df['fecha_llam'] = pd.to_datetime(df['fecha_llam'], format= '%d-%b-%Y', errors='coerce')

# %%
#ordeno el dataframe cronológicamente por fecha
df = df.sort_values(by='fecha_llam')

# %%
df.head(5)

# %%
#ahora sí, para 'tasa_interes.3m' relleno los nulos con función 'interpolate' haciendo una pequeña interpolación lineal para cada uno de los nulos con sus valores adyacentes (en otras palabras es una media entre datos vecinos)
df['tasa_interes.3m'] = df['tasa_interes.3m'].interpolate(method='linear')

# %%
#chequeo rápidamente como quedó la columna
print('Valores más frecuentes:')
print(df['tasa_interes.3m'].value_counts().head(10))

print(f'Cantidad de nulos: {df['tasa_interes.3m'].isnull().sum()}')

# %%
#visualizo un poco el dataframe (utilizando la extensión "Data Wrangler" de Microsoft) que es muy amigable para ir controlando los resultados 
df.sample(8)

# %%
#observo los valores nulos que aún tengo en mi dataframe 
df.isnull().sum() / len(df)*100

# %%
#continúo con los nulos de 'nivel_educativo' y decido hacer para esta variable una imputación condicional a la variable 'empleo' (dado la relación que suponen ambas). Ej: alguien que trabaje como directivo tendría un nivel educativo alto y un obrero uno más bajo
nulos_antes = df['nivel_educativo'].isnull().sum()
print(f'Nulos en nivel_educativo previo a la imputación: {nulos_antes}')

# %%
#calculo la moda de 'nivel_educativo' para cada tipo de empleo (de los valores que sí existen) y con eso imputaré los faltantes del nivel educativo. Aplico lambda para obtener la moda para cada grupo de 'empleo'
modas_por_empleo = df.groupby('empleo')['nivel_educativo'].apply(lambda x: x.mode()[0] if not x.mode().empty else None)

# %%
#lo convierto a un dataframe para visualizarlo
tabla_visual = modas_por_empleo.reset_index()
tabla_visual.columns = ['Tipo de Empleo', 'Nivel Educativo más común']

display(tabla_visual)

# %%
#completo los nulos mapeando con tal información
df['nivel_educativo'] = df['nivel_educativo'].fillna(df['empleo'].map(modas_por_empleo))

# %%
#compruebo que no haya nulos
print(f'Nulos después del tratamiento: {df['nivel_educativo'].isnull().sum()}')

# %%
#consto que aún hay 135 valores nulos (se debe a que en la columna 'empleo' también hay nulos). 
#Entonces ahora completaré los nulos de 'empleo' y para eso haré el mismo procedimiento pero a la inversa: rellenar los nulos de 'empleo' condicionado a los valores más frecuentes del nivel educativo.
#calculo entonces el empleo más común para cada nivel_educativo
modas_por_educacion = df.groupby('nivel_educativo')['empleo'].apply(lambda x: x.mode()[0] if not x.mode().empty else None)

# %%
#visualizo el nuevo dataframe
tabla_visual_inversa = modas_por_educacion.reset_index()
tabla_visual_inversa.columns = ['Nivel Educativo', 'Empleo más frecuente']

display(tabla_visual_inversa)

# %%
#chequeo la cantidad de nulos existentes previo al tratamiento
print(f'Cantidad de nulos de "empleo" antes: {df['empleo'].isnull().sum()}')

# %%
#procedo a completar los nulos de 'empleo' mapeando con los valores obtenidos
df['empleo'] = df['empleo'].fillna(df['nivel_educativo'].map(modas_por_educacion))

# %%
#chequeo ahora la cantidad de nulos (pos tratamiento)
print(f'Cantidad de nulos de "empleo" despues: {df['empleo'].isnull().sum()}')

# %%
#chequeo nuevamente un panorama general de nulos:
df.isnull().sum()

# %%
#me encuentro en que hay 135 nulos restantes tanto para empleo como nivel_educativo (son nulos coincidentes) y en este punto haré lo siguiente:
#para cada variable (empleo y nivel_educativo) aplicaré una imputación condicional a la edad (por separado para cada variable) por ejemplo en el caso del empleo; buscaré el empleo más frecuente según la edad de ese cliente. Y para la educación buscaré el nivel_educativo más frecuente según la edad de ese cliente.

modas_empleo_por_edad = df.groupby('edad')['empleo'].apply(lambda x: x.mode()[0] if not x.mode().empty else None)
modas_educ_por_edad = df.groupby('edad')['nivel_educativo'].apply(lambda x: x.mode()[0] if not x.mode().empty else None)


# %%
#completo entonces con el mapeo según la edad
df['empleo'] = df['empleo'].fillna(df['edad'].map(modas_empleo_por_edad))

df['nivel_educativo'] = df['nivel_educativo'].fillna(df['edad'].map(modas_educ_por_edad))

# %%
#verifico la cantidad de nulos
nulos_empleo = df['empleo'].isnull().sum()
nulos_educ = df['nivel_educativo'].isnull().sum()

print(f'Cantidad de Nulos de "empleo": {nulos_empleo}')
print(f'Cantidad de Nulos "nivel_educativo": {nulos_educ}')

# %%
#ahora para los nulos de 'estado_civil' completo según el siguiente supuesto: si 'num_niños.hogar' = 0 y 'num_joven.hogar' = 0 será 'soltero/a' y si 'num_niños.hogar' > 0 o 'num_joven.hogar' > 0 será 'casado/a'
es_nulo = df['estado_civil'].isnull()

condicion_soltero = (df['num_niños.hogar'] == 0) & (df['num_joven.hogar'] == 0)
condicion_casado = (df['num_niños.hogar'] > 0) | (df['num_joven.hogar'] > 0)

# %%
#imputo los nulos aaplicando las condiciones usando loc
df.loc[es_nulo & condicion_soltero, 'estado_civil'] = 'soltero/a'
df.loc[es_nulo & condicion_casado, 'estado_civil'] = 'casado/a'

# %%
#verifico como quedó la columna 'estado_civil'
print(f'Cant Nulos de "estado_civil": {df['estado_civil'].isnull().sum()}')

# %%
#antes de continuar completando valores nulos, reviso el formato de las variables de mi dataframe
df.info()

# %%
#veo que algunas variables tienen formato string cuando deberían tener numérico (id_precio.cons, id_confza.cons y id_empleado) por lo que reemplazo las comas por puntos y luego le doy el formato adecuado (float64), eso facilita a pandas trabajar correctamente
df['id_precio.cons'] = df['id_precio.cons'].astype(str).str.replace(',', '.')
df['id_precio.cons'] = pd.to_numeric(df['id_precio.cons'], errors = 'coerce')

df['id_confza.cons'] = df['id_confza.cons'].astype(str).str.replace(',', '.')
df['id_confza.cons'] = pd.to_numeric(df['id_confza.cons'], errors = 'coerce')

df['id_empleado'] = df['id_empleado'].astype(str).str.replace(',', '.')
df['id_empleado'] = pd.to_numeric(df['id_empleado'], errors = 'coerce')

# %%
#para los nulos de Índice de precios al consumidor 'id_precio.cons' visualizo previamente la media y la mediana:
media_precio = df['id_precio.cons'].mean()
mediana_precio = df['id_precio.cons'].median()

print(f'La Media para "id_precio.cons" es: {media_precio}')
print(f'La Mediana para "id_precio.cons" es: {mediana_precio}')

# %%
#completo los nulos con la media dado que esta variable tiene los datos muy concentrados
df['id_precio.cons'] = df['id_precio.cons'].fillna(media_precio)

# %%
#chequeo los nulos pos-imputación
print(f'Cantidad de nulos: {df['id_precio.cons'].isnull().sum()}')

# %%
#para los nulos de las variables 'hipoteca' y 'prestamos' podría imputarlos condicionado a la variable 'ingreso_anual' dado que las hipotecas y prestamos en gral se relacionan con el ingreso, pero el desarrollo sería algo complejo y aún así sesgaría un poco los datos. Por lo tanto, decido imputar de forma conservadora asignandole 'Desconocido' o bien un '-1' para mantener el formato 'int' de la variable.
print(f'Cantidad de nulos de "hipoteca" previo a la imputación: {df['hipoteca'].isnull().sum()}')
print(f'Cantidad de nulos de "prestamos" previo a la imputación: {df['prestamos'].isnull().sum()}')

# %%
#procedo a imputar con "-1" categorizando así valores "desconocidos"
df[['hipoteca', 'prestamos']] = df[['hipoteca', 'prestamos']].fillna(-1)

# %%
#chequeo la imputación anterior:
print(f'Cantidad de nulos de "hipoteca" pos-imputación: {df['hipoteca'].isnull().sum()}')
print(f'Cantidad de nulos de "prestamos" pos-imputación: {df['prestamos'].isnull().sum()}')

# %%
#chequeo los nulos restantes
df.isnull().sum()

# %%
#para los nulos de 'fecha_llam' voy a visualizar algunas columnas que pueden estar relacionadas:
desplego_columnas = ['num_llam', 'prod.serv_susc', 'fecha_llam']

#visualizo solo las filas donde la fecha es nula
df_nulos_fecha = df[df['fecha_llam'].isnull()][desplego_columnas]

display(df_nulos_fecha.head(20))

# %%
display(df_nulos_fecha.sample(20))

# %%
#luego de observar las columnas (sin encontrar correlaciones claras) decido imputar los nulos con el método Forward Fill (que rellena el nulo con el valor anterior a este, es decir haciendo un forward del valor existente al faltante).
#pero antes de aplicarlo, debo volver el dataframe a su orden original (dado que para imputar 'tasa_interes.3m' lo ordené cronológicamente por fecha). Lo reordeno meiante la columna 'ref_x'
df = df.sort_values(by='ref_x')

# %%
#verifico el orden 
df.head(5)

# %%
#ahora aplico el método Forward Fill (ffill)
df['fecha_llam'] = df['fecha_llam'].ffill()

# %%
#chequeo la cantidad de nulos para todo el dataframe
df.isnull().sum()

# %%
df.isna().sum()

# %%
#antes de continuar, transformo la varibale "prod.serv_susc" de string a numérica para facilitar operaciones con pandas
df['prod.serv_susc'] = df['prod.serv_susc'].map({'no': 0, 'yes': 1})

# %%
#verifico la transformación
print(df['prod.serv_susc'].value_counts())
print(f'Tipo de dato: {df['prod.serv_susc'].dtype}')

# %%
#chequeo los nulos 
nulos = df['prod.serv_susc'].isna().sum()
print(f"Cantidad de valores nulos: {nulos}")

# %%
#chequeo nuevamente los formatos de las variables
df.info()

# %%
#adapto los formatos de las variables "edad", "morosidad", "hipoteca" y "prestamos"  al formato 'int64'
columnas_a_int = ['edad', 'morosidad', 'hipoteca', 'prestamos']
df[columnas_a_int] = df[columnas_a_int].astype('int64')

# %%
#chequeo el nuevo formato
df.info()

# %%
#ahora para para facilitar la estadística descriptiva de mi dataframe crearé nuevas columnas segmentadoras: 
#creo una nueva columna que muestre la duración de la última llamada en minutos
df['duracion_llam_min'] = round(df['duracion_llam'] / 60, 2)

# %%
#creo una nueva columna que muestra la antigüedad del cliente al momento de la llamada:
diferencia_dias = (df['fecha_llam'] - df['fecha_incio.cliente']).dt.days
df['antiguedad_anos'] = round(diferencia_dias / 365.25, 1)

# %%
#verifico valores de las nuevas columnas 
df[['duracion_llam_min', 'antiguedad_anos']].head(5)

# %%
#creo una nueva columna para segmentar el nivel_educativo
diccionario_educacion = {
    'analfabeto/a': 'Bajo',
    'basico.(4años)': 'Bajo',
    'basico.(6años)': 'Bajo',
    'basico.(9años)': 'Bajo',
    'secundaria': 'Medio',
    'form_profesional': 'Medio',
    'universitario': 'Alto'
}

df['cat_nivel_educativo'] = df['nivel_educativo'].map(diccionario_educacion)

# %%
#segmento ahora el ingreso_anual utilizando cuartiles 
etiquetas_ingreso = {'Bajo', 'Medio-Bajo', 'Medio-Alto', 'Alto'}
df['cat_ingreso_anual'] = pd.qcut(df['ingreso_anual'], q=4, labels = etiquetas_ingreso)

# %%
#visualizo valores de las nuevas columnas 
df[['cat_nivel_educativo', 'cat_ingreso_anual']].sample(8)

# %%
#segmento el número de visitas web mensuales
def categorias_visitas(visitas):
    if visitas <= 10:
        return 'Baja'
    elif visitas <= 20:
        return 'Media'
    else:
        return 'Alta'
    
df['frec_consultas_web'] = df['num.visitas.web_mes'].apply(categorias_visitas)

# %%
#renombro columna para ser más descriptivo 
df = df.rename(columns={'antiguedad_anos': 'antiguedad_cliente_anos'})

# %%
print(df.columns)

# %%
#renombro otra columna para profesionalizar y estandarizar un poco el código 
df = df.rename(columns={'num_niños.hogar': 'num_ninos.hogar'})

# %%
print(df.columns)

# %%
#creo una segmentación según la composición familiar del cliente
def definir_tamano_familia(fila):
    total_menores = fila['num_ninos.hogar'] + fila['num_joven.hogar']
    
    if total_menores <= 2:
        return 'Pequena'
    elif total_menores == 3:
        return 'Mediana'
    else:
        return 'Grande'
    
df['tamano_familia'] = df.apply(definir_tamano_familia, axis= 1)

# %%
df['tamano_familia'].sample(5)

# %%
#comienzo con mi Análisis Descriptivo de los datos (con visualizaciones), pero antes un primer pantallazo general:
df.describe().T

# %%
#comienzo a explorar la distribución de algunas variables y luego pasaré a una exploración más analíticas de las variables de interés. 
#configuro previamente estilo del gráfico 
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))

#Gráfico 1: Histograma de la Edad con curva de densidad
sns.histplot(data=df, x='edad', kde=True, color='skyblue', bins=30)

#personalizo etiquetas
plt.title('Distribución por Edad de los Clientes', fontsize=14, pad=15)
plt.xlabel('Edad (Años)', fontsize=12)
plt.ylabel('Frecuencia (Número de Clientes)', fontsize=12)

plt.show()

# %%
#Gráfico 2: Frecuencias del Empleo
plt.figure(figsize=(10, 7))

#ordeno los valores de mi variable "Empleo" para mejor visualización
order_empleo = df['empleo'].value_counts().index

#gráfico de frecuencias
sns.countplot(data=df, y='empleo', order=order_empleo, palette='viridis')

#etiquetas
plt.title('Perfil Laboral de la Cartera de Clientes', fontsize=14, pad=15)
plt.xlabel('Cantidad de Clientes', fontsize=12)
plt.ylabel('Ocupación / Sector', fontsize=12)

plt.show()

# %%
#Gráfico 3: Distribución de Nivel Educativo
plt.figure(figsize=(10, 6))

#ordeno la variable "Nivel Educativo" para mejor visualización
order_edu = df['nivel_educativo'].value_counts().index

#gráfico de frecuencias
ax = sns.countplot(data=df, x='nivel_educativo', order=order_edu, palette='magma')

#giro las etiquetas del eje "x" por ser nombres largos
plt.xticks(rotation=45)
#etiquetas
plt.title('Distribución por Nivel Educativo', fontsize=14, pad=15)
plt.xlabel('Grado Académico', fontsize=12)
plt.ylabel('Cantidad de Clientes', fontsize=12)

plt.show()

# %%
#visualizo el porcentaje de clientes en cada segmento del ingreso
dist_ingresos = df['cat_ingreso_anual'].value_counts(normalize=True).sort_index() * 100
print("Distribución de clientes por segmento de ingresos:")
print(dist_ingresos.round(2))

# %%
#el resultado anterior muestra que los grupos poblacionales de la segmentación del Ingreso están perfectamente distribuidos (logrado con 'qcut' previamente). Esto permitirá obtener un resultado más fiel (con sesgo bajo) a la hora de un análisis bivariado, por ej: cómo impacta cada segmento del ingreso en la variable objetivo de "Suscribir Producto/Servicio" bancario.

#Represento la Distribución del Ingreso Anual en un diagrama de caja (boxplot):
#configuro estilo del gráfico
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 3))

#Gráfico 4: Boxplot Ingreso Anual
sns.boxplot(data=df, x='ingreso_anual', color='mediumseagreen', width=0.4)

#personalizo etiquetas
plt.title('Dispersión y Detección de Valores Atípicos en el Ingreso Anual', fontsize=14, pad=10)
plt.xlabel('Ingreso Anual', fontsize=12)

plt.show()

# %%
#Represento la Distribución del Ingreso continuo para ver la distribución más detallada:
#configuro el estilo
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))

#Gráfico 5: Distribución del Ingreso Anual (el parámetro "bins" agrupa el ingreso en 40 "cajones" para rmayor detalle)
sns.histplot(data=df, x='ingreso_anual', kde=True, bins=40, color='royalblue')

#personalizo etiquetas
plt.title('Distribución Continua del Ingreso Anual de los Clientes', fontsize=14, pad=15)
plt.xlabel('Ingreso Anual', fontsize=12)
plt.ylabel('Frecuencia (Cantidad de Clientes)', fontsize=12)
#agrego una línea punteada para marcar la Mediana (el cliente "del medio")
mediana_ingreso = df['ingreso_anual'].median()
plt.axvline(mediana_ingreso, color='red', linestyle='--', label=f'Mediana: {mediana_ingreso:,.0f}')
plt.legend()

plt.tight_layout() #ajuste del layout
plt.show()

# %%
#Gráfico 6: Éxito de la Suscripción
plt.figure(figsize=(3, 5))

sns.countplot(data=df, x='prod.serv_susc', palette='viridis')
plt.title('Resultado de la Campaña (0=No, 1=Si)')

# %%
#Gráfico 7: Distribución de la Duración de llamadas
plt.figure(figsize=(10, 6))
sns.set_theme(style="whitegrid")

#visualizo Histograma de la duración de llamadas
sns.histplot(data=df, x='duracion_llam_min', bins=30, kde=True, color='coral')

#etiquetas
plt.title('Distribución del Tiempo de Llamada', fontsize=15, pad=20)
plt.xlabel('Duración (Minutos)', fontsize=12)
plt.ylabel('Cantidad de Clientes Contactados', fontsize=12)

plt.show()

# %%
#Comparativa del Ingreso Anual (continuo) según Suscripción del Producto/Servicio bancario, intentando averiguar si el producto es de consumo masivo o está ligado a la capacidad económica.

#Gráfico 8: Ingreso Anual - Suscripción (boxplots)
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))

#Boxplot comparativo (2 cajas): para los que dijeron "No" (0) y los que dijeron "Si" (1)
sns.boxplot(data=df, x='prod.serv_susc', y='ingreso_anual', palette='Set1', width=0.5)

#etiquetas
plt.title('¿Influye el nivel de ingreso en la decisión de suscripción?', fontsize=14)
plt.xlabel('Suscripción al Producto (0 = No, 1 = Sí)', fontsize=12)
plt.ylabel('Ingreso Anual', fontsize=12)
plt.xticks([0, 1], ['No Suscrito', 'Suscrito'])

plt.show()

# %%
#Chequeo los valores exactos del diagrama anterior (ingreso promedio de los que se suscribieron vs los que no) para especificar en mi informe
resumen_ingreso_exito = df.groupby('prod.serv_susc')['ingreso_anual'].agg(['mean', 'median', 'std']).round(2)
print(resumen_ingreso_exito)

# %%
#Analizo la contingencia (normalizada) entre el Nivel Educativo y la Contratación de un Servicio/Producto (visualizo la proporción en cada nivel educativo)
tabla_educacion = pd.crosstab(df['cat_nivel_educativo'], df['prod.serv_susc'], normalize='index') * 100
print("Composición porcentual (No vs Si) por nivel educativo:")
display(tabla_educacion.round(2))

#Gráfico 9: Suscripción por Nivel Educativo (visualización de barras apiladas: Stacked Bar Chart)
tabla_educacion.plot(kind='bar', stacked=True, figsize=(10, 6), color=["#c54f4fff","#3455af"])
plt.title('Proporción de Suscripción por Nivel Educativo')
plt.legend(['No Suscrito (0)', 'Suscrito (1)'], loc='upper right')
plt.ylabel('Porcentaje (%)')
plt.show()

# %%
#Gráfico 10: Boxplot Número de llamadas
sns.set_theme(style="whitegrid")
plt.figure(figsize=(5, 6))

#visualizo Boxplot
sns.boxplot(data=df, x='prod.serv_susc', y='num_llam', palette='Blues', hue='prod.serv_susc', legend=False)

plt.title('Distribución de Contactos por Resultado', fontsize=13, pad=15)
plt.xlabel('¿Se suscribió?', fontsize=11)
plt.ylabel('Número de veces contactado', fontsize=11)
plt.xticks([0, 1], ['No', 'Sí'])
plt.show()

# %%
#Análisis bivariado entre la Cantidad de llamadas y Suscripción al Producto/Servicio.
#previamente filtro hasta 10 llamadas
df_filtrado = df[df['num_llam'] <= 10]
tasa_exito_llam = df_filtrado.groupby('num_llam')['prod.serv_susc'].mean() * 100

#Gráfico 11: Tasa de Èxito: busco punto de saturación. (utilizo barplot de seaborn) 
ax = sns.barplot(x=tasa_exito_llam.index, y=tasa_exito_llam.values, color='skyblue')

#añado porcentajes sobre las barras
for p in ax.patches:
    ax.annotate(f'{p.get_height():.1f}%', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='bottom', fontsize=10, xytext=(0, 5),
                textcoords='offset points')
    
plt.title('Tasa de Éxito (%) según Número de Contactos', fontsize=13, pad=15)
plt.xlabel('Número de llamada', fontsize=11)
plt.ylabel('% de Suscripción', fontsize=11)
plt.ylim(0, tasa_exito_llam.max() + 5)
plt.show()

# %%
#Análisis bivariado entre Duración de las llamadas y Suscripción del Prod/Servicio (éxito de la campaña). Busco determinar si el tiempo de la llamada es predictor del éxito de la campaña o no.
plt.figure(figsize=(10, 6))

#Gráfico 12: Violin-Plot combina un Boxplot con la densidad (KDE). Muestra dónde está "el grueso" de las llamadas exitosas
sns.violinplot(data=df, x='prod.serv_susc', y='duracion_llam_min', palette='viridis', split=True)

#etiquetas
plt.title('Densidad y Dispersión del Tiempo de Conversación', fontsize=14)
plt.xlabel('¿Se suscribió? (0=No, 1=Sí)', fontsize=12)
plt.ylabel('Duración de la llamada (Minutos)', fontsize=12)

plt.tight_layout()
plt.show()

# %%
#valores numéricos de la eficiencia comercial (para el gráfico anterior)
analisis_eficiencia = df.groupby('prod.serv_susc').agg({
    'num_llam': ['mean', 'median', 'max'],
    'duracion_llam_min': ['mean', 'median', 'max']
    }).round(2)

print("Métricas de Esfuerzo Comercial por Resultado:")
display(analisis_eficiencia)

# %%
#visualización complementaria para el Análisis bivariado entre Duración de las llamadas y Suscripción del Prod/Servicio.
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

#Gráfico 13 (izquierda): Dispersión del tiempo de la llamada
sns.boxplot(data=df, x='prod.serv_susc', y='duracion_llam_min', 
            palette='Set2', hue='prod.serv_susc', legend=False, ax=axes[0])

axes[0].set_title('Dispersión y Mediana del Tiempo de Llamada', fontsize=14, pad=15)
axes[0].set_xlabel('Decisión Final (0 = No, 1 = Sí)', fontsize=12)
axes[0].set_ylabel('Duración de la Llamada (Minutos)', fontsize=12)
axes[0].set_xticks([0, 1])
axes[0].set_xticklabels(['No Suscrito', 'Suscrito'])

#Gráfico 14 (derecha): Densidad del tiempo de la llamada (KDE plot), muestra dónde se concentra la mayor masa de clientes para cada resultado.
sns.kdeplot(data=df, x='duracion_llam_min', hue='prod.serv_susc', 
            fill=True, common_norm=False, palette='Set2', alpha=0.5, 
            linewidth=2, ax=axes[1])

axes[1].set_title('Densidad: ¿Dónde se concentra la conversión?', fontsize=14, pad=15)
axes[1].set_xlabel('Duración de la Llamada (Minutos)', fontsize=12)
axes[1].set_ylabel('Densidad (Proporción de Clientes)', fontsize=12)

plt.tight_layout()
plt.show()

# %%
#cálculo de las métricas clave (para el gráfico anterior)
resumen_duracion = df.groupby('prod.serv_susc')['duracion_llam_min'].agg(
    Promedio='mean',
    Mediana='median',
    Desv_Estandar='std',
    Max_Minutos='max'
).round(2)

resumen_duracion.index = ['0 - No Suscrito', '1 - Suscrito']
print("Impacto del Tiempo en la Decisión de Suscribir (en minutos):")
display(resumen_duracion)

# %%
#Gráfico 15: Heatmap de Carga Financiera al momento de Suscripción Prod/Serv. Busco averiguar qué peso tienen los prestamos e hipotecas a la hora de suscribir un Prod/Serv.
#primero creo una tabla dinámica (Pivot Table) con (prod.serv_susc) en valores, en filas: hipoteca y en columnas: prestamos
pivot_deuda = df.pivot_table(
    values='prod.serv_susc', 
    index='hipoteca', 
    columns='prestamos', 
    aggfunc='mean'
) * 100

#visualizo heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(pivot_deuda, annot=True, cmap='YlGnBu', fmt=".2f", cbar_kws={'label': 'Tasa de Suscripción (%)'})

#etiquetas (asumiendo 0=No, 1=Sí)
plt.title('Impacto de la Carga Financiera en la Suscripción de Prod/Serv', fontsize=14, pad=15)
plt.xlabel('¿Tiene Préstamos?', fontsize=12)
plt.ylabel('¿Tiene Hipoteca?', fontsize=12)
plt.xticks([0.5, 1.5], ['No', 'Sí'])
plt.yticks([0.5, 1.5], ['No', 'Sí'])

plt.tight_layout()
plt.show()

# %%
#Análisis comparativo entre Campañas de Marketing: Actual vs Previa.
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

#Gráfico 16: Campaña Actual (número de llamadas vs éxito actual)
sns.boxplot(data=df, x='prod.serv_susc', y='num_llam', 
            palette='Blues', hue='prod.serv_susc', legend=False, ax=axes[0])

axes[0].set_title('Campaña Actual: Esfuerzo vs. Éxito', fontsize=14, pad=15)
axes[0].set_xlabel('Suscripción Actual (0 = No, 1 = Sí)', fontsize=12)
axes[0].set_ylabel('Contactos Realizados (Campaña Actual)', fontsize=12)
axes[0].set_xticks([0, 1])
axes[0].set_xticklabels(['No Suscrito', 'Suscrito'])

#Gráfico 17: Campaña Previa (número de llamadas previas vs resultado previo)
sns.boxplot(data=df, x='result_camp.previa', y='num_llam.camp.previa', 
            palette='viridis', hue='result_camp.previa', legend=False, ax=axes[1])

axes[1].set_title('Campaña Previa: Esfuerzo vs. Resultado', fontsize=14, pad=15)
axes[1].set_xlabel('Resultado de la Campaña Previa', fontsize=12)
axes[1].set_ylabel('Contactos Realizados (Campaña Previa)', fontsize=12)

plt.tight_layout()
plt.show()

# %%
#complemento el gráfico con porcentajes del resultado de cada campaña:
print('Resultados CAMPAÑA ACTUAL (prod.serv_susc)')
actual_pct = df['prod.serv_susc'].value_counts(normalize = True) * 100

for categoria, porcentaje in actual_pct.items():
    label = "Suscrito (Sí)" if categoria == 1 else "No Suscrito (No)"
    print(f"{label}: {porcentaje:.2f}%")

print('======================================================')

print('Resultados CAMPAÑA ANTERIOR (result_camp.previa)')
previa_pct = df['result_camp.previa'].value_counts(normalize = True) * 100

for resultado, porcentaje in previa_pct.items():
    print(f"{resultado.capitalize()}: {porcentaje:.2f}%")

import os
df.to_csv('data/bank-marketing-processed.csv', index=False, sep=',', encoding='utf-8')
