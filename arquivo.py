import serial
import datetime
from time import sleep
from time import time
import tkinter as tk
#------------ CONSTANTES E VARIÁVEIS DE CONTROLE ---------------#
QT_MAX_FIELD = 7
OBJ_BACKGROUND = "#000000"
leitura_concluida = False
encerrar_programa = False

#---------------------- FUNÇÕES --------------------------------#

def Fechar_Janela(event):
    Encerrar_Programa()

def Encerrar_Programa():
    global encerrar_programa
    encerrar_programa = True

def atualizar_contador_tempo():
    for i in range(1, QT_MAX_FIELD):
        if (tempo_inicial[i] > 0):
            tempo_atual[i] = int((time() - tempo_inicial[i]))  # Tempo em segundos
            print("Atualizado o campo ", str(i), " com o tempo: ", str(tempo_atual[i]))

        if ((tempo_atual[i] > 10) and (tempo_inicial[i] > 0)):
            txt_Resultado[i].configure(state='normal')
            txt_Resultado[i].insert(0,"  FALHOU")
            
            txt_Resultado[i].configure(bg='red')
            tempo_inicial[i] = 0

def Enter_Pressionado(event, index):
    if event.keycode == 13:
        entry = event.widget
        print(entry.get())
        #entry = str(entry)
        i = index
        print("Pressionou <Enter>")
        print(str(i))
        tempo_inicial[i] =int(time())  
        print("tempo",str(tempo_inicial[i]))
        if i < (QT_MAX_FIELD - 1):
            txt_box_id[i + 1].focus()
        else:
            btn_reiniciar.focus()


def Obtem_Medidor(payload):
    k = 0
    medidor = ""
    print("payload", payload)
    while (k < 9):
        medidor = medidor + str(payload[30+k] - 0x30)
        k = k + 1
    return medidor

def Obtem_Data_Hora():
    agora = datetime.datetime.now()
    return agora

def Calcula_Pulsos(qtdPulsosRec, intByte, i):
    if (i == 16):
        qtdPulsosRec = qtdPulsosRec + int(intByte)

    if (i == 15):
        qtdPulsosRec = qtdPulsosRec + (256 * int(intByte))

    if (i == 14):
        qtdPulsosRec = qtdPulsosRec + (256 * 256 * int(intByte))

    return qtdPulsosRec

#--------------------- Leitura do Payload do Medidor -----------------------#

def Leitura_Medidor():
    #3. Inicia o ciclo de leitura dos dados recebidos pela porta serial
    stringHexa = ""
    strPayload = ""
    qtdPulsosRec = 0
    leitura_concluida = False
    payload = []
    i = 0

    if (receive_port.in_waiting > 0):
        tempo_inicial = time() * 1000

        while (True):

            #-- Executa loop realizando a leitura da porta serial
            for byte in receive_port.read():
                payload.append(byte)
                intByte = byte 

                stringHexa = stringHexa + " " + hex(byte).zfill(4)[2:4]
                strPayload = strPayload + chr(byte)
                qtdPulsosRec = Calcula_Pulsos(qtdPulsosRec, intByte, i)
                
                i = i + 1

            if (((tempo_inicial + 500) < (time() * 1000))):
            #if (i == 61):
                medidor = Obtem_Medidor(payload)

                print("Medidor......:", medidor)
                print("Contador.....:", str(qtdPulsosRec))
                i = 0
                leitura_concluida = True

                return (leitura_concluida, medidor, qtdPulsosRec)

    return (leitura_concluida, "         ", 0)

def Identifica_Medidor():
    for i in range(1, QT_MAX_FIELD):
        campo_tela = txt_box_id[i].get()
        print("Campo de tela lido: ", campo_tela)
        print("Medidor lido: ", medidor)
        if (medidor == campo_tela):
            print("Medidor encontrado na posição:", i)

            txt_Resultado[i].configure(state='normal')
            txt_Resultado[i].delete(0, tk.END)
            txt_Resultado[i].insert(0,"  PASSOU")
            txt_Resultado[i].configure(bg="green")
            tempo_inicial[i] = 0


            #chk_Dados_Recebidos[i].select();
            txt_Leitura_Inicial[i].configure(state='normal')
            txt_Leitura_Inicial[i].delete(0, tk.END)
            txt_Leitura_Inicial[i].insert(0,str(contador));
            txt_Leitura_Inicial[i].configure(state='disabled')
            print("contador..........:", str(contador));

#-----------reiniciar Teste----------#
            
def reiniciar_teste():
    #for entry in txt_box_id[1:]:
    for i in range(1,QT_MAX_FIELD):
        txt_box_id[i].delete(0, tk.END)
        txt_Leitura_Inicial[i].configure(state='normal')
        txt_Leitura_Inicial[i].delete(0, tk.END)
        txt_Leitura_Inicial[i].configure(state='disabled')
        txt_Leitura_Final[i].delete(0, tk.END)
    

        txt_Resultado[i].configure(state='normal')
        txt_Resultado[i].delete(0, tk.END)
        txt_Resultado[i].configure(state='disabled')
    txt_box_id[1].focus();

def Ciclo_Envio_Receb():

    #1. Configura portas seriais
    send_port    = serial.Serial(port='COM3', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)
    receive_port = serial.Serial(port='COM4', baudrate=9600  , parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)

    #2. Prepara dados e envia ao gerador de pulsos
    string = ""
    resp_erro = False
    payload = [0] * 62

    qtdPulsos    = str(41).zfill(4)
    tempoOn      = str(40).zfill(4)
    tempoOff     = str(40).zfill(4)
    pulsoStatus  = '1'
    pulsoNormal  = '1'
    pulsoReverso = '0'

    string = qtdPulsos + tempoOn + tempoOff + pulsoStatus + pulsoNormal + pulsoReverso + "\n"
    print("Comando enviado pela porta serial:", string)

    strSend = string.encode("utf-8")
    send_port.write(strSend)


    #3. Inicia o ciclo de leitura dos dados recebidos pela porta serial
    i = 0
    stringHexa = ""
    strPayload = ""
    qtdPulsosRec = 0

    while (leitura_concluida == False):

        #-- Executa loop realizando a leitura da porta serial
        for byte in receive_port.read():
            payload[i] = byte
            intByte = byte

            stringHexa = stringHexa + " " + hex(byte).zfill(4)[2:4]
            strPayload = strPayload + chr(byte)

            qtdPulsosRec = Calcula_Pulsos(qtdPulsosRec, intByte, i)

            #4. L? apenas 62 bytes, mostra na tela e depois aborta ciclo.
            if (i == 61):
                medidor = Obtem_Medidor(payload)

                print("Medidor......:", medidor)
                print("Contador.....:", str(qtdPulsosRec))
                i = 0
                qtdPulsosRec = 0
                leitura_concluida = True
                break;

            i = i + 1

    send_port.close()
    receive_port.close()


#-------------------------INTERFACE-------------------------------------#

root = tk.Tk()
root.title("Banco de testes de dispositivos de contagem de pulsos")
root.geometry("960x500")
root.configure(background=OBJ_BACKGROUND,)
root.update()
root.config(bg="lightblue")
icon = tk.PhotoImage(file="icon.png")
root.iconphoto(True, icon)

#============ imagem ===========================#

background_image = tk.PhotoImage(file="laager1.png")
label_image = tk.Label(root, image=background_image)
label_image.place(x=20, y=20,) 

#================================================#

lbl_box_id = [0] * QT_MAX_FIELD
txt_box_id = [0] * QT_MAX_FIELD
chk_box_id = [0] * QT_MAX_FIELD
txt_Leitura_Inicial = [0] * QT_MAX_FIELD
txt_Leitura_Final   = [0] * QT_MAX_FIELD
chk_Dados_Recebidos = [0] * QT_MAX_FIELD
chk_Leitura_OK      = [0] * QT_MAX_FIELD
chk_Leitura_NOK     = [0] * QT_MAX_FIELD
txt_Resultado = [0] *  QT_MAX_FIELD
tempo_atual = [0] *  QT_MAX_FIELD
tempo_inicial = [0] *  QT_MAX_FIELD

#send_port    = serial.Serial(port='COM3', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)
receive_port = serial.Serial(port='COM4', baudrate=9600  , parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)

#------------------CAMPOS BOX ID-----------------------#

for i in range(1, QT_MAX_FIELD):
    lbl_box_id[i] = tk.Label(root, text=f"Medidor {i}:", background=OBJ_BACKGROUND,bg="lightblue", foreground="#000000", anchor="e", font=("Bell MT", 12))
    lbl_box_id[i].place(x=10, y=110 + (i * 40), width=100, height=20)

    txt_box_id[i] = tk.Entry(root, font=("",10), highlightthickness=1, relief="solid")
    txt_box_id[i].place(x=113, y=110 + (i * 40), width=200, height=23, )
    txt_box_id[i].bind("<Key>", lambda event, index=i: Enter_Pressionado(event, index))

#-----------------RÓTULOS DAS COLUNAS------------------#

    lbl_titulo = tk.Label(root, text="Dados", background=OBJ_BACKGROUND, foreground="#000000",bg='lightblue', font=("Bell MT", 15))
    lbl_titulo.place(x=406, y=85)

    lbl_titulo = tk.Label(root, text="Recebidos", background=OBJ_BACKGROUND, foreground="#000000",bg='lightblue', font=("Bell MT", 15))
    lbl_titulo.place(x=393, y=115)

    lbl_titulo = tk.Label(root, text="Leitura", background=OBJ_BACKGROUND, foreground="#000000",bg='lightblue', font=("Bell MT", 15))
    lbl_titulo.place(x=552, y=85)

    lbl_titulo = tk.Label(root, text="Inicial", background=OBJ_BACKGROUND, foreground="#000000",bg='lightblue', font=("Bell MT", 15))
    lbl_titulo.place(x=556, y=115)

    lbl_titulo = tk.Label(root, text="Leitura", background=OBJ_BACKGROUND, foreground="#000000",bg='lightblue', font=("Bell MT", 15))
    lbl_titulo.place(x=680, y=85)

    lbl_titulo = tk.Label(root, text="Final", background=OBJ_BACKGROUND, foreground="#000000",bg='lightblue', font=("Bell MT", 15))
    lbl_titulo.place(x=685, y=115)

    lbl_titulo = tk.Label(root, text="Status", background=OBJ_BACKGROUND, foreground="#000000",bg='lightblue', font=("Bell MT", 15))
    lbl_titulo.place(x=820, y=115)

  
#-----------CAIXAS DE SELEÇÃO CHECKBOXES---------------#
    

    txt_Resultado[i] = tk.Entry(root, relief='solid',font=("Arial Black",10), highlightthickness=0)
    txt_Resultado[i].place(x=395, y=110 + (i * 40), width=80, height=20)


    #chk_Dados_Recebidos[i] = tk.Checkbutton(root, background=OBJ_BACKGROUND, state='disabled',)
    #chk_Dados_Recebidos[i].place(x=420, y=110 + (i * 30))

    txt_Leitura_Inicial[i] = tk.Entry(root, state='disabled',font=("Arial Black",10), highlightthickness=0, relief="solid")
    txt_Leitura_Inicial[i].place(x=555, y=110 + (i * 40), width=80, height=20)
   
    
    txt_Leitura_Final[i] = tk.Entry(root, state='disabled',font=("Arial",10), highlightthickness=0, relief="solid")
    txt_Leitura_Final[i].place(x=668, y=110 + (i * 40), width=80, height=20)

    chk_Leitura_OK[i] = tk.Entry(root, background=OBJ_BACKGROUND, state='disabled',font=("Arial",10), highlightthickness=0, relief="solid")
    chk_Leitura_OK[i].place(x=780, y=110 + (i * 40))

#---------------BOTÃO REINICIAR------------------------#

btn_reiniciar = tk.Button(root, text="Reiniciar Teste" ,command=reiniciar_teste,bd=2, bg='#17528c', fg="white", activebackground='#108ecb', activeforeground="white", font=('verdana', 10, 'bold'))
btn_reiniciar.place(x=113, y=400)

#---------------BOTÃO ENCERRAR-------------------------#

#btn_encerrar = tk.Button(root, text="Encerrar Programa", command=Encerrar_Programa)
#btn_encerrar.place(x=400, y=400)

#------------------------ PREPARA PARA INICIAR PROGRAMA ----------------------------

root.bind("<Destroy>", Fechar_Janela)

txt_box_id[1].focus()

#=========================== PROGRAMA PRINCIPAL ===================================#

ultima_atualizacao_tempo = int(time())
print("Ultima atualizacao de tempo: ", int(ultima_atualizacao_tempo))
while (encerrar_programa == False):

    #-- Atualiza a tela até que o programa seja fechado
    root.update()
    if (encerrar_programa == True):
        print("Hora de encerrar o programa....")
        root.quit()
        #root.destroy()

    #-- Aguarda passagem do imã no dispositivo
    if (leitura_concluida):
        Identifica_Medidor()
        leitura_concluida = False
    else:
        leitura_medidor   = Leitura_Medidor()
        leitura_concluida = leitura_medidor[0]
        medidor  = leitura_medidor[1]
        contador = leitura_medidor[2]

    if ((ultima_atualizacao_tempo + 1) < int(time())):
        atualizar_contador_tempo()
        ultima_atualizacao_tempo = int(time())
        #print("Momento atual: ", int(time()))
        #print("Ultima atualizacao do contador de tempo: ", str(ultima_atualizacao_tempo))


#========Atualize o Contador de Tempo:=============#


# ... Em algum lugar no código principal ou loop ...
#tempo_inicial = time() * 1000  # Marca o tempo inicial
