import subprocess
import os

def run_file():

    compile_status = subprocess.run(
        args=['javac', os.path.join(filepath, filename)], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    print(compile_status, compile_status.stdout, compile_status.stdout.decode('utf-8'), sep='\n')

    if compile_status.stderr.decode('utf-8'):
        print('VLVLV')
    else:
        print('okoko')


filepath = '/Users/Kleinman/Desktop'
filename = 'Lab0.java'


run_file()