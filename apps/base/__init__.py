from django.conf import settings
import logging, os, subprocess, sys

env = os.environ
log = logging.getLogger('JAGOM')

encoding = "latin-1"

def values_list(qs, par):
	return map(lambda x : x[par], qs.values(par))


def execute_and_log(cmd_args):
    env['JAGOM_HOME'] = settings.PROJECT_ROOT
    env['PYTHONPATH'] = ':'.join(sys.path)
    env['PATH'] += ":%s" % os.path.join(settings.PROJECT_ROOT, 'bin')
    log.debug("Executing: %s" % " ".join(map(lambda x : x.decode(encoding), cmd_args)))
    p = subprocess.Popen(cmd_args, 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env
    )
    stdout, stderr = p.communicate()
    log.debug("stdout: %s" % stdout)
    log.debug("stderr: %s" % stderr)

def init_logger():
    if settings.DEBUG:
        handler = logging.StreamHandler()
        handler.setFormatter( logging.Formatter('%(asctime)s %(levelname)s %(message)s') )
        log.addHandler(handler)
        log.setLevel(logging.DEBUG)
        log.debug("Starting logger...")

init_logger()
