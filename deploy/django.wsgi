import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

VENV_ROOT='/var/www/jagom/pinax_venv'
PYLIBDIR=os.path.join(VENV_ROOT, 'lib','python2.5','site-packages')

#FIXME: os.path.join 

sys.path = ['']
sys.path.append('/var/www/jagom/JAGOM/')

def append_egg(arg, dirname, fnames):

	for i,fname in enumerate(fnames):
		if fname.endswith(".egg"):
			sys.path.append(os.path.join(dirname,fname))
		del fnames[i]

os.path.walk(PYLIBDIR, append_egg, None)

sys.path += [VENV_ROOT + '/lib/python2.5', VENV_ROOT + '/lib/python2.5/plat-linux2', VENV_ROOT + '/lib/python2.5/lib-tk', VENV_ROOT + '/lib/python2.5/lib-dynload', '/usr/lib/python2.5', '/usr/lib/python2.5/lib-tk', VENV_ROOT + '/lib/python2.5/site-packages', '/usr/local/lib/python2.5/site-packages', '/usr/lib/python2.5/site-packages', '/var/lib/python-support/python2.5']


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
