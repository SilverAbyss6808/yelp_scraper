import sys
import subprocess
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
print('Success.')