import socket

def iniciar_cliente():
    # Cria o socket
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Conecta ao servidor
        cliente.connect(('localhost', 12345))
        print("Conectado ao Jogo da Velha!")

        while True:
            jogada = input("Digite a posição da sua jogada (0-8) ou 'sair': ")
            
            if jogada.lower() == 'sair':
                break
                
            # Envia para o servidor
            cliente.send(jogada.encode('utf-8'))
            
            # Recebe a resposta
            confirmacao = cliente.recv(1024).decode('utf-8')
            print(f"Confirmação: {confirmacao}")
            
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        cliente.close()

if __name__ == "__main__":
    iniciar_cliente()