import socket
import tkinter as tk
from tkinter import messagebox
from threading import Thread

class ServidorJogo:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Velha - Servidor (O)")
        self.placar_o = 0
        self.placar_x = 0
        self.turno_ativo = False # Servidor espera o cliente (X) começar, ou vice-versa
        
        self.label_placar = tk.Label(root, text="Servidor (O): 0  |  Cliente (X): 0", font=('Arial', 14, 'bold'))
        self.label_placar.pack(pady=10)

        self.frame_tabuleiro = tk.Frame(root)
        self.frame_tabuleiro.pack()
        
        self.botoes = []
        for i in range(9):
            btn = tk.Button(self.frame_tabuleiro, text="", font=('Arial', 20), width=6, height=3,
                            command=lambda i=i: self.realizar_jogada(i))
            btn.grid(row=i//3, column=i%3)
            self.botoes.append(btn)

        self.btn_reset = tk.Button(root, text="Reiniciar Partida", font=('Arial', 10), command=self.solicitar_reset)
        self.btn_reset.pack(pady=15)

        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.bind(('localhost', 12345))
        self.servidor.listen(1)
        
        self.conn = None
        Thread(target=self.aguardar_conexao, daemon=True).start()

    def aguardar_conexao(self):
        self.conn, addr = self.servidor.accept()
        self.turno_ativo = False # Geralmente o 'X' (cliente) começa
        Thread(target=self.receber_dados, daemon=True).start()

    def receber_dados(self):
        while True:
            try:
                msg = self.conn.recv(1024).decode('utf-8')
                if msg == "reset":
                    self.root.after(0, self.reset_interface)
                elif msg.isdigit():
                    pos = int(msg)
                    self.root.after(0, lambda: self.registrar_jogada_remota(pos))
            except: break

    def realizar_jogada(self, pos):
        if self.botoes[pos]['text'] == "" and self.turno_ativo:
            self.botoes[pos].config(text="O", fg="blue")
            self.conn.send(str(pos).encode('utf-8'))
            self.turno_ativo = False
            self.verificar_fim_de_jogo()

    def registrar_jogada_remota(self, pos):
        self.botoes[pos].config(text="X", fg="red")
        self.turno_ativo = True
        self.verificar_fim_de_jogo()

    def verificar_fim_de_jogo(self):
        tabuleiro = [b['text'] for b in self.botoes]
        combinacoes = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        
        for c in combinacoes:
            if tabuleiro[c[0]] == tabuleiro[c[1]] == tabuleiro[c[2]] != "":
                vencedor = tabuleiro[c[0]]
                self.finalizar_partida(f"O jogador {vencedor} venceu!")
                return

        if "" not in tabuleiro:
            self.finalizar_partida("Empate!")

    def finalizar_partida(self, mensagem):
        vencedor_simbolo = "O" if "O venceu" in mensagem else "X" if "X venceu" in mensagem else None
        if vencedor_simbolo == "O": self.placar_o += 1
        elif vencedor_simbolo == "X": self.placar_x += 1
        
        self.label_placar.config(text=f"Servidor (O): {self.placar_o}  |  Cliente (X): {self.placar_x}")
        messagebox.showinfo("Fim de Jogo", mensagem)
        self.solicitar_reset()

    def solicitar_reset(self):
        if self.conn: self.conn.send("reset".encode('utf-8'))
        self.reset_interface()

    def reset_interface(self):
        for btn in self.botoes:
            btn.config(text="", state="normal")
        self.turno_ativo = False # Reinicia com a vez do Cliente (X)

if __name__ == "__main__":
    root = tk.Tk()
    app = ServidorJogo(root)
    root.mainloop()