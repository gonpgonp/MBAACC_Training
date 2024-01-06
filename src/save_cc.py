import cfg_cc
cfg = cfg_cc

class Save_info:
    def __init__(self):
        self.obj = cfg.para(74576)
        self.stop_situation = cfg.para(1632)
        self.stop = cfg.para(1)
        self.damage = cfg.para(52)
        self.damage2 = cfg.para(1004)
        self.cam1_x = cfg.para(4)
        self.cam2_x = cfg.para(4)
        self.cam1_y = cfg.para(4)
        self.cam2_y = cfg.para(4)
        self.contl_flag = cfg.para(4)
        self.contl_flag2 = cfg.para(4)

        self.active1 = 0
        self.active2 = 0
        self.active3 = 0
        self.active4 = 0


S_info = [Save_info(), Save_info(), Save_info()]
