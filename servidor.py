import socket

def iniciar_servidor():
    # Cria um socket TCP/IP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Define o IP (localhost) e a porta
    servidor.bind(('localhost', 12345))
    servidor.listen(1)
    
    print("Aguardando conexão do jogador...")
    conexao, endereco = servidor.accept()
    print(f"Conectado com: {endereco}")

    try:
        while True:
            # Recebe a jogada do cliente (até 1024 bytes)
            dados = conexao.recv(1024).decode('utf-8')
            if not dados:
                break
                
            print(f"O jogador moveu para a posição: {dados}")
            
            # Envia uma confirmação simples
            resposta = f"Servidor recebeu a jogada na posição {dados}"
            conexao.send(resposta.encode('utf-8'))
    finally:
        conexao.close()
        servidor.close()

if __name__ == "__main__":
    iniciar_servidor()