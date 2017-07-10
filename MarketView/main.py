import os, subprocess, time
from threading import Thread

# the server and the application need to run on different threads
def process_runner(process):
    if process['type'] == 'website_app':
        subprocess.run(['python', process['file'], 'runserver'], shell=True)
    else:
        subprocess.run(['python', process['file']] , shell=True)

if __name__ == '__main__':
    root_path = os.path.dirname(os.path.abspath(__file__))
    files = [{'file': root_path + '/website_app/manage.py', 'type': 'website_app'}, {'file': root_path + '/client_app/marketview.py', 'type': 'client_app'}]
    for i in files:
        t = Thread(target=process_runner, args=(i,))
        t.start()