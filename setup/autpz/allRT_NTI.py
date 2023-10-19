import paramiko
import getpass
import time

#Configuração inicial do roteador RT_NTI
# Requisito 1: Verifique se o ssh está habilitado no roteador RT_NTI
# Requisito 2: Verifique se a senha do modo privilegiado (thiago) está configurada
# Requisito 3: Verifique se no roteador RT_NTI as interfaces e0/1 e e0/2 estão configuradas com Ip 172.16.6.1 e 172.16.7.1, respectivamente.
# Requisito 4: Se certifique que existe comunicação entre a vm DebianMGMT e o roteador RT_NTI, em seguida execute o script com o comando python3 allRT_NTI.py

# Endereço IP do roteador Cisco e credenciais de autenticação
host = "172.16.6.1"
user = input("Enter your remote account: ") # thiago
password = getpass.getpass("Enter your password: ") # thiago

comandos = [
    "en",
    "thiago",
    "conf t",
    "hostname RT_NTI",
    "int e0/0",
    "ip add 172.16.5.2 255.255.255.0",
    "no shut",
    "exit",
    "int e0/1",
    "ip add 172.16.6.1 255.255.255.0",
    "no shut",
    "exit",
    "int e0/2",
    "ip add 172.16.7.1 255.255.255.0",
    "no shut",
    "exit",
    "int e0/1.10",
    "encapsulation dot1q 10",
    "ip add 172.16.10.1 255.255.255.240",
    "int e0/1.20",
    "encapsulation dot1q 20",
    "ip add 172.16.20.1 255.255.255.248",
    "int e0/1.30",
    "encapsulation dot1q 30",
    "ip add 172.16.30.1 255.255.255.192",
    "int e0/1.40",
    "encapsulation dot1q 40",
    "ip add 172.16.40.1 255.255.255.240",
    "int e0/1.50",
    "encapsulation dot1q 50",
    "ip add 172.16.50.1 255.255.255.248",
    "int e0/1.60",
    "encapsulation dot1q 60",
    "ip add 172.16.60.1 255.255.255.248",
    "int e0/1.70",
    "encapsulation dot1q 70",
    "ip add 172.16.70.1 255.255.255.0",
    "exit",
    "ip dhcp pool Secretaria",
    "network 172.16.10.0 255.255.255.240",
    "default-router 172.16.10.1",
    "exit",
    "ip dhcp pool Corredor",
    "network 172.16.20.0 255.255.255.248",
    "default-router 172.16.20.1",
    "exit",
    "ip dhcp pool LI",
    "network 172.16.30.0 255.255.255.192",
    "default-router 172.16.30.1",
    "exit",
    "ip dhcp pool SP",
    "network 172.16.40.0 255.255.255.240",
    "default-router 172.16.40.1",
    "exit",
    "ip dhcp pool CP",
    "network 172.16.50.0 255.255.255.248",
    "default-router 172.16.50.1",
    "exit",
    "ip dhcp pool Diretoria",
    "network 172.16.60.0 255.255.255.248",
    "default-router 172.16.60.1",
    "exit",
    "access-list 100 deny ip 172.16.10.0 0.0.0.255 172.16.20.0 0.0.0.255",
    "access-list 100 deny ip 172.16.10.0 0.0.0.255 172.16.30.0 0.0.0.255",
    "access-list 100 deny ip 172.16.10.0 0.0.0.255 172.16.40.0 0.0.0.255",
    "access-list 100 deny ip 172.16.10.0 0.0.0.255 172.16.50.0 0.0.0.255",
    "access-list 100 deny ip 172.16.10.0 0.0.0.255 172.16.60.0 0.0.0.255",
    "access-list 100 deny ip 172.16.20.0 0.0.0.255 172.16.30.0 0.0.0.255",
    "access-list 100 deny ip 172.16.30.0 0.0.0.255 172.16.40.0 0.0.0.255",
    "access-list 100 deny ip 172.16.30.0 0.0.0.255 172.16.50.0 0.0.0.255",
    "access-list 100 deny ip 172.16.30.0 0.0.0.255 172.16.60.0 0.0.0.255",
    "access-list 100 deny ip 172.16.40.0 0.0.0.255 172.16.50.0 0.0.0.255",
    "access-list 100 deny ip 172.16.40.0 0.0.0.255 172.16.60.0 0.0.0.255",
    "access-list 100 deny ip 172.16.50.0 0.0.0.255 172.16.60.0 0.0.0.255",
    "access-list 100 permit ip any any",
    "int e0/1.10",
    "ip access-group 100 out",
    "int e0/1.20",
    "ip access-group 100 out",
    "int e0/1.30",
    "ip access-group 100 out",
    "int e0/1.40",
    "ip access-group 100 out",
    "int e0/1.50",
    "ip access-group 100 out",
    "int e0/1.60",
    "ip access-group 100 out",
    "exit",
    "ip route 0.0.0.0 0.0.0.0 172.16.5.1",
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