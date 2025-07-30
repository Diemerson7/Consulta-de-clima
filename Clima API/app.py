import customtkinter as ctk
from clima import obter_clima

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Clima - Cidades do Paraná")
app.geometry("400x300")

titulo = ctk.CTkLabel(app, text="Consulta de Clima", font=("Poppins", 20))
titulo.pack(pady=10)

entrada_cidade = ctk.CTkEntry(app, placeholder_text="Digite a cidade (ex: Curitiba)")
entrada_cidade.pack(pady=10)

resposta_clima = ctk.CTkLabel(app, text="", justify="left", font=("Poppins", 16))
resposta_clima.pack(pady=10)

def ao_clicar():
    cidade = entrada_cidade.get()
    if cidade.strip() == "":
        resposta_clima.configure(text="⚠️ Digite o nome da cidade.")
    else:
        clima = obter_clima(cidade)
        resposta_clima.configure(text=clima)

def limpar():
    entrada_cidade.delete(0, "end")    
    resposta_clima.configure(text="")  

botao = ctk.CTkButton(app, text="Consultar Clima", command=ao_clicar)
botao.pack(pady=10)

botao_limpar = ctk.CTkButton(app, text="Limpar", command=limpar)
botao_limpar.pack(pady=5)

app.mainloop()
