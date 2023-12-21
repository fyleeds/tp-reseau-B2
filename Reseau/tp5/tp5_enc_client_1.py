import socket
import re
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.1.2.12', 13337))

# Récupération d'une string utilisateur
msg = input("Calcul à envoyer: ")

pattern = r'^(-?\d{1,10})\s*([+*-])\s*(-?\d{1,10})$'

match = re.match(pattern, msg)

if match:
  num1, operator, num2 = match.groups()
  num1, num2 = int(num1), int(num2)

  # Vérifiez si les nombres sont dans la plage
  if -4294967295 <= num1 <= 4294967295 and -4294967295 <= num2 <= 4294967295:

    # on encode le message explicitement en UTF-8 pour récup un tableau de bytes
    encoded_num1 = str(num1).encode('utf-8')
    encoded_operator = operator.encode('utf-8')
    encoded_num2 = str(num2).encode('utf-8')
    encoded_endmessage = "hehe".encode('utf-8')

    # on calcule sa taille, en nombre d'octets
    encoded_num1_len = len(encoded_num1)
    encoded_operator_len = len(encoded_operator)
    encoded_num2_len = len(encoded_num2)
    encoded_endmessage_len = len(encoded_endmessage)

    # on encode ce nombre d'octets sur une taille fixe de 4 octets
    encoded_num1_header = encoded_num1_len.to_bytes(4, byteorder='big')
    encoded_operator_header = encoded_operator_len.to_bytes(4, byteorder='big')
    encoded_num2_header = encoded_num2_len.to_bytes(4, byteorder='big')
    encoded_endmessage_header = encoded_endmessage_len.to_bytes(4, byteorder='big')

    # on peut concaténer ce header avec le message, avant d'envoyer sur le réseau
    payload = encoded_num1_header + encoded_num1 + encoded_operator_header + encoded_operator + encoded_num2_header + encoded_num2 + encoded_endmessage_header + encoded_endmessage

    # on peut envoyer ça sur le réseau
    s.send(payload)

  else:
    raise ValueError(
        "l'opération autorisée n'accepte que des nombres entiers compris entre -4294967295 et +4294967295"
    )
else:
  raise ValueError(
      "l'opération autorisée n'accepte que les signes suivants (-,+,*) et des nombres entiers compris entre -4294967295 et +4294967295"
  )

# Réception et affichage du résultat
s_data = s.recv(1024)
print(f"résultat : {s_data.decode()}")
s.close()
sys.exit(0)
