import imaplib
import email
import re

server, host_name, host_password, mail_box = "imap.gmail.com", "d.emanu.moli@gmail.com", "homero1000", "INBOX"


mail = imaplib.IMAP4_SSL(server)
mail.login(host_name, host_password)
mail.select(mail_box)

file = open("import_data.txt","r")
datos = file.readline().split()
reg = datos[0]
date = datos[1]
correo = datos[2]
file.close()

print ("\nExpresión Regular: ", reg)
print ("Email emisor     : ", correo)
print ("Fecha            : ", date)

print("\n")
print("==============================================SIN FILTRO DE FECHA============================================================")
print("\n")


typ, data  = mail.search(None,'FROM "noreply@blizzard.com"')

lista = []

for num in data[0].split():
    typ, data = mail.fetch(num, '(BODY[HEADER.FIELDS (MESSAGE-ID)])')
    msg_str = email.message_from_string(data[0][1].decode())
    message_id = msg_str.get('Message-ID')
    lista.append(message_id)

count = 0

for element in lista:
    z = re.match(reg , element)
    
    if z:
        count+=1

print('Total de mensajes obtenidos desde "noreply@blizzard.com": ', len(lista),'\nMessage-ID que hicieron match: ',count)

print("\n")
print("==============================================CON FILTRO DE FECHA============================================================")
print("\n")

typ,data = mail.search(None, 'FROM "'+correo+'" SINCE '+date)
lista1 = []

for num in data[0].split():
    typ, data = mail.fetch(num, '(BODY[HEADER.FIELDS (MESSAGE-ID)])')
    msg_str = email.message_from_string(data[0][1].decode())
    message_id = msg_str.get('Message-ID')
    lista1.append(message_id)

print("Total de Message-ID obtenidos desde el "+date+": ", len(lista1),"\n")
count = 0

for element in lista1:
    z = re.match(reg , element)
    
    if not z:
        print("Correo falso detectado:\n", element,"\n")

    else:
        count+=1


print('Total de correos que hicieron match con la expresión regular: ', count)

