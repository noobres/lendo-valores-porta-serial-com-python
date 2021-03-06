import tkinter as tk
from tkinter import font
 
import sys
import serial
# importa a biblioteca pyserial
 
class myApp(object):
     
    def __init__(self, **kw):
        #insira toda a inicialização aqui
                            
        self.root = tk.Tk()
        self.root.title("Interface Tk tempNTC")
        self.root.geometry('550x300')
        self.create_menu_bar()
        self.create_canvas_area()
        self.create_status_bar()
         
        self.idPorta= "/dev/ttyACM0"
        self.msgRecebida = "" 
         
        # abre a  porta disponível
        try:
            self.portaSerial = serial.Serial(port=self.idPorta,timeout=10)   
  
        except serial.SerialException as e:
            sys.stderr.write("Impossivel abrir porta  %r: %s\n" % (port,e))
            sys.exit(1)     
         
        self.leSerial()
         
     
     
     
    def leSerial(self):
        """
        este método le um caracter por vez da porta serial
        """
        if self.portaSerial.isOpen():   #so faz a leitura se a porta estiver aberta
            while self.portaSerial.inWaiting() > 0: 
                # se tiver 1(um) ou mais caracteres na recepção da porta serial  
                caracLido = self.portaSerial.read(1)
                #le o próximo caracter disponível
                self.decodificaComando(caracLido)
                #apenda o caracter aos lidos anteriormente procurando montar
                #um comando. Se um comando tiver sido montado, executa o mesmo
        self.root.after(1,self.leSerial)   
                #daqui a 1 milisegundo volta a executar a leSerial, procurando
                #por outro caracter
         
     
    def decodificaComando(self,caracLido):
             
        if caracLido.decode() != '\n':
            self.msgRecebida += caracLido.decode()
             
             
        else:
            msg1= self.msgRecebida.replace('\n'," ")
             
            
            cmd,param= msg1.split(",")
                     
             
            if cmd == "$0":
                saida= "Versão: " + param
                self.text1.insert(tk.END, saida + '\n')  
            if cmd == "$1":
                saida= "Temperatura: " + param
                self.text1.insert(tk.END, saida + '\n') 
                 
            self.msgRecebida= ""
         
         
         
         
    def create_status_bar(self):
        self.status = tk.Label(self.root,
                               text="Bemvindo a Interface tk tempNTC",
                               bd=1, relief=tk.SUNKEN)
        self.status.pack(side= tk.BOTTOM, fill = tk.X)
 
 
 
    def clear_status_bar(self):
        self.status.config(text="")
        self.status.update_idletasks() 
         
    def set_status_bar(self, texto):
        self.status.config(text=texto)
        self.status.update_idletasks()       
 
    def create_menu_bar(self):           
        menubar = tk.Menu(self.root)
         
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.finaliza_software)
        
        
        menubar.add_cascade(label="File", menu=filemenu)
         
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.mnu_about)
        menubar.add_cascade(label="Help", menu=helpmenu)
         
        self.root.config(menu=menubar)
 
    def create_canvas_area(self):
        self.lbl1 = tk.Label(self.root, text="Interface tempNTC",fg= "blue", font= ("Arial" ,"28", "bold"))
 
         
        self.text1 = tk.Text(self.root, height=10, width=60)
        self.text1.insert(tk.END, "\t\tPronto para entrar em operação!\n")
        self.text1.insert(tk.END, "\tNão esqueça configuração da porta serial\n")
 
         
         
        self.frame1 = tk.Frame(self.root)
         
        self.btnVersao= tk.Button(self.frame1, text = "Versão?",command=self.sendMsg0)
        self.btnTemp= tk.Button(self.frame1, text = "Temperatura?",command=self.sendMsg1)
        self.btnIntervalo= tk.Button(self.frame1, text ="Intervalo:",command=self.sendMsg2)
        self.entry1= tk.Entry(self.frame1,width=5 )
        self.entry1.insert( 0,"10")
         
        self.btnVersao.pack(side = tk.LEFT, padx= 10, pady= 15)
        self.btnTemp.pack(side = tk.LEFT,  padx= 10, pady= 15)
        self.btnIntervalo.pack(side = tk.LEFT, padx= 10, pady= 15)
        self.entry1.pack(side = tk.LEFT,pady= 15)
                 
        self.lbl1.pack()
        self.text1.pack()
        self.frame1.pack()
         
         
         
         
         
    def finaliza_software(self):
        if self.portaSerial.isOpen():
            self.portaSerial.close()
        self.root.quit()       
     
         
    def mnu_about(self):
        pass
  
     
    def execute(self):
        self.root.mainloop()
 
 
    def sendMsg0(self):
        if self.portaSerial.isOpen():
            msg= "0\n"
            self.portaSerial.write(msg.encode());
             
    def sendMsg1(self):
        if self.portaSerial.isOpen():
            msg= "1\n"
            self.portaSerial.write(msg.encode());  
 
    def sendMsg2(self):
        if self.portaSerial.isOpen():
            msg= "2,"
            msg += self.entry1.get()
            msg += "\n"
            self.portaSerial.write(msg.encode()); 
 
 
 
def main(args):
    app_proc = myApp()
    app_proc.execute()
    return 0
 
 
if __name__ == '__main__':
    sys.exit(main(sys.argv))
