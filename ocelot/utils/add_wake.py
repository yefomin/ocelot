'''

utilities to add externaly calculated wakes to beam files
Usage:
from command line:
python add_wake.py add           beamfile beamfile_wake
python add_wake.py add_from_file beamfile wakefile       beamfile_wake
python add_wake.py current       beamfile currentfile
from script:
from ocelot.utils.add_wake import add_wake_to_beamf
add_wake_to_beamf(beamf, new_beamf)
'''
#sys.path.append("../../")
from ocelot.adaptors.genesis import *
import cpbd.reswake as w
from copy import deepcopy
#try:
#    import matplotlib.animation as anim
#except:
#    print 'animation not installed'
#import matplotlib.pyplot as plt


def get_current(beamf):
    beam = read_beam_file(beamf)
    beam.columns = ['ZPOS','CURPEAK']
    #beam.I = beam.I[::-1]
    return beam


def get_wake_from_file(wakefile):
    buf = open(wakefile).read().split('\n')
    wake = []
    for l in buf:
        d = l.split()
        if len(d)>1:
            wake.append(float(d[1]))
    return wake


def add_wake_to_beam(beam):
    # beam = read_beam_file(beamf)
    # s, bunch, wake = w.xfel_pipe_wake(s=beam.z, current=beam.I[::-1])
    s, bunch, wake = w.xfel_pipe_wake(s=beam.z, current=beam.I)
    print ('read ', len(wake), ' slice values')
    beam1 = deepcopy(beam)
    beam1.eloss = wake[::-1]
    # f=open(new_beamf,'w')
    # f.write(beam_file_str(beam))
    # f.close()
    return beam1

if len(sys.argv)>3:
    command = sys.argv[1]
    beamf = sys.argv[2]    
    outf = sys.argv[3]
else:
    command = ''
    #beamf = '/home/iagapov/tmp/run_2/tmp.beam'
    #command = 'current'
    #outf = 'tmp.beam'
 

if command == 'current':
        beam = read_beam_file(beamf)
        beam.columns = ['ZPOS','CURPEAK']
        beam.I = beam.I[::-1]
        f=open(outf,'w')
        f.write(beam_file_str(beam))
        f.close()
        #print beam_file_str(beam)

if command == 'add_from_file':

    if len(sys.argv)>2:
        wakef = sys.argv[3]
        outf = sys.argv[4]    
    else:
        beamf = '/home/iagapov/tmp/run_2/tmp.beam'
        command = 'current'
   
    wake = get_wake_from_file(wakef)

    beam = read_beam_file(beamf)
    #s, bunch, wake = w.xfel_pipe_wake(s=array(beam.z), current=array(beam.I))
    print ('read ', len(wake), ' slice values')
    beam.eloss = wake[::-1]
    
    f=open(outf,'w')
    f.write(beam_file_str(beam))
    f.close()

    beam = read_beam_file(beamf)

if command == "add":
    #if len(sys.argv)>2:
    #    #wakef = sys.argv[3]
    #    outf = sys.argv[4]
    #else:
    #    beamf = '/home/iagapov/tmp/run_2/tmp.beam'
    #    command = 'current'

    #wake = get_wake_from_file(wakef)
    beam = read_beam_file(beamf)
    beam1 = add_wake_to_beam(beam)
    write_beam_file(outf, beam1)


"""
if __name__ == "__main__":
    import ocelot.utils.reswake as w
    from numpy import array
    from matplotlib.pyplot import *
    #beamf = "../../desy/xfel/beams/beam_1nC.txt"
    #beamf = "../../desy/xfel/beams/beam_0.02nC.txt"
    #beamf = "../../desy/xfel/beams/beam_0.25nC.txt"
    beamf = "../test/100pC_skew.txt"
    beamf_new = "../test/100pC_skew_wake.txt"

    beam = read_beam_file(beamf)
    print (beam.z, beam.I)
    #I = array(beam.I[::-1])
    #s = -array(beam.z[::-1])
    s, bunch, wake = w.xfel_pipe_wake(s=array(beam.z), current=array(beam.I))
    beam.eloss = wake[::-1]
    fig, ax1 = subplots()
    ax1.plot(beam.z, beam.I, "b")
    ax1.grid(True)
    ax1.set_ylabel('I[A]', color='b')
    ax2 = ax1.twinx()
    ax2.plot(beam.z, beam.eloss/1000 , "r")
    ax2.set_ylabel('wake, [kV/m]', color='r')
    show()
    add_wake_to_beamf(beamf, beamf_new)
    beam = read_beam_file(beamf_new)

    fig, ax1 = subplots()
    ax1.plot(beam.z, beam.I, "b")
    ax1.set_ylabel('I[A]', color='b')
    ax2 = ax1.twinx()
    ax2.plot(beam.z, beam.eloss/1000 , "r")
    ax2.set_ylabel('wake, [kV/m]', color='r')
    show()
"""