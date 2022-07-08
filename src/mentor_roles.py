"""Stores roles for mentors"""
class MentorRoles:
    """Enum for Mentor Roles in OS Paradise"""
    GENERAL_PVM = { 'name': 'General PvM', 'abr': 'pvm' }
    COX = { 'name': 'Chambers of Xeric', 'abr': 'cox,chambers' }
    COX_CM = { 'name': 'Challenge Mode: Chambers of Xeric', \
        'abr': 'cox,chambers,cm' }
    TOB = { 'name': 'Thearte of Blood', 'abr': 'tob' }
    TOB_HM = { 'name': 'Hard Mode: Thearte of Blood', 'abr': 'tob, hm tob' }
    VORKATH = { 'name': 'Vorkath', 'abr': 'vork,vorkath' }
    ZULRAH = { 'name': 'Zulrah', 'abr': 'zulrah' }
    SOLO_COX = {'name': 'Chambers of Xeric: Solo', \
        'abr': 'cox solo,solo cox'}
    GAUNTLET = { 'name': 'Gauntlet', 'abr': 'gauntlet,cg,corrupted gauntlet' }
    INFERNO = { 'name': 'Inferno', 'abr': 'inferno,infernal cape' }
    JAD = { 'name': 'Jad', 'abr': 'fire cape,fight caves,jad' }
    SEPULCHRE = {'name': 'Hallowed Sepulchre', \
        'abr': 'sepulchre,hallowed sepulchre'}
    GWD = {'name': 'God wars dungeon', \
        'abr': 'gwd,zammy,sara,kril,arma,bandos'}
    NEX = { 'name': 'Nex', 'abr': 'nex' }
    NIGHTMARE = { 'name': 'Nightmare', 'abr': 'nightmare' }

    ACCEPTED_CONTENT = 'gwd, cox, tob, vork, vorkath, zul, zulrah',\
    'gauntlet, cg, corrupted gauntlet, inferno','Sepulchre', 'gwd', 'nex'

    def get_abbreviation(self, content_type):
        """Return abbreviation for the given content type"""
        switcher = {
            self.GENERAL_PVM['name']: 'PvM',
            self.COX['name']: 'CoX',
            self.COX_CM['name']: 'CoX CM',
            self.TOB['name']: 'ToB',
            self.TOB_HM['name']: 'Hardmode ToB',
            self.VORKATH['name']: 'Vorkath',
            self.ZULRAH['name']: 'Zulrah',
            self.SOLO_COX['name']: 'Solo CoX',
            self.GAUNTLET['name']: 'Gauntlet',
            self.INFERNO['name']: 'Inferno',
            self.JAD['name']: 'Jad',
            self.SEPULCHRE['name']: 'Sepulchre',
            self.GWD['name']: 'GWD',
            self.NEX['name']: 'Nex',
            self.NIGHTMARE['name']: 'Nightmare'
        }
        return switcher.get(content_type, None)
