#!/usr/bin/python3

import socket
import sys
from IPy import IP
import os
import openai_secret_manager
import openai
import re
import pyfiglet


ascii_banner = pyfiglet.figlet_format("ScVploit")
print("\033[34m" + ascii_banner + "\033[0m")
print("---------------------------------------------By Josh")


def get_exploits(service_name):
    openai.api_key = openai_secret_manager.get_secret("openai")["api_key"]
    model_engine = "text-davinci-002"
    prompt = (f"List of exploits for {service_name}")
    response = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=1024, n=1, stop=None, temperature=0.5)
    return response.choices[0].text.strip()


def scan_port(ip_address, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)
        s.connect((ip_address, port))
        service_name = socket.getservbyport(port)
        print(f"[+] Port {port} is open. Service: {service_name}")
        os.system(f"nmap -sV -p{port} {ip_address}")
        exploits = get_exploits(service_name)
        if exploits:
            print(f"Exploits for {service_name}: {exploits}")
    except KeyboardInterrupt:
        print("\nScanning interrupted")
        raise
    except:
        print(f"[-] Port {port} is closed.")

def main():
    while True:
        try:
            print("Select an option:\n[1] Scan ports of an IP address\n[0] Exit")
            option = input("> ")
            if option == "1":
                target = input("Enter the target IP address: ")
                try:
                    IP(target)
                except ValueError:
                    print("Invalid IP address or domain name.")
                    continue

                print(f"Scanning ports on {target}...\n")
                ports = range(1, 81)
                for port in ports:
                    try:
                        scan_port(target, port)
                    except KeyboardInterrupt:
                        print("\nScanning interrupted.")
                        break
            elif option == "0":
                print("Exiting...")
                break
            else:
                print("Invalid option.")
        except KeyboardInterrupt:
            print("\nProgram terminated with Ctrl+C")
            break


if __name__ == '__main__':
    main()
