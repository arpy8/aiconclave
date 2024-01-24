import os
import tqdm
import time
import random
import subprocess
from termcolor import colored

from aiconclave.constants import path_converter, ART


def fake_loading():
    for i in tqdm.tqdm(range(10), desc="Initializing boot sequence..."):
        time.sleep(random.uniform(0.08, 0.12))

    print(colored("Boot sequence initialized.", "green"))
    print("Loading modules...")
    
    time.sleep(1)
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(chr(27)+'[2j')
    print(colored(ART, "green"))
    print(colored("App started...", "green"))

def run_streamlit_app():
    exe_path = path_converter('streamlit_app.py')
    command = ['streamlit', 'run' , exe_path, '--server.port', '8205']
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    return result.stdout

def main():
    try:
        fake_loading()
        run_streamlit_app() 
        
    except KeyboardInterrupt:
        print(colored("Bye Bye 🤫🧏...", "red"))
        exit()
    except Exception as e:
        print(e)
        print(colored("Bye Bye 🤫🧏...", "red"))
        exit()
        
if __name__ == '__main__':
    main()