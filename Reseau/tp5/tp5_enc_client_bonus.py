import socket
import re
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 13337))

# Récupération d'une string utilisateur
msg = input("Calcul à envoyer: ")

pattern = r'(-?\d+|\s*([-+*/%]||\*\*)\s*-?\d+)'

matches = re.findall(pattern, msg)  

payload = b""

for match in matches:
    # Extract numbers from each match and convert them to integers
    print(f"match found : {match}")
    i=0
    result_num = 0
    result_ope = ""
    for result in match:
      print(f"result num : {result}")
      if not result=="":

        try:
            operator = re.search(r'[-+*/%]||\*\*', match[1])
            if len(operator.group(i)) > 1:
                result_ope = num.group(i)
                print(f"(1)match found ope {operator.group(i)}")
                break
        except Exception as e:
          print(f"error matching operator{e}")
        
        if result_ope == "":
          try:
            num = re.search(r'\d+', result)
            if len(num.group(i)) > 1:
              result_num = int(num.group(i))
              print(f"(1)match found num {num.group(i)}")
          except Exception as e:
            print(f"error matching num {e}")
        else:
           print("sign already found")
           
        i+=1

    if result_ope != "":
        
        print(f"(2)match found ope :  {result_ope}")

        encoded_operator = result_ope.encode('utf-8')
        encoded_operator_len = len(encoded_operator)
        encoded_operator_header = encoded_operator_len.to_bytes(4, byteorder='big')
        payload += encoded_operator_header + encoded_operator
        print(f"{result_ope} added to payload : {payload}")


    elif result_num != 0:
        
        print(f"(2)match found num :  {result_num}")

        # Vérifiez si les nombres sont dans la plage
        if -4294967295 <= result_num <= 4294967295:

          # on encode le message explicitement en UTF-8 pour récup un tableau de bytes
          encoded_num = result_num.to_bytes((result_num.bit_length()+7)//8, byteorder='big')

          # on calcule sa taille, en nombre d'octets
          encoded_num_len = len(encoded_num)
          
          # on encode ce nombre d'octets sur une taille fixe de 4 octets
          encoded_num_header = encoded_num_len.to_bytes(4, byteorder='big')

          payload += encoded_num_header + encoded_num
          print(f"{result_num} added to payload : {payload}")
        else:
           raise ValueError(
          "l'opération autorisée n'accepte que les nombres entiers compris entre -4294967295 et +4294967295"
          )
    else:
      raise ValueError(
          "l'opération autorisée n'accepte que les signes suivants (-,+,*) et des nombres entiers compris entre -4294967295 et +4294967295"
      )
    
encoded_endmessage = "hehe".encode('utf-8')
encoded_endmessage_len = len(encoded_endmessage)
encoded_endmessage_header = encoded_endmessage_len.to_bytes(4, byteorder='big')

# on peut concaténer ce header avec le message, avant d'envoyer sur le réseau
payload += encoded_endmessage_header + encoded_endmessage
# on peut envoyer ça sur le réseau
s.send(payload)


# Réception et affichage du résultat
s_data = s.recv(1024)
result = int.from_bytes(s_data, byteorder='big')
print(f"résultat : {result}")
s.close()
sys.exit(0)
