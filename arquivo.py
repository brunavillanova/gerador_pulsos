import serial
import datetime
from time import sleep
from time import time

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

def Enter_Pressionado(event, index):
    if event.keycode == 13:
        entry = event.widget
        print(entry.get())
        #entry = str(entry)
        i = index
        print("Pressionou <Enter>")
        print(str(i))
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
            chk_Dados_Recebidos[i].select();
            txt_Leitura_Inicial[i].configure(state='normal')
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
        chk_Dados_Recebidos[i].deselect();
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


import tkinter as tk


root = tk.Tk()
root.title("Banco de testes de dispositivos de contagem de pulsos")
root.geometry("1200x1200")
root.configure(background=OBJ_BACKGROUND)
root.update()
root.iconbitmap("icon.ico")
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

#send_port    = serial.Serial(port='COM3', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)
receive_port = serial.Serial(port='COM4', baudrate=9600  , parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)

#------------------CAMPOS BOX ID-----------------------#

for i in range(1, QT_MAX_FIELD):
    lbl_box_id[i] = tk.Label(root, text=f"Medidor {i}:", background=OBJ_BACKGROUND, foreground="#FFF", anchor="e", font=("Arial", 12))
    lbl_box_id[i].place(x=10, y=110 + (i * 30), width=100, height=20)

    txt_box_id[i] = tk.Entry(root)
    txt_box_id[i].place(x=113, y=110 + (i * 30), width=200, height=20)
    txt_box_id[i].bind("<Key>", lambda event, index=i: Enter_Pressionado(event, index))





#-----------------RÓTULOS DAS COLUNAS------------------#

    lbl_titulo = tk.Label(root, text="Dados", background=OBJ_BACKGROUND, foreground="#FFF",bg='#4682B4', font=("Arial", 12))
    lbl_titulo.place(x=406, y=80)

    lbl_titulo = tk.Label(root, text="Recebidos", background=OBJ_BACKGROUND, foreground="#FFF",bg='#4682B4', font=("Arial", 12))
    lbl_titulo.place(x=393, y=105)

    lbl_titulo = tk.Label(root, text="Leitura", background=OBJ_BACKGROUND, foreground="#FFF",bg='#4682B4', font=("Arial", 12))
    lbl_titulo.place(x=552, y=80)

    lbl_titulo = tk.Label(root, text="Inicial", background=OBJ_BACKGROUND, foreground="#FFF",bg='#4682B4', font=("Arial", 12))
    lbl_titulo.place(x=556, y=105)

    lbl_titulo = tk.Label(root, text="Leitura", background=OBJ_BACKGROUND, foreground="#FFF",bg='#4682B4', font=("Arial", 12))
    lbl_titulo.place(x=697, y=80)

    lbl_titulo = tk.Label(root, text="Final", background=OBJ_BACKGROUND, foreground="#FFF",bg='#4682B4', font=("Arial", 12))
    lbl_titulo.place(x=703, y=105)

    lbl_titulo = tk.Label(root, text="Passou", background=OBJ_BACKGROUND, foreground="#FFF",bg='#4682B4', font=("Arial", 12))
    lbl_titulo.place(x=815, y=105)

    lbl_titulo = tk.Label(root, text="Não Passou", background=OBJ_BACKGROUND, foreground="#FFF",bg='#4682B4', font=("Arial", 12))
    lbl_titulo.place(x=950, y=105)

    lbl_contador_tempo = tk.Label(root, text="Contador de Tempo:", background=OBJ_BACKGROUND, foreground="#FFF",bg='#4682B4', font=("Arial", 12))
    lbl_contador_tempo.place(x=800, y=10, width=150, height=20)

    contador_tempo = tk.StringVar()
    lbl_tempo = tk.Label(root, textvariable=contador_tempo,)
    lbl_tempo.place(x=960, y=10, width=100, height=20)


#-----------CAIXAS DE SELEÇÃO CHECKBOXES---------------#
    
    chk_Dados_Recebidos[i] = tk.Checkbutton(root, background=OBJ_BACKGROUND, state='disabled',)
    chk_Dados_Recebidos[i].place(x=420, y=110 + (i * 30))

    txt_Leitura_Inicial[i] = tk.Entry(root, state='disabled')
    txt_Leitura_Inicial[i].place(x=555, y=110 + (i * 30), width=50, height=20)

    txt_Leitura_Final[i] = tk.Entry(root, state='disabled')
    txt_Leitura_Final[i].place(x=700, y=110 + (i * 30), width=50, height=20)

    chk_Leitura_OK[i] = tk.Entry(root, background=OBJ_BACKGROUND, state='disabled' ,foreground="#228B22",bg='#228B22',)
    chk_Leitura_OK[i].place(x=780, y=110 + (i * 30))

    chk_Leitura_NOK[i] = tk.Entry(root, background=OBJ_BACKGROUND,state='disabled' , foreground="#FF0000",bg='#FF0000',)
    chk_Leitura_NOK[i].place(x=950, y=110 + (i * 30))

#---------------BOTÃO REINICIAR------------------------#

btn_reiniciar = tk.Button(root, text="Reiniciar Teste", command=reiniciar_teste)
btn_reiniciar.place(x=113, y=400)

#---------------BOTÃO ENCERRAR-------------------------#

#btn_encerrar = tk.Button(root, text="Encerrar Programa", command=Encerrar_Programa)
#btn_encerrar.place(x=400, y=400)

#------------------------ PREPARA PARA INICIAR PROGRAMA ----------------------------

root.bind("<Destroy>", Fechar_Janela)

txt_box_id[1].focus()

#=========================== PROGRAMA PRINCIPAL ===================================#

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

#========Atualize o Contador de Tempo:=============#

def atualizar_contador_tempo():
    tempo_atual = int((time() - tempo_inicial) / 1000)  # Tempo em segundos
    contador_tempo.set(f"{tempo_atual} s")

# ... Em algum lugar no código principal ou loop ...
tempo_inicial = time() * 1000  # Marca o tempo inicial

while (encerrar_programa == False):
    # ... Seu código existente ...
    atualizar_contador_tempo()
    root.update()
