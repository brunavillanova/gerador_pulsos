# Projeto gerador_pulsos 
 um programa de interface gráfica usando a biblioteca Tkinter para realizar testes em dispositivos de contagem de pulsos
     Configuração de Portas Seriais:
        Configuração de portas seriais para envio (send_port) e recebimento (receive_port).
            Funções para Interagir com a Interface Gráfica:
        Fechar_Janela: Encerra o programa quando a janela é fechada.
        Encerrar_Programa: Seta a flag encerrar_programa para True.
        Enter_Pressionado: Avança para o próximo campo ao pressionar Enter.

    Funções Relacionadas ao Teste do Dispositivo:
        Leitura_Medidor: Realiza a leitura do dispositivo de contagem de pulsos e retorna os resultados.
        Obtem_Medidor: Extrai o número do medidor a partir do payload recebido.
        Obtem_Data_Hora: Obtém a data e hora atuais.
        Calcula_Pulsos: Calcula a quantidade de pulsos recebidos.

    Função de Identificação do Medidor:
        Identifica_Medidor: Compara o medidor lido com os campos da interface e marca os checkboxes correspondentes.

    Função para Reiniciar o Teste:
        reiniciar_teste: Limpa os campos da interface para reiniciar o teste.

    Função do Ciclo de Envio e Recebimento:
        Ciclo_Envio_Receb: Configura as portas seriais, envia comandos para o dispositivo e inicia o ciclo de leitura dos dados recebidos.

    Interface Gráfica:
        Usa Tkinter para criar uma janela com campos de entrada, checkboxes e botões.
        Exibe informações sobre dados recebidos, leituras iniciais e finais, entre outros.
        Atualiza um contador de tempo.

    Loop Principal:
        Executa um loop principal que atualiza a interface, aguarda a passagem do imã no dispositivo e identifica o medidor quando a leitura é concluída.
