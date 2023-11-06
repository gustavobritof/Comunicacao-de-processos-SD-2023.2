# Superclasse de animal
class Animal:
    def __init__(self, nome, idade, nomeDono = None):
        self.nome = nome
        self.idade = idade
        self.nome_dono = nomeDono

    def __str__(self):
        return f"Nome: {self.nome}\nIdade: {self.idade}\nNome do Dono: {self.nome_dono}\n"

    def to_dict(self):
        animal_dict = self.__dict__
        animal_dict['tipo'] = type(self).__name__
        return animal_dict

# Subclasses de animal
class Gato(Animal):
    def __init__(self, nome, idade, nomeDono, cor_pelo):
        super().__init__(nome, idade, nomeDono)
        self.cor_pelo = cor_pelo    

    def __str__(self):
        return super().__str__() + f"Cor do Pelo: {self.cor_pelo}\n"

class Cachorro(Animal):
    def __init__(self, nome, idade, nomeDono, raca):
        super().__init__(nome, idade, nomeDono)
        self.raca = raca

    def __str__(self):
        return super().__str__() + f"Raça: {self.raca}\n"

class Coelho(Animal):
    def __init__(self, nome, idade, nomeDono, tamanho):
        super().__init__(nome, idade, nomeDono)
        self.tamanho = tamanho

    def __str__(self):
        return super().__str__() + f"Tamanho: {self.tamanho}\n"
    
# Interface de consulta
class Consulta:
    def __init__(self, animal: Animal, veterinario, data):
        self.animal = animal
        self.veterinario = veterinario
        self.status = "Agendada"
        self.data = data
        self.consultas = []

    def add_consulta(self, consulta):
        self.consultas.append(consulta)

    def buscar_consultas(self, nome_animal=None, tipo_animal=None, data_consulta=None):
        consultas_encontradas = []
        for consulta in self.consultas:
            if (nome_animal is None or consulta.animal.nome == nome_animal) and \
               (tipo_animal is None or type(consulta.animal).__name__ == tipo_animal) and \
               (data_consulta is None or consulta.data == data_consulta):
                consultas_encontradas.append(consulta)
        return consultas_encontradas


    def __str__(self):
        return f"Animal: {self.animal.nome}, Veterinário: {self.veterinario}, Status: {self.status}, Data: {self.data}"
