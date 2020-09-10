# odbElementConnectivity.py
# Script to extract node and element information.
#
# Command line argument is the path to the output
# database.
#
# For each node of each part instance:
#     Print the node label and the nodal coordinates.
#
# For each element of each part instance:
#     Print the element label, the element type, the
#     number of nodes, and the element connectivity.
from odbAccess import *
import sys
# Check that an output database was specified.
if len(sys.argv) != 2:
    print 'Error: you must supply the name of an odb on the common line'
    sys.exit(1)
# Get the command line argument
odbPath = sys.argv[1]
odb = openOdb(path=odbPath)
assembly = odb.rootAssembly
print 'Model data for ODB: ', odbPath
numNodes = numElements = 0
for name, instance in assembly.instances.items():
    n = len(instance.nodes)
    print 'Number of nodes of instance %s: %d' % (name, n)
    numNodes = numNodes + n

    print
    print 'NODAL COORDINATES'

    # For each node of each part instance
    # print the node label and the nodal coordinates.
    # Three-dimensional parts include X-, Y-, and Z-coordinates.
    # Two-dimensional parts include X- and Y-coordinates.

    if instance.embeddedSpace == THREE_D:
        print '    X         Y         Z'
        for node in instance.nodes:
            print node.coordinates
    else:
        print '    X         Y'
        for node in instance.nodes:
            print node.coordinates
    # For each element of each part instance
    # print the element label, the element type, the
    # number of nodes, and the element connectivity.

    n = len(instance.elements)
    print
    'Number of elements of instance ', name, ': ', n
    numElements = numElements + n

    print 'ELEMENT CONNECTIVITY'
    print ' Number  Type    Connectivity'
    for element in instance.elements:
        print '%5d %8s' % (element.label, element.type),
        for nodeNum in element.connectivity:
            print '%4d' % nodeNum,
        print

print
print 'Number of instances: ', len(assembly.instances)
print 'Total number of elements: ', numElements
print 'Total number of nodes: ', numNodes