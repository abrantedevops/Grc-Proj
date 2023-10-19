import paramiko
import getpass
import time

#Configuração inicial do roteador R3
# Requisito 1: Verifique se o ssh está habilitado no roteador R3
# Requisito 2: Verifique se a senha do modo privilegiado (thiago) está configurada
# Requisito 3: Verifique se no roteador R3 a interface e0/1 está configuradas com Ip 10.0.0.33 e no debianMGMT o Ip 172.16.7.2.
# Requisito 4: Se certifique que existe comunicação entre a vm DebianMGMT e o roteador R3, em seguida execute o script com o comando python3 r3.py


# Endereço IP do roteador Cisco e credenciais de autenticação
host = "10.0.0.33"
user = input("Enter your remote account: ") # thiago
password = getpass.getpass("Enter your password: ") # thiago

comandos = [
    "en",
    "thiago",
    "conf t",
    "hostname R3",
    "int e0/0",
    "ip add 10.0.0.29 255.255.255.252",
    "no shut",
    "exit",
    "int e0/1",
    "ip add 10.0.0.33 255.255.255.252",
    "no shut",
    "exit",
    "int Loopback0",
    "ip add 3.3.3.3 255.255.255.255",
    "no shut",
    "exit",
    "router ospf 10",
    "network 0.0.0.0 255.255.255.255 area 0",
    "exit",
    "ip route 0.0.0.0 0.0.0.0 10.0.0.30",
    "do wr",
    "end"
]

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(host, username=user, password=password, look_for_keys=False)

    shell = ssh.invoke_shell()

    for comando in comandos:
        shell.send(comando + "\n")
        time.sleep(0.5)
        output = shell.recv(65535).decode('utf-8')
        print(output)

except paramiko.AuthenticationException:
    print("Authentication error. Please check your credentials.")
except paramiko.SSHException as e:
    print("Error establishing SSH connection:", str(e))
finally:
    ssh.close()