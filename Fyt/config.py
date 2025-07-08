from supabase import create_client, Client

# Configuración de Supabase
SUPABASE_URL = "https://wvxylrznhdxhbwpubbdt.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind2eHlscnpuaGR4aGJ3cHViYmR0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE4ODM4MjUsImV4cCI6MjA2NzQ1OTgyNX0.QCCu06sYq30n-5leutW0FJpd83cTNbwb3tpi8pC_S_E"

# Cliente Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Función auxiliar para insertar datos en Supabase
def insert_into_supabase(table, data):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    response = requests.post(url, headers=HEADERS, json=data)
    return response.status_code, response.text
