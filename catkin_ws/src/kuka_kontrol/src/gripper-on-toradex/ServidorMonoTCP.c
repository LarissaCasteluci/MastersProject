/*
 * 			ServidorMonoTCP.c
 *
 * Este programa foi desenvolvido para simular uma aplicacao servidora
 *
 * Funcao:     Receber e retornar streams compostos de caracteres
 * Plataforma: Linux (Unix), ou Windows com CygWin
 * Compilar:   gcc -Wall ServidorMonoTCP.c -o ServidorMonoTCP
 * Uso:        ./ServidorMonoTCP [porta_do_servidor]
 *
 * Autor:      Jose Martins Junior
 *
 * Portas Utilizadas: 46 (positivo) e 88 (negativo)
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <netdb.h>

#define QUEUE_LENGTH 5      //Tamanho maximo da fila de conexoes de clientes
#define MAX_FLOW_SIZE 1000  //Tamanho maximo do buffer de caracteres
#define true 1


char buf[MAX_FLOW_SIZE];
int fd1, fd2;

/*
 *******************************************************************************
               Comeco da main, onde os outputs sao configurados
 *******************************************************************************
 */

int main(int argc, char *argv[]) {
	int sockId, recvBytes, bindRet, getRet, sentBytes, connId, serverPort;
	unsigned int servLen, cliLen;
	struct sockaddr_in server, client;
	
    fd1 = open("/sys/class/gpio/export", O_WRONLY);
    write(fd1, "46", 2);
    close(fd1);
    
    fd2 = open("/sys/class/gpio/export", O_WRONLY);
    write(fd2, "88", 2);
    close(fd2);
 
    // configure as output
    fd1 = open("/sys/class/gpio/gpio46/direction", O_WRONLY);
    write(fd1, "out", 3);
    close(fd1);
    
    fd2 = open("/sys/class/gpio/gpio88/direction", O_WRONLY);
    write(fd2, "out", 3);
    close(fd2);
    
    // seta valor inicial
    fd2 = open("/sys/class/gpio/gpio88/value", O_WRONLY | O_SYNC);
	write(fd1, "0", 1);
	close(fd1);
	
	fd1 = open("/sys/class/gpio/gpio46/value", O_WRONLY | O_SYNC);
	write(fd2, "0", 1);
	close(fd2);

/*
 *******************************************************************************
               Abrindo um socket do tipo stream (TCP)
 *******************************************************************************
 */
	sockId = socket(AF_INET, SOCK_STREAM, 0);
	if (sockId < 0) {
		printf("Stream socket nao pode ser aberto\n");
		return(1);
	}
/*----------------------------------------------------------------------------*/

/*
 *******************************************************************************
               Setando os atributos da estrutura do socket
 *******************************************************************************
 */
	server.sin_family	= AF_INET;
	server.sin_addr.s_addr = INADDR_ANY;
	if (argc == 2) {
		serverPort	= atoi(argv[1]);
		if (serverPort <= 0) {
			printf("Porta Invalida: %s\n", argv[1]);
			close(sockId);
			return(1);
		}
		else server.sin_port	= htons(serverPort);
	}
	else server.sin_port = 0;
/*----------------------------------------------------------------------------*/

/*
 *******************************************************************************
               Fazendo o bind para o stream socket aberto
 *******************************************************************************
 */
	bindRet = bind(sockId, (struct sockaddr *)&server, sizeof(server));
	if (bindRet < 0) {
		printf("O bind para o stream socket falhou\n");
		close(sockId);
		return(1);
	}
/*----------------------------------------------------------------------------*/

/*
 *******************************************************************************
               Obtendo o nome do socket
 *******************************************************************************
 */
	servLen = sizeof(server);
	getRet	= getsockname(sockId, (struct sockaddr *)&server, &servLen);
	if (getRet < 0) {
		printf("Nao foi possivel obter o nome do socket\n");
		close(sockId);
		return(1);
	}
/*----------------------------------------------------------------------------*/

	printf("Porta do servidor: %d\n",ntohs(server.sin_port));

/*
 *******************************************************************************
               Colocando o servidor em modo listening
 *******************************************************************************
 */
	listen(sockId, QUEUE_LENGTH);
/*----------------------------------------------------------------------------*/

	do { //REPETE PARA SEMPRE ************************************************** <------------ Troca de mensagens e resto do codigo

/*
 *******************************************************************************
               Habilitando o servidor de receber conexoes
 *******************************************************************************
 */
		cliLen = sizeof(client);
                connId = accept(sockId, (struct sockaddr *)&client, &cliLen);
		if (connId < 0)
			printf("O socket nao pode aceitar conexoes\n");
/*----------------------------------------------------------------------------*/

		else do {

/*
 *******************************************************************************
               Recebendo as mensagens do cliente
 *******************************************************************************
 */
				memset(buf, 0, sizeof(buf)); //Substitui todos os char de buf por 0
				recvBytes = recv(connId, buf, MAX_FLOW_SIZE, 0);
				if (recvBytes <= 0) {
					if (recvBytes < 0)
						printf("Ocorreu um erro na aplicacao\n");
					else
						printf("Encerrando a conexao do cliente\n");
				}
/*----------------------------------------------------------------------------*/
/*
 *******************************************************************************
               Interpreta a mensagem do cliente
 *******************************************************************************
 */
				else {
					msg_handler_gripper();//Funcao que gerencia garra

/*
 *******************************************************************************
               Enviando as mensagens para o cliente
 *******************************************************************************
 */
					sentBytes = send(connId, buf, strlen(buf), 0);
					if (sentBytes < 0) {
						printf("A conexao foi perdida\n");
						recvBytes = 0;
					}
					else {
						printf("Mensagem enviada: [%s]\n",buf);
					}
/*----------------------------------------------------------------------------*/

				}
			} while (recvBytes > 0);
		close(connId);
	} while (true);
	close(sockId);
	return(0);
}

/*
 *******************************************************************************
               Funcao que administra acao da garra
 *******************************************************************************
 */
void msg_handler_gripper()
{
    if(strcmp(buf,"command_open") == 0){
        open_gripper();
    }
    else if(strcmp(buf,"command_close") == 0){
        close_gripper();
    }
    else if(strcmp(buf,"command_calibration") == 0){
        calibration_gripper(); 
    }
    
}
/*
 *******************************************************************************
               Funcoes de abrir, fechar e calibrar a garra
 *******************************************************************************
 */
void open_gripper() 
{
	//CODIGO PARA ABRIR
	
/*	
 * Eh necessario ter certeza que o negativo esta em Zero e depois eh importante
 * ligar o positivo por um periodo de tempo correto para abrir a garra
 */
	fd2 = open("/sys/class/gpio/gpio88/value", O_WRONLY | O_SYNC);
	write(fd2, "0", 1);
	close(fd2);
	
	usleep(100000);
	fd1 = open("/sys/class/gpio/gpio46/value", O_WRONLY | O_SYNC);
	write(fd1, "1", 1);
	usleep(1000000);
	write(fd1, "0", 1);
	close(fd1);
	// buf recebe string para enviar msg para cliente novamente
	strcpy(buf, "status_gripper_open_successful");
}

/*----------------------------------------------------------------------------*/

void close_gripper()
{
	//CODIGO PARA FECHAR
	
/*	
 * Eh necessario ter certeza que o positivo esta em Zero e depois eh importante
 * deixar o motor da garra ligado, para nao perder o torque para o grip
 */
	fd2 = open("/sys/class/gpio/gpio46/value", O_WRONLY | O_SYNC);
	write(fd1, "0", 1);
	close(fd1);
	
	usleep(100000);
	fd2 = open("/sys/class/gpio/gpio88/value", O_WRONLY | O_SYNC);
	write(fd2, "1", 1);
	close(fd2);
	// buf recebe string para enviar msg para cliente novamente
	strcpy(buf, "status_gripper_close_successful");
}

/*----------------------------------------------------------------------------*/

void calibration_gripper()
{

  	//CODIGO PARA CALIBRAR
  	fd1 = open("/sys/class/gpio/gpio46/value", O_WRONLY | O_SYNC);
	write(fd1, "0", 1);
	close(fd1);
	
  	fd2 = open("/sys/class/gpio/gpio88/value", O_WRONLY | O_SYNC);
	write(fd2, "1", 1);
	usleep(2000000);
	write(fd2, "0", 1);
	close(fd2);
	
	usleep(100000);
	fd1 = open("/sys/class/gpio/gpio46/value", O_WRONLY | O_SYNC);
	write(fd1, "1", 1);
	usleep(1000000);
	write(fd1, "0", 1);
	close(fd1);
	
  	// buf recebe string para enviar msg para cliente novamente
  	strcpy(buf, "status_gripper_calibration_successful");
}

