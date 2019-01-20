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