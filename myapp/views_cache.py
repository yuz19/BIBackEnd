from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import connection
import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests
import plotly.graph_objects as go
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from myapp.management.commands import CreateModels,CreateSerializer,GetTables
import mysql.connector
from django.conf import settings
def get_columns_from_table(table_name):
    cursor = connection.cursor()
    cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
    rows = cursor.fetchall()
    columns = [row[0] for row in rows]
    return columns

def granger(columns):
    tables_with_columns = {}
    # Récupérer les tables associées à chaque colonne spécifiée
    for column in columns:
        cursor = connection.cursor()
        cursor.execute(f"SELECT DISTINCT TABLE_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE COLUMN_NAME = '{column}'")
        rows = cursor.fetchall()
        for row in rows:
            table_name = row[0]
            if table_name in tables_with_columns:
                tables_with_columns[table_name].append(column)
            else:
                tables_with_columns[table_name] = [column]

    if not tables_with_columns:
        return Response({"message": "No tables found containing the specified columns."})

    # Récupérer les données pour chaque colonne et les stocker dans un DataFrame
    data_frames = {}
    for table_name, table_columns in tables_with_columns.items():
        for column in table_columns:
            cursor = connection.cursor()
            cursor.execute(f"SELECT {column} FROM {table_name}")
            rows = cursor.fetchall()
            if column in data_frames:
                data_frames[column].extend([row[0] for row in rows])
            else:
                data_frames[column] = [row[0] for row in rows]
    # Create a figure
    fig = go.Figure()
        
    # Add traces for each column in data_frames
    for column_name, column_data in data_frames.items():
        fig.add_trace(go.Scatter(x=list(range(len(column_data))), y=column_data, mode='lines', name=column_name))



    # Create a DataFrame from the dictionary
    df = pd.DataFrame(data_frames)
    # Print the shape of the DataFrame
    print("Shape of DataFrame:")
    print(df.shape)

    # Replace missing values with the mean of each column
    df = df.fillna(df.mean())
    # Effectuer le test de causalité de Granger pour chaque colonne dans cette table
    max_lag = 5  # Choisissez le nombre maximal de retards à tester
    print(df)
    # Update layout
    initial_range = [df.index.min(), df.index.min() + 500] 
    fig.update_layout(title='Data Visualization', xaxis_title='Index', yaxis_title='Value', xaxis=dict(range=initial_range))

    # Save the HTML string to a variable
   
    html_file_path = 'graph.html'
    fig.write_html(html_file_path)
    # Show the figure
    # fig.show()
    # Perform the Granger causality test
    try:
        results = grangercausalitytests(df, max_lag, verbose=True)
    except Exception as e:
        print("Error during Granger causality test:")
        print(e)
        results = None
    test_F_values = []
    p_values = []
    affichage_granger = []
    # Afficher et stocker les résultats dans les variables
    if results:
        for lag in range(1, max_lag + 1):
            print(f'\nRésultats pour le délai {lag}:')
            test_F_value = results[lag][0]["ssr_ftest"][0]
            p_value = results[lag][0]["ssr_ftest"][1]
            print(f'Test F : {test_F_value}')
            print(f'P-valeur : {p_value}')
            # Stocker les résultats dans les listes
            test_F_values.append(test_F_value)
            p_values.append(p_value)

    # Vérification de la causalité
    significant_lags = [lag for lag, p_value in enumerate(p_values, 1) if p_value < 0.05]

    if significant_lags:
        affichage_granger.append(f'\nCausalité trouvée pour au moins un délai : {significant_lags}\n')
    else:
        affichage_granger.append('\nAucune causalité trouvée pour tous les délais testés.\n')

    # Imprimer les résultats d'affichage
    for affichage in affichage_granger:
        print(affichage)

    return affichage_granger

@api_view(['POST'])
def analyse(request):
    columns = request.data.get('columns', [])
    algorithms=request.data.get('algorithms',[])
    if(any(algorithms)):
        if(algorithms['granger']): 
            granger(columns)  # Appeler la fonction de test de causalité de Granger avec les colonnes fournies
        if(algorithms['apriori']):
            #apriori(columns)  # Appeler la fonction de test de causalité de Granger avec les colonnes fournies
            print("apriori")
        if(algorithms['decision']):
            #decision(columns)  # Appeler la fonction de test de causalité de Granger avec les colonnes fournies
            print("decision")
            
        if(algorithms['proposer']): 
            #proposer(columns)  # Appeler la fonction de test de causalité de Granger avec les colonnes fournies
            print("proposer")
    else:
        return Response({"Error": "Choisir un algorithms"})   
    return Response({"message": "Analysis completed"})

 



# Connexion MySQL
import json
conn = None
def camel_case_to_spaces(text):
    result = ''
    for char in text:
        if char.isupper():
            result += ' '
        result += char
    return result.strip().lower()
@csrf_exempt
def connect_to_mysql(request):
    global conn
    if request.method == 'POST':
        # Récupérer les données POST du frontend
        data = json.loads(request.body)
        # Extraire les informations de connexion MySQL
        hostname = data.get('host')
        dbname = data.get('database')
        root = data.get('user')
        password = data.get('password')
        port=data.get('port')
        print(data.get('host')) 
        # Etablir une connexion avec MySQL
        try:
            connection = mysql.connector.connect(
                host=hostname,
                database=dbname,
                user=root,
                password=password,
                port=port
            )
            if connection.is_connected():
                db_info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_info)
                cursor = connection.cursor(dictionary=True)

                # Get list of tables in the database
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()

                for table in tables:
                    table_name = table['Tables_in_'+dbname]

                    # Get table columns
                    cursor.execute(f"DESCRIBE {table_name}")
                    columns = cursor.fetchall()

                    model_name = camel_case_to_spaces(table_name).replace(' ', '')

                    model_code = f"class {model_name}(models.Model):\n"
                    for column in columns:
                        field_name = column['Field']
                        field_type = column['Type']
                        primary_key = "primary_key=True" if column['Key'] == 'PRI' else ""
                        unique = "unique=True" if column['Key'] == 'UNI' else ""
                        foreign_key = ""
                        if "int" in field_type:
                            field_type = "IntegerField()"
                        elif "varchar" in field_type or "char" in field_type:
                            field_type = f"CharField(max_length={column['Field']})"
                        elif "datetime" in field_type:
                            field_type = "DateTimeField()"
                        elif "decimal" in field_type or "float" in field_type:
                            field_type = "DecimalField()"
                        else:
                            field_type = "UnknownField()"
                        model_code += f"    {field_name} = models.{field_type}({primary_key}, {unique})\n"
                       
                        if column['Key'] == 'MUL':
                            # Get referenced table and column
                            cursor.execute(f"SHOW CREATE TABLE {table_name}")
                            row = cursor.fetchone()
                            print("Fetched row:", row)  # Add this line to print the fetched row
                            if row is not None and 'Create Table' in row:
                                create_table_statement = row['Create Table']
                                print("Create table statement:", create_table_statement)  # Add this line to print the create table statement
                                referenced_table = ''  # Define referenced_table variable
                                referenced_table_split = create_table_statement.split(f'FOREIGN KEY (`{field_name}`) REFERENCES `')
                                if len(referenced_table_split) > 1:
                                    referenced_table_part = referenced_table_split[1]
                                    referenced_table_parts = referenced_table_part.split('`')
                                    if len(referenced_table_parts) > 1:
                                        referenced_table = referenced_table_parts[0]
                                        referenced_column = referenced_table_parts[1]
                                        foreign_key = f"ForeignKey('{referenced_table}', on_delete=models.CASCADE)"
                                        model_code += f"    {field_name}_id = models.{foreign_key}\n"
                                    else:
                                        print(f"No referenced column found for table {table_name} and field {field_name}")
                                else:
                                    print(f"No referenced table found for field {field_name}")
                            else:
                                print(f"No table creation statement found for table {table_name}")



                    model_code += "\n"

                    # Write the model code to a Python file
                    with open(f"{model_name.lower()}.py", "w") as f:
                        f.write("from django.db import models\n\n")
                        f.write(model_code)

                    print(f"Model {model_name} generated successfully!")


                return JsonResponse({'message': 'Connexion réussie à MySQL'})
            else:
                return JsonResponse({'error': 'Impossible de se connecter à MySQL'}, status=500)
        except mysql.connector.Error as e:
            return JsonResponse({'error': f'Erreur de connexion à MySQL : {str(e)}'}, status=500)

    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def reconnect_to_mysql(request):
    global conn
    if request.method == 'POST':
        # Récupérer les données POST du frontend
        data = json.loads(request.body)


        # Extraire les nouvelles informations de connexion MySQL
        hostname = data.get('host')
        dbname = data.get('database')
        root = data.get('user')
        password = data.get('password')
        port=data.get('port')
         
        # Mettre à jour la connexion MySQL avec les nouvelles informations de connexion
        try:
            if conn and conn.is_connected():
                conn.close()
             
            conn = mysql.connector.connect(
                host=hostname,
                database=dbname,
                user=root,
                password=password,
                port=port
            )
            if conn.is_connected():
                CreateModels();
                CreateSerializer();
                GetTables();
                return JsonResponse({'message': 'Reconnexion réussie à MySQL avec de nouvelles informations de connexion'})
            else:
                return JsonResponse({'error': 'Impossible de se reconnecter à MySQL avec de nouvelles informations de connexion'}, status=500)
        except mysql.connector.Error as e:
            return JsonResponse({'error': f'Erreur de reconnexion à MySQL avec de nouvelles informations de connexion : {str(e)}'}, status=500)

    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
# Define the connect_to_mysql function

# @csrf_exempt
# def connect_to_mysql(request):
#     if request.method == 'POST':
#         # Retrieve POST data from the frontend
#         data = json.loads(request.body)
#         # Extract MySQL connection information
#         hostname = data.get('host')
#         dbname = data.get('database')
#         user = data.get('user')
#         password = data.get('password')
#         port = data.get('port')
       

#         # Execute necessary commands after modifying settings
#         try:
#             # Modify Django settings dynamically
#             settings.DATABASES['default'] = {
#                 'ENGINE': 'django.db.backends.mysql',
#                 'NAME': dbname,
#                 'USER': user,
#                 'PASSWORD': password,
#                 'HOST': hostname,
#                 'PORT': port,
#             }

#             return JsonResponse({'message': 'Connexion réussie à MySQL'})
#         except Exception as e:
#             return JsonResponse({'error': f'Internal Server Error: {str(e)}'}, status=500)
 

        
#         print('message : Connexion réussie à MySQL')

#         return JsonResponse({'message': 'Connexion réussie à MySQL'})
    
#     else:
#         return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
