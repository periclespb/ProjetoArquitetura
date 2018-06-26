# -*- coding: utf-8 -*-
'''
00000000 	NOP
00000001	load da memoria para registrador
00000010	load do registrador para memoria
00000011	and
00000100	or
00000101	not
00000110	add
00000111	sub
00001000	eq
00001001	neq
00001010	maior 
00001011	menor
00001100	jump
00001101	print
00001110	end
00001111
'''

class ULA:

        def __init__(self):
		#Flags
		self.sign = False
		self.overflow = False
		self.zero = False
		#criando a pilha
        self.pilha= []
        self.mbr = 0b0

	def imprimir(self):
		print"\n -- ULA --\nSign:\t\t" +str (self.sign) + "\nOverflow:\t" + str(self.overflow) + "\nZero:\t\t" + str (self.zero)+ "\n\nItens na pilha:"
		tmp="\t=> "
		for i in self.pilha:
			tmp = tmp+str(i) + "\t"
		if (tmp =="\t=> "):
			tmp = "-> Empty"
		print str (tmp)

	def pop(self):
		return self.pilha.pop(0)
	def getFlags(self):
		return self.sign, self.overflow, self.zero
        def load (self, a):
                self.pilha.append(bin(int (a, 2)))
        def orOp(self):

                ss1= eval(self.pilha[0])
                for i in range (1, len ( self.pilha)):
                        ss1 =ss1 or eval (self.pilha[i])
                self.mbr = ss1
                self.pilha = []

        def andOp(self):
                ss1= eval(self.pilha[0])
                for i in range (1, len ( self.pilha)):
                        ss1 =ss1 and eval (self.pilha[i])
                self.mbr = ss1
                self.pilha = []

        def notOp(self):
                ss1= eval(self.pilha[0])
                self.mbr = not ss1
                self.pilha = []

        def addOp(self):
                ss1= eval(self.pilha[0])
                for i in range (1, len ( self.pilha)):
                        ss1 =ss1 + eval (self.pilha[i])
                self.mbr = ss1
		if ss1 > 255:
			print "\033[91mULA-> Overflow. \033[0m\n"
		
		print "\033[91mSIGN-> Flase. \033[0m\n"
		if ss1 == 0:
			print "\033[91mSIGN-> False. \033[0m\n"
			print "\033[91mZERO-> False. \033[0m\n"
                self.pilha = []

        def subOp(self):
                ss1= eval(self.pilha[0])
                for i in range (1, len ( self.pilha)):
                        ss1 =ss1 - eval (self.pilha[i])
                self.mbr = ss1
		if ss1 > 127 or ss1 < -127:
			print "\033[91mULA-> Overflow. \033[0m\n"
		if ss1 < 0:
			print "\033[91mSIGN-> True. \033[0m\n"
		elif ss1 >0 :
			print "\033[91mSIGN-> Flase. \033[0m\n"
		elif ss1 == 0:
			print "\033[91mSIGN-> Flase. \033[0m\n"
			print "\033[91mZERO-> Flase. \033[0m\n"
                self.pilha = []

        def maiorOp(self):

        ss1= eval(self.pilha[0])
		ss2 = eval(self.pilha[1])
		if (ss1 > ss2):
			self.mbr = 1
		else:
			self.mbr = 0
            self.pilha = []


        def menorOp(self):

        ss1= eval(self.pilha[0])
		ss2 = eval(self.pilha[1])
		if (ss1 < ss2):
			self.mbr = 1
		else:
			self.mbr = 0
            self.pilha = []

        def eqOp(self):
                ss1= eval(self.pilha[0])
		ss2 = eval(self.pilha[1])
		if (ss1 == ss2):
			self.mbr =1 
		else:
			self.mbr = 0
                self.pilha = []



        def getMbr(self):
                ss1 = self.mbr
                self.mbr = 0b0
                return ss1


		
				
class Palavra:
	def __init__(self):
		self.opcode = "00000000"
		self.address = "00000000"
	def set (self, data):
		self.opcode = data [0:8]
		self.address = data[8:16]
	def isEmpty(self):
		if (self.opcode == "00000000" and self.address == "00000000"):
			return True
		return False
	def toString(self):
		return self.opcode + " "+ self.address	
	def getOp(self):
		return self.opcode
	def getAddress(self):
		return self.address

class Memoria:
	def __init__ (self):
		self.memory = [0]* 50 # de 1 a 10 sao variaveis

	def add (self, address, value):
		self.memory[address] = value

	def get (self, address):
		return self.memory [address]

	def getInt (self, address):
		return int (self.memory[address].getOp(), 2)
		#return int (self.memory [address].getAddress(),2)
	def imprimir (self):
		for i in range (len(self.memory)):
			if self.memory[i] != 0:
				print "M["+ str (i)+"]= "+ str (self.memory[i].toString())#.toString 
			

class UC:
	def __init__ (self):
		self.base = 10
		self.end= False
		self.memoria = Memoria()
		self.ula = ULA()
		self.ibr = Palavra()	#guarda codigo de proxima instrucao quando fica guardado em mesma posicao de memoria (palavra se divide em duas operacoes)
		self.ir = "00000000"		#guarda o codigo de operacao 
		self.pc = self.base 			#guarda posicao do contador de programa
		self.mar = Palavra() 	#registrador de endereços
		
		
	def fetch(self):
		if self.ibr.isEmpty():  #instrução não está no IBR ,devemos buscar na memoria
			self.mar = self.pc
			self.mbr = self.memoria.get (self.mar)
			#apenas uma instrucao por palavra
			self.ir = self.mbr.getOp() #carregar apenas a parte da instrucao da palavra
			print "Instrução Carregada:" + str (self.ir)+"\n"
			self.mar = self.mbr.getAddress()
		else: #instrucao no IBR
			pass

	def getEnd(self):
		return self.end
	def run(self):
		#decodifica instrucao no IR
		if self.ir == "00000000":  #do nothing
			pass
		if self.ir == "00000001":  #MOVR 
			self.ula.load(self.memoria.get(int(self.mar, 2)).getAddress())
		elif self.ir =="00000010":  #MOVM
			dado = self.ula.pop()
			print ("dado obtido "+str (dado)+ "\n\n")
			resp = Palavra()
			resp.set("00000000" + "{0:#b}".format(int(dado,2)).replace("0b",""))
			self.memoria.add(int (self.mar,2),resp)
		elif self.ir == "00000011": #and
			self.ula.andOp()
			resp = Palavra()
			resp.set(  "{0:#b}".format(int(self.ula.getMbr())).replace("0b",""))
			if self.mar != "00000000":
				self.memoria.add(self.mar, resp)
			self.memoria.add(6, resp) #senao salva em tmp1
		elif self.ir == "00000100": #	or
			self.ula.orOp()
			resp = Palavra()
			resp.set(  "{0:#b}".format(int(self.ula.getMbr())).replace("0b",""))
			if self.mar != "00000000":
				self.memoria.add(self.mar, resp)
			self.memoria.add(6, resp) #senao salva em tmp1
		elif self.ir == "00000101": #	not
			self.ula.notOp()
			resp = Palavra()
			resp.set(  "{0:#b}".format(int(self.ula.getMbr())).replace("0b",""))
			if self.mar != "00000000":
				self.memoria.add(self.mar, resp)
			self.memoria.add(6, resp) #senao salva em tmp1
		elif self.ir == "00000110": 	#ADD
			self.ula.addOp()
			resp = Palavra()
			resp.set(  "{0:#b}".format(int(self.ula.getMbr())).replace("0b",""))
			if self.mar != "00000000":
				self.memoria.add(int (self.mar), resp)
			self.memoria.add(6, resp) #senao salva em tmp1
		elif self.ir == "00000111":	#SUB
			self.ula.subOp()
			resp = Palavra()
			resp.set(  "{0:#b}".format(int(self.ula.getMbr())).replace("0b",""))
			if self.mar != "00000000":
				self.memoria.add(self.mar, resp)
			self.memoria.add(6, resp) #senao salva em tmp1
		elif self.ir == "00001000": 	#EQ
			self.ula.eqOp()
			resp = Palavra()
			resp.set(  "{0:#b}".format(int(self.ula.getMbr())).replace("0b",""))
			if self.mar != "00000000":
				self.memoria.add(self.mar, resp)
			self.memoria.add(6, resp) #senao salva em tmp1
		elif self.ir == "00001001":	#NEQ
			self.ula.neqOp()
			resp = Palavra()
			resp.set(  "{0:#b}".format(int(self.ula.getMbr())).replace("0b",""))
			if self.mar != "00000000":
				self.memoria.add(self.mar, resp)
			self.memoria.add(6, resp) #senao salva em tmp1
		elif self.ir == "00001010":	#MAIOR 
			self.ula.maiorOp()
			resp = Palavra()
			resp.set(  "{0:#b}".format(int(self.ula.getMbr())).replace("0b",""))
			if self.mar != "00000000":
				self.memoria.add(self.mar, resp)
			self.memoria.add(6, resp) #senao salva em tmp1
		elif self.ir == "00001011":#menor
			self.ula.menorOp()
			resp = Palavra()
			resp.set(  "{0:#b}".format(int(self.ula.getMbr())).replace("0b",""))
			if self.mar != "00000000":
				self.memoria.add(self.mar, resp)
			self.memoria.add(6, resp) #senao salva em tmp1
		elif self.ir == "00001100":#	jump
			self.pc = self.base + int (self.mar,2)-1
			#basicamente pc vai para a linha do endereco 
			pass
		elif self.ir == "00001101":#	print
			print "\033[93m Saída padrão: M[" + str (self.mar) + "]="+ str (self.memoria.getInt(int(self.mar,2))) + "\n\033[0m"
		elif self.ir == "00001110":# input
			ss1 = input ("digite o valor ")
			self.memoria.set(self.mar, ss1)
		elif self.ir == "00001111":# load in register 
			self.ula.load(self.mar)
		elif self.ir == "00010000":# Fim do programar 
			print "\033[92m Instrução fim de programa.\033[0m"
			self.end = True
		elif self.ir == "00010001":#loadm
			valor = self.ula.pop()
			resp = Palavra()
			resp.set("00000000" + "{0:#b}".format(int(valor,2)).replace("0b",""))
			self.memoria.add(int (self.mar,2),resp)
		self.pc += 1

class Montador ():
	def __init__ (self):
		self.instset = {"dod": "00000000", "movr": "00000001", "movm": "00000010", "and": "00000011", "or": "00000100",  "not": "00000101", "add" : "00000110", "sub": "00000111", "eq": "00001000", "neq":"00001001", "g": "00001010", "l":"00001011", "jump":  "00001100", "print": "00001101", "input":"00001110", "loadr":"00001111", "end": "00010000", "loadm":"00010001"}
		self.memReg = {"s1":1, "s2":2, "s3":3, "s4":4, "s5":5, "tmp1":6}

	def avaliar (self, string):
		string = str(string)
		if len (string.split (" ")) > 1:
			op, address = string.split (" ")
			if address in self.memReg.keys():
				address = self.memReg[address]
			op = self.instset[op]
			return  str (op)  +  "{0:#b}".format(int(address)).replace("0b","") 
		return str (self.instset[string] + "000000000")

mont = Montador()
instrucao = "inicio"
uc = UC()
end = 10 #incio das instrucoes na memoria
print "\nLeitura de instruções:\n"
while (instrucao != "0"):
	instrucao = input ("digite uma instrucao:")
	if instrucao == "0": 
		break 
	palavra = Palavra()
	palavra.set (mont.avaliar(instrucao))
	uc.memoria.add (end , palavra)
	end+=1
print "\nAlocação de dados na memória antes da execução:\n"
uc.memoria.imprimir()
uc.ula.imprimir()
uc.base = 10
while  not uc.getEnd():
	print "\n --- Início de ciclo: PC - "+ str (uc.pc)+ "  ----\n"
	uc.fetch()
	uc.run()
	uc.memoria.imprimir()
	uc.ula.imprimir()

