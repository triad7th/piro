import mido
import time
from clock import PrClock, PrHelper

mido.set_backend('mido.backends.pygame')

print(mido.get_output_names())
mid = mido.MidiFile('.\\source\\mido test\\midi\\furelise.mid')
# for i, track in enumerate(mid.tracks):
#     print('Track {}: {}'.format(i, track.name))
#     for msg in track:
#         print(msg)

port = mido.open_output('Pro40 MIDI')
print(mido.backend)
for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track[:100]:
        print(msg.bytes(), msg.time)



# for msg in mid.play():
#     print(msg)
#     port.send(msg)


for msg in mid:
    if msg.is_meta and msg.type=='set_tempo':
        print("tempo is :",msg.tempo)
        break

delta_list = [0.0, 0.0009999275207519531, 0.004000663757324219, 0.0040013790130615234, 0.022017717361450195, 0.47411036491394043, 0.014003753662109375, 0.022005796432495117, 0.020005226135253906, 0.0030007362365722656, 0.01900506019592285, 0.09902548789978027, 0.007001638412475586, 0.019005298614501953, 0.003000974655151367, 0.08803439140319824, 0.0339968204498291, 0.18704843521118164, 0.004000663757324219, 0.007002115249633789, 0.00400090217590332, 0.003000974655151367, 0.03701162338256836, 0.10202550888061523, 0.37509727478027344, 0.011002779006958008, 0.0070018768310546875, 0.00400090217590332, 0.0030002593994140625, 0.025006532669067383, 0.01800394058227539, 0.12503290176391602, 0.0, 0.03200817108154297, 0.07001829147338867, 0.007001399993896484, 0.2060534954071045, 0.04001021385192871, 0.0, 0.006000995635986328, 0.0, 0.003000020980834961, 0.04401135444641113, 0.13603544235229492, 0.3530912399291992, 0.029007911682128906, 0.018004417419433594, 0.5151333808898926, 0.015003681182861328, 0.0070018768310546875, 0.04001045227050781, 0.1140294075012207, 0.13603520393371582, 0.026006698608398438, 0.011002540588378906, 0.0070018768310546875, 0.03000807762145996, 0.0290071964263916, 0.008002042770385742, 0.058014869689941406, 0.01500391960144043, 0.02200627326965332, 0.12004280090332031, 0.01900482177734375, 0.003989219665527344, 0.0030002593994140625, 0.008002519607543945, 0.1320340633392334, 0.0070188045501708984, 0.0, 0.0070018768310546875, 0.06099677085876465, 0.06301665306091309, 0.03300809860229492, 0.012002944946289062, 0.0040013790130615234, 0.0, 0.006000995635986328, 0.09202408790588379, 0.01100301742553711, 0.07401895523071289, 0.03700971603393555, 0.08002591133117676, 0.0, 0.006001949310302734, 0.0, 0.03200364112854004, 0.04000997543334961, 0.05903148651123047, 0.010998725891113281, 0.1840355396270752, 0.0, 0.005995273590087891, 0.0, 0.024006366729736328, 0.040010690689086914, 0.044011592864990234, 0.17304468154907227, 0.05000734329223633, 0.0, 0.0, 0.01300358772277832, 0.044011592864990234, 0.14503765106201172, 0.1250324249267578, 0.004000663757324219, 0.003000974655151367, 0.0, 0.3080770969390869, 0.00400090217590332, 0.0030007362365722656, 0.006001472473144531, 0.0, 0.006001472473144531, 0.022005796432495117, 0.05901503562927246, 0.00800180435180664, 0.01500391960144043, 0.12504220008850098, 0.1060178279876709, 0.015003681182861328, 0.0070040225982666016, 0.0, 0.043010711669921875, 0.15504026412963867, 0.10602760314941406, 0.12903308868408203, 0.03700971603393555, 0.24406123161315918, 0.004017353057861328, 0.020004987716674805, 0.10704374313354492, 0.02599048614501953, 0.018016815185546875, 0.12902140617370605, 0.0, 0.05101299285888672, 0.0, 0.02799844741821289, 0.12504863739013672, 0.2570500373840332, 0.019005298614501953, 0.026007652282714844, 0.047028541564941406, 0.2720530033111572, 0.07001781463623047, 0.07403182983398438, 0.2080237865447998, 0.01500391960144043, 0.011002779006958008, 0.007001399993896484, 0.01100301742553711, 0.14603734016418457, 0.382098913192749, 0.0, 0.003000497817993164, 0.0070018768310546875, 0.00800180435180664, 0.014003992080688477, 0.11102867126464844, 0.003017425537109375, 0.009988069534301758, 0.0070018768310546875, 0.09202384948730469, 0.0, 0.2530653476715088, 0.0, 0.002000093460083008, 0.0, 0.009994029998779297, 0.015003681182861328, 0.11804318428039551, 0.39709043502807617, 0.007001638412475586, 0.03000783920288086, 
0.011002779006958008, 0.003000974655151367, 0.03300833702087402, 0.011002779006958008, 0.0980372428894043, 0.010990619659423828, 0.0, 0.07601809501647949, 0.018004417419433594, 0.1140296459197998]

prClock = PrClock()
prHelper = PrHelper()

idx = 0


for msg in mid:    
    prClock.set_timer(0)
    prClock.set_timer(1)

    if not msg.is_meta:
        #time.sleep(delta_list[idx])
        time.sleep(msg.time)
        idx += 1
    else:
        time.sleep(msg.time)

    delta = prClock.elapsed(1)
    if not msg.is_meta:
        prHelper.msg_print(prClock.elapsed(0), prClock.elapsed(1), msg)
        port.send(msg)
