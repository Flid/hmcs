import sys
from os import listdir

from hmcs.app import HMCSApp

print('AAAAAAAAAAAAAAAAA', sys.path)
print('BBBBBB', list(listdir('/data/user/0/org.test.hmcs/files/app/lib/python2.7/lib-dynload')))


app = HMCSApp()
app.run()
