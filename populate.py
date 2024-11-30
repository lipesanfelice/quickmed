import pandas as pd
import mysql.connector

# Load the CSV data into a DataFrame
df = pd.read_csv('Unidades_Basicas_Saude-UBS.csv', delimiter=';')

df = df.dropna()

# Replace commas with periods in latitude and longitude columns
df['LATITUDE'] = df['LATITUDE'].apply(lambda x: str(x).replace(',', '.'))
df['LONGITUDE'] = df['LONGITUDE'].apply(lambda x: str(x).replace(',', '.'))

# Convert LATITUDE and LONGITUDE to float for proper database insertion
df['LATITUDE'] = df['LATITUDE'].astype(float)
df['LONGITUDE'] = df['LONGITUDE'].astype(float)

# Establish a connection to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="Chico2704",
    database="quickmed"
)

cursor = conn.cursor()

# Set the limit to 100 rows
df_limited = df.head(100)  # This selects only the first 100 rows

# Iterate over each row in the limited DataFrame and insert into the 'Clinica' table
for index, row in df_limited.iterrows():
    sql = """
    INSERT INTO Clinica (nome, endereco, latitude, longitude)
    VALUES (%s, %s, %s, %s)
    """
    values = (row['NOME'], row['LOGRADOURO'], row['LATITUDE'], row['LONGITUDE'])
    cursor.execute(sql, values)

# Commit the transaction
conn.commit()

# Close the connection
cursor.close()
conn.close()
