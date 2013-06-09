#! /usr/bin/python

class Separar():
    def Separar(self, numero):
      self.numero = numero
      j=0
      i=0
      v1 = ' '
      v2 = ' '
      n = len(numero)

      while i<n:
          if j== 0:
            if numero[i] != ' ':
              v1 += numero[i]
              i += 1
            else:
              if numero[i] == ' ':
                i += 1
              j = 1 
          else:
            if j==1:
              v2 += numero[i]
              i += 1

      numero1 = float(v1)
      numero2 = float(v2)

      return numero1, numero2
