package questao_02;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;
import questao_02.entidades.Pessoa;

public class PessoasInputStream {
    private Pessoa[] pessoas;

    public PessoasInputStream(Pessoa[] pessoas) {
        this.pessoas = pessoas;
    }

    public void tcp(){
        int port = 12345; // Porta em que o servidor escutará as conexões.
        try {
            ServerSocket serverSocket = new ServerSocket(port);
            System.out.println("Aguardando conexões na porta " + port + "...");
            
           while (true) {
                Socket clientSocket = serverSocket.accept(); // Aguarda a conexão do cliente.
                System.out.println("Cliente conectado: " + clientSocket.getInetAddress());

                // Agora, leia os dados enviados pelo cliente e imprima-os
                BufferedReader reader = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                String line;
                while ((line = reader.readLine()) != null) {
                    System.out.println("Mensagem do cliente: " + line);
                }

                clientSocket.close(); // Fecha a conexão com o cliente.
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    } 

    public void leitorDeArquivo() {
        String nomeArquivo = "FileOutputStream.txt";

        try (BufferedReader br = new BufferedReader(new FileReader(nomeArquivo))) {
            String line;

            while ((line = br.readLine()) != null) {

            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void imprimirPessoas() {
        for (Pessoa pessoa : pessoas) {
            if (pessoa != null) {
                System.out.println("Nome: " + pessoa.getNome());
                System.out.println("CPF: " + pessoa.getCpf());
                System.out.println("Idade: " + pessoa.getIdade());
                System.out.println("------------------");
            }
        }
    }
    
    public static void main(String[] args) {
        // p.leitorDeArquivo();
        
        Pessoa[] pessoas = new Pessoa[3];
        pessoas[0] = new Pessoa("Joao", 123456789, 20);
        pessoas[1] = new Pessoa("Maria", 987654321, 30);
        pessoas[2] = new Pessoa("Jose", 123456789, 40);
        
        PessoasInputStream p = new PessoasInputStream(pessoas);

        //imprimir na tela
        p.imprimirPessoas();
        
        //ler do arquivo
        p.leitorDeArquivo();

        //roda o servidor TCP para a questão 1 conectar
        p.tcp();

    }
}