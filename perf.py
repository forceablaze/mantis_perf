from prompt_toolkit import prompt
from optparse import OptionParser

import functools
print_flush = functools.partial(print, flush=True)


from mantis_api_types import print_types as mantis_print_types
from mantis_api_types import types as mantis_types

from mantis_api_types import *

ALL_PERF_TYPES = {**mantis_types}

def print_types():
    allTypes = list(ALL_PERF_TYPES.keys())
    i = 0
    for t in allTypes:
        print_flush("{}; {}\t\t{}".format(i, t, ALL_PERF_TYPES[t]))
        i += 1

def perf(types):
    #mantis_server = prompt('Please input mantis server.')

    mantis_login(options.server, options.username, options.password)

    allTypes = list(ALL_PERF_TYPES.keys())
    for t in types:
        index = int(t)
        typeName = allTypes[index]
        print_flush("\nperf type: {}, {}".format(typeName, ALL_PERF_TYPES[typeName]['name']))
        perf_func_name = ALL_PERF_TYPES[typeName]['name'] + '_perf'

        total_elapsed = 0
        for i in range(0, options.count):
            elapsed = globals()[perf_func_name]()
            total_elapsed += elapsed
        print_flush('{}: {}s'.format(typeName, total_elapsed / options.count))

if __name__ == '__main__':

    parser = OptionParser()  

    parser.add_option("-L", "--list", default = False,
        action = "store_true", dest = "list",
        help = "list test type")

    parser.add_option("-x", "--execute", default = False,
        action = "store_true", dest = "perf",
        help = "do perf")

    parser.add_option("-t", "--type", default = None,
        action = "append", dest = "types",
        help = "specified type")

    parser.add_option("-c", "--count", type="int", default = 3,
        action = "store", dest = "count",
        help = "test count")

    parser.add_option("-s", "--server", default = None,
        action = "store", dest = "server",
        help = "Mantis SOAP server")

    parser.add_option("-u", "--username", default = None,
        action = "store", dest = "username",
        help = "Mantis username")

    parser.add_option("-p", "--password", default = None,
        action = "store", dest = "password",
        help = "Mantis password")

    (options, args) = parser.parse_args()  
    if options.list == True:
        print_types()

    if options.perf == True:
        perf(options.types)
