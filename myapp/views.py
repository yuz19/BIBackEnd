from rest_framework.response import Response
from rest_framework.decorators import api_view

import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests
import plotly.graph_objects as go
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import mysql.connector

def get_columns_from_table(table_name):
    global conn
    cursor = conn.cursor()
    cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
    rows = cursor.fetchall()
    columns = [row[0] for row in rows]
    return columns

def granger(columns):
    tables_with_columns = {}
    # Récupérer les tables associées à chaque colonne spécifiée
    for column in columns:
        cursor = conn.cursor()
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
            cursor = conn.cursor()
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
    html_content = fig.to_html()
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

    return affichage_granger, html_content
array_return=[]
@csrf_exempt
@api_view(['GET', 'POST'])
def analyse(request):
    global array_return
     
    if request.method == 'POST':
        

        columns = request.data.get('columns', [])
        algorithms = request.data.get('algorithms', [])
        
        if any(algorithms):
            if algorithms.get('granger', False):
                granger_result = granger(columns)
                if granger_result:
                    array_return.append({'granger': granger_result})
                    
            if algorithms.get('apriori', False):
                apriori_result = apriori(columns)
                if apriori_result:
                    array_return.append({'apriori': apriori_result})
                    
            if algorithms.get('decision', False):
                decision_result = decision(columns)
                if decision_result:
                    array_return.append({'decision': decision_result})
                    
            if algorithms.get('proposer', False):
                proposer_result = proposer(columns)
                if proposer_result:
                    array_return.append({'proposer': proposer_result})
                    
            if array_return:
                return Response(array_return)
            else:
                return Response({"message": "No results found"}, status=404)
        
        
        else:
            return Response({"Error": "Choisir un algorithme"})
    
    elif request.method == 'GET':
        return Response(array_return)



# Connexion MySQL
import json
conn = None
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
            conn = mysql.connector.connect(
                host=hostname,
                database=dbname,
                user=root,
                password=password,
                port=port
            )
            if conn.is_connected():
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
