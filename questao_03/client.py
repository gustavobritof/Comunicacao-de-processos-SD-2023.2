import socket
from serialize import serialize, deserialize
from animal import Animal, Cachorro, Gato, Coelho

def make_request(action, param):
    if action == 'agendar_consulta':
        return {'action': action, 'animal_type': type(param).__name__, 'animal_data': param.to_dict()}
    elif action == 'buscar':
        return {'action': action, 'animal_name': param[0], 'animal_type': param[1]}

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8080))

    while True:
        print("Opções:")
        print("1. Agendar consulta")
        print("2. Checar o andamento da consulta")
        print("3. Sair")

        choice = input("Escolha a opção (1/2/3): ")

        if choice == '1':
            animal_name = input("Digite o nome do animal: ")
            animal_age = int(input("Digite a idade do animal: "))
            animal_owner = input("Digite o nome do dono do animal: ")
            animal_type = input("Digite o tipo de animal (Cachorro/Gato/Coelho): ")
            if animal_type == 'Cachorro':
                animal_race = input("Digite a raça do animal: ")
                cachorro = Cachorro(animal_name, animal_age, animal_owner, animal_race)
                request = make_request('agendar_consulta', cachorro)
            elif animal_type == 'Gato':
                animal_fur_color = input("Digite a cor do pelo do animal: ")
                gato = Gato(animal_name, animal_age, animal_owner, animal_fur_color)
                request = make_request('agendar_consulta', gato)
            elif animal_type == 'Coelho':
                animal_size = input("Digite o tamanho do animal: ")
                coelho = Coelho(animal_name, animal_age, animal_owner, animal_size)
                request = make_request('agendar_consulta', coelho)
            else:
                print("Tipo de animal inválido. Tente novamente.")
                continue
            
            client.send(serialize(request))
            response = client.recv(1024)
            response_data = deserialize(response)
            if 'erro' in response_data:
                print(f"Erro: {response_data['erro']}")
            else:
                print(response_data['mensagem'])
                    
        elif choice == '2':
            animal_name = input("Digite o nome do animal: ")
            animal_type = input("Digite o tipo de animal (Cachorro/Gato/Coelho): ")
            request = make_request('buscar', (animal_name, animal_type))
            client.send(serialize(request))
            response = client.recv(1024)
            response_data = deserialize(response)
            if 'erro' in response_data:
                print(f"Erro: {response_data['erro']}")
            else:
                print(response_data['mensagem'])
        elif choice == '3':
            client.close()
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()

