class PrEnv():
    """Environment Variables"""

    # Number of octaves which will be drawn in the piano / roll
    MAX_OCTAVES = 11

    # Pixel Per Quarter Note(PIPQN) for the initial zoom_to
    PIPQN = 200

    # Color Pallette - Piano
    PNO_IVORY_COLOR = [1, 1, 1, 1]
    PNO_EBONY_COLOR = [0, 0, 0, 1]
    PNO_PRESSED_COLOR = [1, 0, 0, 1]
    @staticmethod
    def PNO_KEYMAP():
        """ returns drawing order of each note 
            ex) PNO_KEYMAP()[3] => returns the drawing order of D#0
        """
        # set reverse keymap
        rev_keymap = []
        for octave in range(PrEnv.MAX_OCTAVES):
            for ivory in [0, 2, 4, 5, 7, 9, 11]:
                rev_keymap.append(octave*12+ivory)
        for octave in range(PrEnv.MAX_OCTAVES):
            for ebony in [1, 3, 6, 8, 10]:
                rev_keymap.append(octave*12+ebony)
        
        # reverse it to set keymap
        keymap = []
        for idx in range(len(rev_keymap)):
            keymap.append(rev_keymap.index(idx))
        return keymap

    # Color Pallette - Roll
    ROLL_METERBAR_COLOR = [.3, .3, .3, 1]
    ROLL_BACKGROUND_COLOR = [.8, .8, 1, 1]
    ROLL_IVORY_COLOR = [1, 1, 1, 1]
    ROLL_EBONY_COLOR = [.8, .8, .8, 1.0]
    ROLL_TIMEBAR_COLOR = [1, .1, .1, 1]
    @staticmethod
    def ROLL_NOTEMAP():
        """ returns list of {y, height} for each note in the roll """
        notemap = []

        # pos_y / interval
        pos_y = 0
        interval = 13

        for i in range(128):                  
            notemap.append({
                'y': pos_y,
                'height': interval
            })
            pos_y += interval
        return notemap


    # Color Pallette - Note
    NOTE_COLOR = {
        0 : [0.5, 0.5, 0.5],
        1 : [0.34, 0.34, 0.34],
        2 : [0.67, 0.13, 0.13],
        3 : [0.16, 0.29, 0.84],
        4 : [0.11, 0.41, 0.07],
        5 : [0.5, 0.29, 0.09],
        6 : [0.5, 0.14, 0.75],
        7 : [0.62, 0.62, 0.62],
        8 : [0.5, 0.77, 0.47],
        9 : [0.61, 0.68, 1],
        10 : [0.16, 0.81, 0.81],
        11 : [1, 0.57, 0.2],
        12 : [1, 0.93, 0.2],
        13 : [0.91, 0.87, 0.73],
        14 : [1, 0.8, 0.95],
        15 : [0.2, 0.2, 0.2]
    }