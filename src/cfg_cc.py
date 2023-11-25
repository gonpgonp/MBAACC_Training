from ctypes import create_string_buffer
Bar80_flag = 0
bar_range = 80
mem_range = 400

class para:
    def __init__(self, byte_len):
        self.ad = 0x00
        self.num = 0
        self.b_dat = create_string_buffer(byte_len)

class Character_info:
    def __init__(self):
        #Full Character
        self.dmp = para(971)
        
        #State
        self.exist = para(1)
        self.pattern = para(2)
        self.state = para(4)
        
        #Meters
        self.health = para(4)
        self.rhealth = para(4)
        self.circuit = para(4)
        
        #Movement
        self.x_posi = para(4)
        self.y_posi1 = para(4)
        self.y_posi2 = para(4)
        self.x_spd = para(4)
        self.y_spd = para(4)
        self.x_acc = para(2)
        self.y_acc = para(2)
        self.momentum = para(4)

        #Others
        self.shield_time = para(2)
        self.hitstop = para(1)
        self.step_inv = para(1)
        self.untechend = para(2)
        self.untech = para(2)
        self.hitstun = para(4)
        self.chstate = para(1)
        self.grav = para(4)
        self.utpen = para(2)
        
        #Inputs
        self.dir_input = para(1)
        self.button_input = para(1)
        self.macro_input = para(1)
        
        #Pointers
        self.pat_st_pointer = para(4)
        self.anim_st_pointer = para(4)
        self.st_pointer = para(4) #child of anim_st_pointer
        self.atk_st_pointer = para(4)
        
        #Pointer Children
        self.anim_box = para(1)
        self.st_sac = para(1)
        self.st_invuln = para(1)
        
        #Addresses outside of character
        self.tag_flag = para(1)
        self.anten_stop = para(1)
        self.motion = para(4)
        
        self.active = 0
        
        self.Bar_1 = ''
        self.Bar_2 = ''
        self.Bar_3 = ''
        self.Bar_4 = ''
        self.Bar_5 = ''
        self.barlist_1 = [""] * mem_range
        self.barlist_2 = [""] * mem_range
        self.barlist_3 = [""] * mem_range
        self.barlist_4 = [""] * mem_range
        self.barlist_5 = [""] * mem_range

class Actor_info:
    def __init__(self):
        #State
        self.exist = para(1)
        self.pattern = para(4)
        self.state = para(4)
        
        #Others
        self.owner = para(1)
        
        #Pointers
        self.atk_st_pointer = para(4)

P_info = [Character_info(), Character_info(), Character_info(), Character_info()]
p_info = [Character_info(), Character_info(), Character_info(), Character_info()]

A_info = [Actor_info() for i in range(100)]

for info1, info2 in zip(P_info, p_info):
    for n in range(bar_range):
        info1.barlist_1[n] = ""
        info1.barlist_2[n] = ""
        info1.barlist_3[n] = ""
        info1.barlist_4[n] = ""
        info1.barlist_5[n] = ""

        info2.barlist_1[n] = ""
        info2.barlist_2[n] = ""
        info2.barlist_3[n] = ""
        info2.barlist_4[n] = ""
        info2.barlist_5[n] = ""

pid = 0
h_pro = 0
base_ad = 0
f_timer = 0
b_timer = create_string_buffer(4)
f_timer2 = 0
fn1_key = para(1)
fn2_key = para(1)
dummy_st = para(1)
recording_mode = para(1)
stop = para(2)
game_mode = para(1)

P1 = P_info[0]
P2 = P_info[1]
P3 = P_info[2]
P4 = P_info[3]

p1 = p_info[0]
p2 = p_info[1]
p3 = p_info[2]
p4 = p_info[3]

bar_flag = 0
bar_num = 0
bar_ini_flag = 0
bar_ini_flag2 = 0
st_Bar = ""
bar_offset_f = 0.0
bar_offset = 0

DataFlag1 = 1
anten = 0
anten_flag = 0
advantage_f = 0
hitstop = 0
interval = 41
interval2 = 80
interval_time = 0
reset_flag = 0
temp = create_string_buffer(4)
debug_flag = 0
extra_save = 1