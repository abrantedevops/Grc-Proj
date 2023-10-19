import paramiko
import getpass
import time

#Configuração inicial do roteador R2
# Requisito 1: Verifique se o ssh está habilitado no roteador R2
# Requisito 2: Verifique se a senha do modo privilegiado (thiago) está configurada
# Requisito 3: Verifique se no roteador R2 a interface e0/0 está configuradas com Ip 10.0.0.18 e no debianMGMT o Ip 172.16.7.2.
# Requisito 4: Se certifique que existe comunicação entre a vm DebianMGMT e o roteador R2, em seguida execute o script com o comando python3 r2.py

# ATENÇÃO: A rede utilizada para o acesso do projeto à internet foi a 192.168.0.0/24 na interface e0/2 do roteador R2. Faça o ajuste necessário conforme a sua rede. 

# Endereço IP do roteador Cisco e credenciais de autenticação
host = "10.0.0.18"
user = input("Enter your remote account: ") # thiago
password = getpass.getpass("Enter your password: ") # thiago

comandos = [
    "en",
    "thiago",
    "conf t",
    "hostname R2",
    "int e0/0",
    "ip add 10.0.0.18 255.255.255.252",
    "no shut",
    "exit",
    "int e0/1",
    "ip add 10.0.0.30 255.255.255.252",
    "no shut",
    "exit",
    "int e0/2",
    "ip add 192.168.0.2 255.255.255.0",
    "no shut",
    "exit",
    "int Loopback0",
    "ip add 2.2.2.2 255.255.255.255",
    "no shut",
    "exit",
    "router ospf 10",
    "network 0.0.0.0 255.255.255.255 area 0",
    "exit",
    "ip route 0.0.0.0 0.0.0.0 192.168.0.1",
    "int e0/0",
    "ip nat inside",
    "exit",
    "int e0/1",
    "ip nat inside",
    "exit",
    "int e0/2",
    "ip nat outside",
    "exit",
    "ip nat inside source static 10.0.0.13 192.168.0.2",
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