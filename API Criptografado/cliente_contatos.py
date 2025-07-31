import customtkinter as ctk
import tkinter.messagebox as messagebox
import requests
import re
from threading import Thread

API_URL = "http://127.0.0.1:5000"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Agenda de Contatos Criptografada")
        self.geometry("500x600")
        self.resizable(False, False)
        
        # Inicializar variáveis de entrada
        self.ent_nome = None
        self.ent_telefone = None
        self.ent_email = None
        
        self.configure_layout()
        self.create_widgets()
        
    def configure_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
    def create_widgets(self):
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Campo Nome
        lbl_nome = ctk.CTkLabel(self.frame, text="Nome:")
        lbl_nome.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.ent_nome = ctk.CTkEntry(self.frame, width=300)
        self.ent_nome.grid(row=0, column=1, padx=10, pady=5)
        
        # Campo Telefone
        lbl_telefone = ctk.CTkLabel(self.frame, text="Telefone:")
        lbl_telefone.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.ent_telefone = ctk.CTkEntry(self.frame, width=300)
        self.ent_telefone.grid(row=1, column=1, padx=10, pady=5)
        
        # Campo Email
        lbl_email = ctk.CTkLabel(self.frame, text="Email:")
        lbl_email.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.ent_email = ctk.CTkEntry(self.frame, width=300)
        self.ent_email.grid(row=2, column=1, padx=10, pady=5)
        
        # Botão Adicionar
        self.btn_add = ctk.CTkButton(
            self.frame, 
            text="Adicionar Contato", 
            command=self.adicionar_contato_thread
        )
        self.btn_add.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Botão Listar
        self.btn_listar = ctk.CTkButton(
            self.frame, 
            text="Listar Contatos", 
            command=self.listar_contatos_thread
        )
        self.btn_listar.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Área de resultados
        self.txt_result = ctk.CTkTextbox(
            self.frame, 
            width=400, 
            height=250,
            wrap="word"
        )
        self.txt_result.grid(row=5, column=0, columnspan=2, pady=10)
        
    def validar_campos(self):
        nome = self.ent_nome.get().strip()
        telefone = self.ent_telefone.get().strip()
        email = self.ent_email.get().strip().lower()
        
        if not all([nome, telefone, email]):
            messagebox.showerror("Erro", "Preencha todos os campos")
            return False
            
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Erro", "E-mail inválido")
            return False
            
        return True
        
    def adicionar_contato_thread(self):
        Thread(target=self.adicionar_contato, daemon=True).start()
        
    def adicionar_contato(self):
        if not self.validar_campos():
            return
            
        nome = self.ent_nome.get().strip()
        telefone = self.ent_telefone.get().strip()
        email = self.ent_email.get().strip().lower()
        
        try:
            r = requests.post(
                f"{API_URL}/contatos",
                json={"nome": nome, "telefone": telefone, "email": email},
                timeout=5
            )
            
            if r.status_code == 200:
                messagebox.showinfo("Sucesso", r.json()["msg"])
                self.ent_nome.delete(0, 'end')
                self.ent_telefone.delete(0, 'end')
                self.ent_email.delete(0, 'end')
            else:
                messagebox.showerror("Erro", r.json().get("msg", "Erro ao adicionar contato"))
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Erro na conexão: {str(e)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
            
    def listar_contatos_thread(self):
        Thread(target=self.listar_contatos, daemon=True).start()
        
    def listar_contatos(self):
        try:
            self.txt_result.delete("1.0", "end")
            self.txt_result.insert("end", "Carregando contatos...\n")
            
            r = requests.get(f"{API_URL}/contatos", timeout=5)
            
            if r.status_code == 200:
                self.txt_result.delete("1.0", "end")
                contatos = r.json()
                
                if not contatos:
                    self.txt_result.insert("end", "Nenhum contato encontrado.")
                    return
                    
                for c in contatos:
                    self.txt_result.insert("end", 
                        f"Nome: {c['nome']}\n"
                        f"Telefone: {c['telefone']}\n"
                        f"Email: {c['email']}\n\n"
                    )
            else:
                messagebox.showerror("Erro", "Erro ao listar contatos")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Erro na conexão: {str(e)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = App()
    app.mainloop()