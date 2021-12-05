# -*- coding: utf-8 -*-

# The present version of JCalc has been programmed on Python 3.8 & Numpy.
# It is a scientific and technical oriented calculator (not finances or computer science...)
# Press the "hlp" button in the interface for more info.

#  Copyright 2021 Juan Carlos del Caño
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

from tkinter import *
from tkinter import ttk, messagebox, filedialog

import numpy as np
from fractions import Fraction

from os import kill, getppid
import signal


class Gui:
    
    def __init__(self):

        self.v0=Tk()
        self.v0.title('JCalc')

        self.estilo = ttk.Style()
        self.estilo.configure('jc_blue.TCheckbutton', background='#D7ECFF')
        self.estilo.configure('jc_green.TCheckbutton', background='#DAFFD7')
        self.estilo.configure('jc.TLabelframe.Label', foreground ='green')
        self.estilo.configure('jc_blue.TFrame', background='#D7ECFF')
        self.estilo.configure('jc_blue.TLabel', font='mono 14', background='#D7ECFF')
        #self.estilo.configure('jc_white.TEntry', 
                      #background=[('readonly','white'),('active','white')] )

        self.frame_general = ttk.Frame(self.v0, padding='4', style='jc_blue.TFrame')
        self.frame_general.grid(sticky=(N, W, E, S))

        self.frame_irst= ttk.Frame(self.frame_general, style='jc_blue.TFrame')
        self.frame_irst.grid(column=0,row=0,ipadx=3)

        self.frame_botones= ttk.Frame(self.frame_general, style='jc_blue.TFrame')
        self.frame_botones.grid(column=1,row=0,ipadx=3)
        
        self.pila= [0.,0.,0.,0.]
        self.pila_strv=[StringVar(value='0'),StringVar(value='0'),
                        StringVar(value='0'),StringVar(value='0')]
        self.entries_wgt=[ 
            Entry(self.frame_irst, textvariable=self.pila_strv[0], font=('mono',14), width=30,
                background='#D9D9D9'),
            Entry(self.frame_irst, textvariable=self.pila_strv[1], font=('mono',14), width=30, state=(['disabled']), disabledforeground='black'),
            Entry(self.frame_irst, textvariable=self.pila_strv[2], font=('mono',14), width=30, state=(['disabled']), disabledforeground='black'),
            Entry(self.frame_irst, textvariable=self.pila_strv[3], font=('mono',14), width=30, state=(['disabled']), disabledforeground='black' ) ]

        a=['i:','r:','s:','t:']
        for i in range(4):
            ttk.Label(self.frame_irst, text=a[i], style='jc_blue.TLabel').grid(
                    row=3-i, column=0, padx=4, sticky='w')            
            self.entries_wgt[i].grid(row=3-i, column=1, sticky='e')


        self.cifras_strv = StringVar(value='6')
        self.cifras_wgt = ttk.Spinbox(self.frame_botones, from_=1, to=12, width=2, 
                        textvariable=self.cifras_strv, command=self.poner_cifras,
                        state='readonly')
        self.cifras_wgt.grid(row=0, column=1, padx=2, pady=2, sticky='w')
        ttk.Label(self.frame_botones, text='fix ', style='jc_blue.TLabel', font=('mono',11)).grid(
                    row=0, column=0, sticky='e')

        self.rad_strv= StringVar(value='0')
        self.Cdeg= np.pi/180
        self.rad_wgt= ttk.Checkbutton(self.frame_botones, variable=self.rad_strv, 
                                      style='jc_blue.TCheckbutton', command=self.pon_Cdeg)
        self.rad_wgt.grid(row=1, column=1, padx=2, pady=2, sticky='w') 
        ttk.Label(self.frame_botones, text='rad ', style='jc_blue.TLabel', font=('mono',11)).grid(
                    row=1, column=0, sticky='e')
        
        self.hlp_strv= StringVar(value='0')
        self.help_wgt= ttk.Checkbutton(self.frame_botones, variable=self.hlp_strv, onvalue='1',
                    offvalue='0', style='jc_blue.TCheckbutton', command=self.ayuda)
        self.help_wgt.grid(row=2, column=1, padx=2, pady=2, sticky='w') 
        ttk.Label(self.frame_botones, text='hlp ', style='jc_blue.TLabel', font=('mono',11)).grid(
                    row=2, column=0, sticky='e')

        self.estoy_poniendo, self.mover_pila = False, False
        self.entries_wgt[0].configure(background='white')
        self.mem, self.lasti = 0., 0.

        self.v0.bind('<KeyPress>', self.tecla_pres)
        self.entries_wgt[0].focus()
        self.v0.protocol('WM_DELETE_WINDOW', self.salir)
        self.v0.mainloop()


    def ayuda(self):
        
        def cierrayuda():
            self.hlp_strv.set('0')
            self.v1.destroy()
            self.entries_wgt[0].focus()
            
            
        texto = '''
JCalc: the computer desktop calculator by JC. No more, no
less! Notes & license at the end.

                    PLEASE START HERE
____________________________________________________________

- The present version of JCalc has been programmed in
Python 3.8 with NumPy as The only dependence. It's intended
for tech & scientific calculations (not financial etc).

- JCalc uses reverse polish notation (RPN), the efficient
notation introduced by polish mathematician Jan Lukasiewicz.
Like any calculator, it benefits from the use of a KeyPad
but it's not a requirement.

- The stack's registers are named i,r,s,t (instead of 
x,y,z,t, as found in HP calculators). That's because when 
operating with complex numbers the R_eal part will lie in r,
and the I_maginary part will lie in i. Ditto for the R_adius
and the argument (angle) of the complex number. As real-imag
is often associated with x-y (not the other way around), the
present denomination aims for better mnemonics.

- Enter (from KeyPad) or Return (from keyboard) makes the 
stack to go up (r,s,t become previous i,r,s), and i gets 
ready to receive a new number from the user. The number 
currently in i will be erased when typing starts, but it 
will not be lost as it is copied in r. 

- An unary function, say 's' which stands for 'sin', will
be applied to i. A binary function, as basic arithmetics 
+-*/ are, will take i&r as arguments and place the answer
on i (when the result of the operation is a single number).
The stack will move down (s,r=t,s). When you start typing
a new number, the stack moves up automatically. 

- For a power of 10 use the 'e' character when typing. For
example, 2.2e4 is equivalent to 22000.

- A negative number is obtained by writing it as positive,
then applying the 'change sign' function which is assigned
to the space bar. This function also works on an existing
number in i. For a negative power of 10, type '-' after 'e'.
In this situation '-' will remain as a character instead of
invoking the subtraction function. For example, -0.00022 can
be obtained by the key sequence '2.2e-4' and then space.

- Lowercase keys are in general associated with direct 
functions. Thus s,c,t,l will call the sin, cos, tan, log_e
operations. Their inverses are associated with S,C,T,L. 
Please note: the key sequence '1L' will produce the number
e, the base of natural logarithms (2.718...).

- The backspace key deletes a single character when you are
writing a number. Otherwise, it erases the i register. The
left and right arrows move the cursor when you're writing
a number. They don't act otherwise. Sometimes a cursor 
appears when you are not editing a number. Ignore it.

- As a redundant, perhaps handy feature, the i background
gets white when your eventual typing will not lead to a
stack push. This is the case when you're typing, after
some typing errors, and after Enter/Return. If a stack
push will occur at your typing, the i background will be
grey.


                KEYBOARD & FUNCTIONS GUIDE
____________________________________________________________
                 Writing a number (on i):
                
0..9                            Digits 0..9    (characters)
.                               Decimal point   (character)
e                               Exponent of 10 (character)
space bar "esp" (or ñ)          Change sign (function)
          Note: after 'e', any of the keys esp, ñ, -, will
          write the character '-' right in your input 
          instead of calling any function. You can carry on
          with your input afterwards.
____________________________________________________________
                Stack management (i,r,s,t):
                
Enter or Return:   Move up the stack: t=s, s=r, r=i
                   The number on i is duplicated in r, and
                   the number on t is lost. If you start 
                   writing a new number afterwards, it will
                   replace the current content of i. This is
                   core management in JCalc. For example:
                   '3 Enter 2 +' leads to 5 (=3+2).
up arrow:          Also pushes up the stack, but the content
                   of t moves to i (instead of being lost).
down arrow:        Moves down the stack. The content of i
                   goes to t.
x                  Exchanges the values on i, r
          Note: Only the first among the previous functions
          (Enter/Return) disables stack displacement. Almost
          any other function in the calculator leaves 
          enabled the stack displacement (when you start 
          writing a new number, the stack moves up and t is
          lost).
____________________________________________________________
                     Basic arithmetics:

+  performs r+i leaving the result on i
-     "     r-i    "            "        (except after "e")
*     "     r*i    "            "
/     "     r/i    "            "
          Note: The stack moves down with these operations:
          r=s, s=t, leaving s & t with the same value.
____________________________________________________________
                      Unary functions:

s,c,t         replaces the value on i with its sin, cos, tg.
S,C,T         idem. arc sin, arc cos, arc tg.
l,k           idem. natural logarithm, 10-base logarithm
L,K           idem. antilogs e^i & 10^i, respectively.
i,r           idem. inverse, square root
!             idem. factorial (for integer values < 170)
          Notes: 
          - The above functions leave rst untouched and the 
          stack displacement enabled.
          - Angles, when applicable, are understood/given
          in degrees or radians according with the selector
          on the right of the interface, 
____________________________________________________________
                        Raise to power:

p             Leaves on i the result of r^i. The stack moves
              down and stack displacement is enabled (other
              binary functions as +-*/ behave similarly).
____________________________________________________________
                        Complex numbers:

j             Leaves i with the complex number r+i*j.
J             When i contains a complex number, leaves on r
              its real part, on i its imaginary part.
n             Leaves on i the complex number with radius r
              and argument i (in the form real+imag*j)
N             When i contains a complex number, leaves on r
              its radius, on i its argument (angle)
          Notes:
          - All operations in JCalc do support complex 
          arguments (if it makes sense in the first place).
          - A complex number in a register will always be
          shown as real+imag*j
          - When multiple answers are possible, the one with
          the lesser argument is given as the result.
          - Remember to operate in radians when using 
          trigonometric functions in the complex field.
          - As a security feature, an error is raised when
          you are operating in the real field and attempt an
          operation which is only possible in the complex
          field. For example, to perform (-5)^(1/2) you must
          start with -5+0j (then press the r key).
          - Mnemonics: operations with 'n' (as in norm) 
          involve the norm (radius) of the complex number.
____________________________________________________________
                        Memory register:

m             The number on i is stored for future use.
M             Retrieves to i the stored number and pushes up
              the stack.
____________________________________________________________
                        Special actions:

y             Special function "last i": push up the stack
              and brings to i the content it had before the
              last operation. Does not apply to P (pi) or M
              (memory register).
P             Brings number pi (3.14...) to i, pushes up the
              stack and leaves its displacement enabled.
f             Approximates i (decimal number) by the best 
              fraction with denominator lesser than 100000. 
              Numerator on r, denominator on i.
BackSpace     When typing a number, it erases characters one
              at a time. Otherwise, it deletes the i content
              and disables the stack displacement. Thus, you
              can start typing a new number with no effects
              on the rest of the stack.
Escape        When typing a number, it is discarded and 
              brings to i its last valid content. Stack 
              displacement results disabled.
z             Reset. Takes to zero all registers, memory and
              "last i" included.
____________________________________________________________
                      Fields on the right side:

fix           Sets the number of significant figures to be 
              shown in the i,r,s,t, registers. Does not
              affect the precission of the operations. Only 
              relevant figures are shown in any case.
rad           When pressed, angles are taken/retrieved
              in radians. When it is released, operations
              are based on degrees.
hlp           Show or hide this text. You can also close the
              window to hide it.
____________________________________________________________

The author offers JCalc under Gnu's GPL v3 license, in the
hope that it will be useful and assuming that a calculator
should be a handy tool to perform direct calculations. The
author thinks JCalc does this in a very efficient manner.
For further features (matrices, function solvers etc) a
specialized framework like Octave or a programming language
like Python or Julia are considered more suitable options.

If you have an eye on the code, you may find similar chunks
that could be a target for optimization (for example by
making a function). However, this kind of "optimization" has
been considered unsuitable in this case, as responsiveness
has been the priority. Also, the two-level grouping of keys
in the function tecla_pres() may seem redundant at first
glance. Its purpose is again to get a faster triage.

If the key assignments are not of your liking, I encourage
you to go for a different choice by editing the code. All
the relevant logic is inside the tecla_pres() function.


                                    The author:
                                    Juan Carlos del Caño
____________________________________________________________
'''
        if self.hlp_strv.get()=='0':
            cierrayuda()
        else:
            self.v1=Toplevel(self.v0)
            self.v1.title('JCalc')

            tcaja = Text(self.v1, width=60, height=34,wrap='word', font=('Mono',9),
                background='#EDECEB', foreground='green', border=None, padx=5, pady=12)
            tcaja.grid(column=0, row=1, padx=8, sticky=(N,W,E,S))
            tcaja.insert('1.0',texto)

            scb = ttk.Scrollbar(self.v1, orient=VERTICAL, command=tcaja.yview)
            scb.grid(column=1, row=1, sticky='ns')
            
            tcaja['yscrollcommand'] = scb.set

            tcaja['state']='disabled'

            self.v1.grid_columnconfigure(0, weight=1)
            self.v1.grid_rowconfigure(0, weight=1)
            self.v1.grid_rowconfigure(1, weight=4)
            self.v1.grid_rowconfigure(2, weight=1)
            self.v1.geometry('+240+60')

            self.v1.protocol('WM_DELETE_WINDOW', cierrayuda)
            self.v1.mainloop()


    def flashes(self,a ):
        # a es un color de background no rojo: '#D9D9D9' (gris) ó 'white'
        self.entries_wgt[0].configure(background='#FF8B81', foreground='white')

        self.v0.after(1200, lambda : self.entries_wgt[0].configure(background=a, foreground='black') )
        self.v0.after(900, lambda : self.entries_wgt[0].configure(background='#FF8B81', foreground='white') )
        self.v0.after(600, lambda : self.entries_wgt[0].configure(background=a, foreground='black') )
        self.v0.after(300, lambda : self.entries_wgt[0].configure(background='#FF8B81', foreground='white') )


    def poner_en_strv(self, *args):
        j=0 if len(args)==0 else args[0]
        b='{:.' + self.cifras_strv.get() + 'g}'
        for i in range(j,4):
            self.pila_strv[i].set(b.format(self.pila[i]))
        self.entries_wgt[0].focus()


    def poner_cifras(self):
        if self.estoy_poniendo:
            try:
                self.pila[0]=float(self.pila_strv[0].get()) # no se mete caracter
                self.estoy_poniendo=False
            except:
                self.flashes('white')
                return()
        self.poner_en_strv(0)
        self.entries_wgt[0].focus()
        self.entries_wgt[0].icursor('end')
    
    def pon_Cdeg(self):
        self.Cdeg= np.pi/180 if self.rad_strv.get()=='0' else  1.
        self.entries_wgt[0].focus()
        self.entries_wgt[0].icursor('end')


    def tecla_pres(self, evento):
        print(evento)

        ks, ch = evento.keysym, evento.char
        if not len(ch): ch='ª' # si no se lía con '' de len=0 (flechas...)
        self.entries_wgt[0].focus()
        
        if ch in '0123456789.e': # escribiendo un numero en KeyPad
            self.entries_wgt[0].configure(background='white') # si estoy poniendo -> white a piñon
            
            if self.estoy_poniendo: # chequeo provisional. Evita estados inesperados
                a = self.pila_strv[0].get()
                if a.count('.')>1 or a.count('e')>1:
                    self.flashes('white')
                    return()
            else:
                if self.mover_pila:
                    self.pila[3]=self.pila[2]
                    self.pila[2]=self.pila[1]
                    self.pila[1]=self.pila[0]
                    self.poner_en_strv(1)
                if self.pila_strv[0].get()[-1]=='e': # si empiezo por e, poner 1e
                    self.pila_strv[0].set('1e')
                else:
                    self.pila_strv[0].set(ch)
                self.mover_pila= True
                self.estoy_poniendo= True

        elif ks in ('Return', 'KP_Enter'): # Return o KP_Enter
            if self.estoy_poniendo:
                try:
                    self.pila[0]= float(self.pila_strv[0].get())
                    self.estoy_poniendo=False
                except:
                    self.flashes('white')
                    return()
            self.pila[3]=self.pila[2]
            self.pila[2]=self.pila[1]
            self.pila[1]=self.pila[0]
            self.poner_en_strv(0)
            self.mover_pila = False
            self.entries_wgt[0].configure(background='white')

        elif ch in '+-*/': # +-*/ binarias aritmeticas
            self.lasti= self.pila[0]
            if self.estoy_poniendo:
                try:
                    self.pila[0]= float(self.pila_strv[0].get()[0:-1])
                    self.estoy_poniendo=False
                    self.lasti= self.pila[0] # lo sobreescribe (mas claro que un else final)
                except:
                    if ch=='-' and self.pila_strv[0].get()[-2]=='e':
                        return() # que deje el -, seguir escribiendo
                    else:
                        self.pila_strv[0].set(self.pila_strv[0].get()[0:-1])
                        self.flashes('white')
                    return()
                
            if ch=='+':
                self.pila[0] += self.pila[1]
            elif ch=='-':
                try:
                    self.pila[0] = self.pila[1] - self.pila[0]
                except ValueError:
                    pass # como caracter para despues de 'e' en 1.22e-7
            elif ch=='*':
                self.pila[0] *= self.pila[1]
            elif ch=='/':
                if self.pila[0] != 0:
                    self.pila[0] = self.pila[1]/self.pila[0]
                else:
                    self.flashes('#D9D9D9')
                    self.pila_strv[0].set('0')
                    self.mover_pila= False
                    #self.entries_wgt[0].configure(background='white')
                    return()
            
            self.pila[1]=self.pila[2]
            self.pila[2]=self.pila[3]
            self.poner_en_strv(0)
            self.mover_pila = True
            self.entries_wgt[0].configure(background='#D9D9D9')
            self.entries_wgt[0].icursor('end')


        elif ks in ('Up','Down'): # manejos de pila
            self.lasti= self.pila[0]
            if self.estoy_poniendo:
                try:
                    self.pila[0]=float(self.pila_strv[0].get()) # flechas no meten caracter
                    self.estoy_poniendo=False
                except:
                    self.flashes('white')  # ('#D9D9D9')
                    return()
                    
            if ks=='Down': # flecha abajo (Down), rotar escala abajo
                a=self.pila[0]
                self.pila[0]=self.pila[1]
                self.pila[1]=self.pila[2]
                self.pila[2]=self.pila[3]
                self.pila[3]=a
            elif ks=='Up': # flecha arriba (Up), rotar hacia arriba
                a=self.pila[3]
                self.pila[3]=self.pila[2]
                self.pila[2]=self.pila[1]
                self.pila[1]=self.pila[0]
                self.pila[0]=a
                
            self.poner_en_strv(0)
            self.mover_pila = True
            self.entries_wgt[0].configure(background='#D9D9D9')
            self.entries_wgt[0].icursor('end')

        elif ch in 'ñ mlLsctSCTi!xrkK' : # unarias (o q no mueven pila)
            self.lasti= self.pila[0]
            if self.estoy_poniendo:
                try:
                    self.pila[0]= float(self.pila_strv[0].get()[0:-1])
                    self.estoy_poniendo=False
                    self.lasti=self.pila[0]
                except:
                    if ch==' ' or ch=='ñ':
                        self.pila_strv[0].set(self.pila_strv[0].get()[0:-1])
                        self.entries_wgt[0].insert('end','-')
                        return() # escribe caracter- y sigue escribiendo
                    else:
                        self.pila_strv[0].set(self.pila_strv[0].get()[0:-1])
                        self.flashes('white')  # ('#D9D9D9')
                    return()
            
            if ch=='m': # x a memoria
                self.mem = self.pila[0]
            elif ch==' ' or ch=='ñ': # cambio de signo
                try:
                    self.pila[0] = -self.pila[0]
                except:
                    self.pila_strv[0].set(self.pila_strv[0].get()[0:-1])
                    self.entries_wgt[0].insert('end','-')
                    return() # again como caracter despues de 'e' en 1.2e-3
                
            elif ch=='l': # log natural
                self.pila[0]=np.log(self.pila[0])
            elif ch=='L': # antilog natural (e**x)
                self.pila[0]=np.exp(self.pila[0])
            elif ch=='s': # seno
                self.pila[0]=np.sin(self.pila[0]*self.Cdeg)
            elif ch=='c': # coseno
                self.pila[0]=np.cos(self.pila[0]*self.Cdeg)
            elif ch=='t': # tangente
                self.pila[0]=np.tan(self.pila[0]*self.Cdeg)
            elif ch=='S': # arco seno
                self.pila[0]=np.arcsin(self.pila[0])/self.Cdeg
            elif ch=='C': # arco coseno
                self.pila[0]=np.arccos(self.pila[0])/self.Cdeg
            elif ch=='T': # arco tangente
                self.pila[0]=np.arctan(self.pila[0])/self.Cdeg
            elif ch=='i': # inverso de x
                if self.pila[0] == 0:
                    self.flashes('#D9D9D9')
                    self.pila_strv[0].set('0')
                    return()
                else:
                    self.pila[0]=1./self.pila[0]
            elif ch=='x':  # intercambiar xy
                self.pila[0], self.pila[1] = self.pila[1], self.pila[0]
            elif ch=='r':  # raiz cuadrada
                self.pila[0] = np.sqrt(self.pila[0])
            elif ch=='!': # factorial; es especial porque no admite complejo & no da nan
                a= self.pila[0]
                if np.iscomplex(a):
                    self.flashes('#D9D9D9')
                    self.pila[0]=self.lasti
                elif  int(a)==a  and  a>=0  and  a<171:
                    self.lasti= self.pila[0]
                    self.pila[0]= float(np.math.factorial(int(self.pila[0]))) 
                                # ln de un entero muy grande falla en numpy --> float
                else:
                    self.flashes('#D9D9D9')
            elif ch=='k': # log 10
                self.pila[0]= np.log10(self.pila[0])
            elif ch=='K': # antilog 10 (10^x)
                self.pila[0]= 10.**(self.pila[0])
            
            
            if np.isnan(self.pila[0]): # sqrt ó log de -, arcsin de >1 etc
                self.flashes('#D9D9D9')
                self.pila[0] = self.lasti
            
            self.poner_en_strv(0)
            self.mover_pila = True
            self.entries_wgt[0].configure(background='#D9D9D9')
            self.entries_wgt[0].icursor('end')
    
        elif ch in 'pjn': # otras binarias 
            self.lasti= self.pila[0]
            
            if self.estoy_poniendo:
                try:
                    self.pila[0]= float(self.pila_strv[0].get()[0:-1])
                    self.estoy_poniendo=False
                    self.lasti= self.pila[0]
                except:
                    self.pila_strv[0].set(self.pila_strv[0].get()[0:-1])
                    self.flashes('white')  # ('#D9D9D9')
                    return()
            if ch=='p': # potenciacion y**x 
                self.pila[0] = self.pila[1]**self.pila[0]
            elif ch=='j': # complejo y+xj
                if np.isreal(self.pila[0]) and np.isreal(self.pila[1]): 
                    self.pila[0]= np.complex(self.pila[1], self.pila[0])
                else:
                    self.flashes('#D9D9D9')
                    self.poner_en_strv(0)
                    return()
            elif ch=='n': # complejo mod=y, arg=x
                if np.isreal(self.pila[0]) and np.isreal(self.pila[1]): 
                    a,b= self.pila[0]*self.Cdeg, self.pila[1]
                    self.pila[0]= np.complex(b*np.cos(a), b*np.sin(a))
                else:
                    self.flashes('#D9D9D9')
                    self.poner_en_strv(0)
                    return()

            self.pila[1]=self.pila[2]
            self.pila[2]=self.pila[3]
            self.poner_en_strv(0)
            self.mover_pila = True
            self.entries_wgt[0].configure(background='#D9D9D9')
            self.entries_wgt[0].icursor('end')

        elif ch in 'PMy': # especial poner pi, traer mem, lasti
            # self.lasti= self.pila[0] para estos no reza lasti

            if self.estoy_poniendo:
                a=self.pila_strv[0].get()
                try:
                    self.pila[0]= float(self.pila_strv[0].get()[0:-1])
                    self.estoy_poniendo=False
                except:
                    self.pila_strv[0].set(self.pila_strv[0].get()[0:-1])
                    self.flashes('white')  # ('#D9D9D9')
                    return()
            self.pila[3] = self.pila[2]
            self.pila[2] = self.pila[1]
            self.pila[1] = self.pila[0]

            if ch=='P': # numero pi
                self.pila[0] = np.pi
            elif ch=='M': # memoria a i
                self.pila[0]= self.mem
            elif ch=='y': # last i
                self.pila[0]= self.lasti

            self.poner_en_strv(0)
            self.mover_pila = True
            self.entries_wgt[0].configure(background='#D9D9D9')
            self.entries_wgt[0].icursor('end')
        
        elif ch=='f': # hacer fraccion, es muy particular
            self.lasti=self.pila[0]
            if self.estoy_poniendo:
                try:
                    self.pila[0]= float(self.pila_strv[0].get()[0:-1])
                    self.estoy_poniendo=False
                except:
                    self.flashes('#D9D9D9')
                    self.poner_en_strv()
                    return()
            if np.isreal(self.pila[0]):
                fr= Fraction(self.pila[0]).limit_denominator(100000)
                self.pila[3]=self.pila[2]
                self.pila[2]=self.pila[1]
                self.pila[1]= fr.numerator
                self.pila[0]= fr.denominator
            else:
                self.flashes('#D9D9D9')

            self.poner_en_strv(0)
            self.mover_pila = True
            self.entries_wgt[0].configure(background='#D9D9D9')
            self.entries_wgt[0].icursor('end')
        
        elif ch in 'JN': # deshacer complejo
        
            if self.estoy_poniendo:
                self.flashes('white')  # ('#D9D9D9')
                self.pila_strv[0].set(self.pila_strv[0].get()[0:-1])
                return()
            elif ch=='J': # complejo --> y=real, x=imag
                # entiende 5+0j como real -> que opere en todo caso, no dara error
                self.lasti= self.pila[0]
                self.pila[3] = self.pila[2]
                self.pila[2] = self.pila[1]
                self.pila[1] = self.pila[0].real
                self.pila[0] = self.pila[0].imag
            elif ch=='N': # complejo --> y=modulo, x=angulo
                if self.pila[0] != 0: # si es real q al menos no sea 0
                    self.lasti= self.pila[0]
                    self.pila[3] = self.pila[2]
                    self.pila[2] = self.pila[1]
                    a,b= self.pila[0].real, self.pila[0].imag
                    self.pila[1]= np.linalg.norm((a,b))
                    self.pila[0]= np.arctan2(b,a)/self.Cdeg
                else:
                    self.flashes('#D9D9D9')

            self.poner_en_strv(0)
            self.mover_pila = True
            self.entries_wgt[0].configure(background='#D9D9D9')
            self.entries_wgt[0].icursor('end')
        
        elif ks=='Escape': # escape, restituir pila[0]
            self.poner_en_strv(0)
            self.mover_pila= True
            self.entries_wgt[0].configure(background='#D9D9D9')
            self.entries_wgt[0].icursor('end')
            self.estoy_poniendo=False
        
        elif ks=='BackSpace': # backspace, dejar actuar si estoy poniendo, poner 0 si no
            if self.estoy_poniendo:
                if not len(self.pila_strv[0].get()):
                    self.pila_strv[0].set('0')
                    self.pila[0]=0
                    self.estoy_poniendo = False
                    self.mover_pila = False # si borro todo que ponga 0 como si <Enter 0>
            else:
                self.pila[0]=0
                self.poner_en_strv(0)
                self.mover_pila= False # no mover pila al seguir escribiendo numero
                self.entries_wgt[0].configure(background='white')
        
        elif ch=='z': # reseteo
            for i in range(4): self.pila[i]=0.
            self.lasti, self.mem = 0., 0.
            self.poner_en_strv(0)
            self.mover_pila=True
            self.entries_wgt[0].configure(background='#D9D9D9')
            self.estoy_poniendo=False

        elif ks in ('Right','Left'): # flechas izda & dcha
            if not self.estoy_poniendo: # si estoy poniendo -> dejarlas actuar
                self.entries_wgt[0].focus()
                self.entries_wgt[0].icursor('end')

        elif ks in ('Tab','Shift_L','Shift_R','Shift', # teclas tab shift
                'Control_L','Control_R','Control','Super_R', #  teclas ctrl, super_R, 
                'Alt_L','ISO_Level3_Shift','Menu', # alt, altgr, menu
                'Meta_R','Meta_L'):  # para mac
            self.entries_wgt[0].focus()
            self.entries_wgt[0].icursor('end') # por si el tab
            
            '''
            elif kc in (113,114): # flechas izda & dcha (inhabilitarlas de facto)
                self.entries_wgt[0].icursor('end')
                
            elif kc in (23,50,62): # teclas tab shift
                self.entries_wgt[0].focus()
                self.entries_wgt[0].icursor('end') # por si el tab

            elif kc in (37,105,108,134,135,64): # teclas ctrl, super_R, alt, altgr, menu
                pass
            '''
        else: # simplemente reponer la pila y resetear estado
            if self.estoy_poniendo:
                self.flashes('white')
                self.pila_strv[0].set(self.pila_strv[0].get()[0:-1])
            else:
                self.flashes('#D9D9D9')
                self.poner_en_strv(0)
                self.mover_pila = True
                self.estoy_poniendo = False
                self.entries_wgt[0].icursor('end')
            

    def salir(self):
    
        self.v0.destroy()
        try: # si es linux que cierre el terminal tambien
            kill(getppid(), signal.SIGHUP)        
        except:
            exit()
        # con extension .pyw no saca terminal.



gui=Gui()



