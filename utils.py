import os 
import subprocess
def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        


def run_cmd(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
    except Exception as e:
        return str(e)

        print(output.stderr)

