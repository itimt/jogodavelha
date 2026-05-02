import socket
import tkinter as tk
from tkinter import messagebox
from threading import Thread

class ClienteJogo:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Velha - Cliente (X)")
        self.placar_o = 0
        self.placar_x = 0
        self.turno_ativo = True # Cliente (X) começa
        
        self.label_placar = tk.Label(root, text="Servidor (O): 0  |  Cliente (X): 0", font=('Arial', 14, 'bold'))
        self.label_placar.pack(pady=10)

        self.frame_tabuleiro = tk.Frame(root)
        self.frame_tabuleiro.pack()

        self.botoes = []
        for i in range(9):
            btn = tk.Button(self.frame_tabuleiro, text="", font=('Arial', 20), width=6, height=3,
                            command=lambda i=i: self.enviar_jogada(i))
            btn.grid(row=i//3, column=i%3)
            self.botoes.append(btn)

        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.cliente.connect(('localhost', 12345))
            Thread(target=self.receber_dados, daemon=True).start()
        except:
            messagebox.showerror("Erro", "Inicie o Servidor primeiro!")
            self.root.destroy()

    def enviar_jogada(self, pos):
        if self.botoes[pos]['text'] == "" and self.turno_ativo:
            self.botoes[pos].config(text="X", fg="red")
            self.cliente.send(str(pos).encode('utf-8'))
            self.turno_ativo = False
            self.verificar_fim_de_jogo()

    def receber_dados(self):
        while True:
            try:
                msg = self.cliente.recv(1024).decode('utf-8')
                if msg == "reset":
                    self.root.after(0, self.reset_interface)
                elif msg.isdigit():
                    pos = int(msg)
                    self.root.after(0, lambda: self.registrar_jogada_remota(pos))
            except: break

    def registrar_jogada_remota(self, pos):
        self.botoes[pos].config(text="O", fg="blue")
        self.turno_ativo = True
        self.verificar_fim_de_jogo()

    def verificar_fim_de_jogo(self):
        tabuleiro = [b['text'] for b in self.botoes]
        combinacoes = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        
        for c in combinacoes:
            if tabuleiro[c[0]] == tabuleiro[c[1]] == tabuleiro[c[2]] != "":
                venc = tabuleiro[c[0]]
                if venc == "O": self.placar_o += 1
                else: self.placar_x += 1
                self.label_placar.config(text=f"Servidor (O): {self.placar_o}  |  Cliente (X): {self.placar_x}")
                messagebox.showinfo("Fim de Jogo", f"O jogador {venc} venceu!")
                return

        if "" not in tabuleiro:
            messagebox.showinfo("Fim de Jogo", "Empate!")

    def reset_interface(self):
        for btn in self.botoes:
            btn.config(text="", state="normal")
        self.turno_ativo = True

if __name__ == "__main__":
    root = tk.Tk()
    app = ClienteJogo(root)
    root.mainloop()