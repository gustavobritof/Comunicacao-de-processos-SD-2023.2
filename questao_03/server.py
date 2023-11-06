import socket
from serialize import serialize, deserialize
import threading
from datetime import date
from animal import Consulta, Cachorro, Gato, Coelho

# Lista compartilhada para armazenar as consultas
consultas = []

def handle_client(client_socket):
    while True:
        request = client_socket.recv(1024)
        if not request:
            break
        
        request_data = deserialize(request)
        response_data = {}  # Inicializa a resposta vazia

        if request_data['action'] == 'agendar_consulta':
            animal_type = request_data['animal_type']
            animal_data = request_data['animal_data']

            if animal_type == 'Cachorro':
                animal = Cachorro(animal_data['nome'], animal_data['idade'], animal_data['raca'], animal_data['nome_dono'])
            elif animal_type == 'Gato':
                animal = Gato(animal_data['nome'], animal_data['idade'], animal_data['cor_pelo'], animal_data['nome_dono'])
            elif animal_type == 'Coelho':
                animal = Coelho(animal_data['nome'], animal_data['idade'], animal_data['tamanho'], animal_data['nome_dono'])
            else:
                response_data = {'erro': 'Tipo de animal inválido'}

            if not response_data.get('erro'):
                consulta = Consulta(animal, 'Dr. Veterinário', date.today())
                consultas.append(consulta)
                response_data = {'mensagem': 'Consulta agendada com sucesso!'}

        elif request_data['action'] == 'buscar':
            animal_name = request_data['animal_name']
            animal_type = request_data['animal_type']
            consultas_encontradas = []

            for consulta in consultas:
                if (not animal_name or consulta.animal.nome == animal_name) and \
                   (not animal_type or type(consulta.animal).__name__ == animal_type):
                    consultas_encontradas.append(consulta)

            if consultas_encontradas:
                consultas_str = '\n'.join([str(consulta) for consulta in consultas_encontradas])
                response_data = {'mensagem': consultas_str}
            else:
                response_data = {'mensagem': 'Nenhuma consulta encontrada'}

        elif request_data['action'] == 'sair':
            client_socket.close()
            break

        else:
            response_data = {'erro': 'Ação desconhecida'}

        response = serialize(response_data)
        client_socket.send(response)

def alterarStatus():
    while True:
        print("Opções:")
        print("1. Mostrar agendamentos")
        print("2. Alterar status")
        print("3. Sair")
        escolha = input("Escolha a opção (1/2/3): ")

        if escolha == '1':
            for consulta in consultas:
                print(consulta)
                
        elif escolha == '2':
            animal_name = input("Digite o nome do animal: ")
            novo_status = input("Digite o novo status: ")
            for consulta in consultas:
                if consulta.animal.nome == animal_name:
                    consulta.status = novo_status
                    print("Status alterado com sucesso!")
                    break
            else:
                print("Animal não encontrado")
        elif escolha == '3':
            break
        else:
            print("Opção inválida. Tente novamente.")
        
                


def main():
    alterar_Status = threading.Thread(target=alterarStatus)
    alterar_Status.daemon = True
    alterar_Status.start()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 8080))
    server.listen(5)
    print("Servidor pronto para receber conexões...")

    while True:
        client_socket, addr = server.accept()
        print('')
        print(f"Conexão de {addr[0]}:{addr[1]} estabelecida")
        print('')
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
