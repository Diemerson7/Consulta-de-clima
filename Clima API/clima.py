import requests

API_KEY = "194c6f32d3eca0dad939059007abbf9a"

def obter_clima(cidade):
    try:
        if not API_KEY:
            return "⚠️ Chave da API não definida."

        url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade},BR&appid={API_KEY}&lang=pt&units=metric"
        resposta = requests.get(url)
        dados = resposta.json()

        if resposta.status_code != 200:
            return f"Erro: {dados.get('message', 'Cidade não encontrada!')}"

        temp = dados["main"]["temp"]
        feels_like = dados["main"]["feels_like"]
        condicao = dados["weather"][0]["description"]

        return f"🌡 Temperatura: {temp}°C\n🤒 Sensação Térmica: {feels_like}°C\n🌥 Condição: {condicao.capitalize()}"
    except Exception as e:
        return f"Erro ao consultar clima: {str(e)}"
    
