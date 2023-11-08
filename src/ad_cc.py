import cfg_cc
import save_cc

cfg = cfg_cc
save = save_cc
P_info = cfg.P_info
A_info = cfg.A_info
S_info = save.S_info

###########################################################################
# 各種アドレス
###########################################################################
TIMER_AD = 0x162A40
cfg.fn1_key.ad = FN1_KEY_AD = 0x37144C  # BUTTON_FN1
cfg.fn2_key.ad = FN2_KEY_AD = 0x37144D  # BUTTON_FN2 リセットキー
cfg.dummy_st.ad = DUMMY_STATUS_AD = 0x34D7F8
# STATUS_STAND  ( 0 ) STATUS_JUMP  ( 1 ) STATUS_CROUCH( 2 )
# STATUS_CPU    ( 3 ) STATUS_MANUAL( 4 ) STATUS_DUMMY ( 5 )
# STATUS_RECORD( -1 )
cfg.recording_mode.ad = RECORDING_MODE_AD = 0x155137
cfg.stop.ad = ANTEN_STOP_AD = 0x162A48  # 全体停止
cfg.game_mode.ad = GAME_MODE_AD = 0x14EEE8

TRAINING_PAUSE_AD = 0x162A64  # メニュー画面開いているとき
MAX_DAMAGE_AD = 0x157E0C
CIRCUIT_POSITION = 0x15DEF0
RESET_AD = 0x15DEC3  # リセット FF
COMB_AFTER_TIMER_AD = 0x36E708

PLR_STRUCT_BASE_ADDRESS = 0x155130
PLR_STRUCT_SIZE = 0xAFC  # 3084

ACTOR_STRUCT_BASE_ADDRESS = 0x027BDE8
ACTOR_STRUCT_SIZE = 0x33C

CAM1_X_AD = 0x164B14
CAM1_Y_AD = 0x15DEC4
CAM2_X_AD = 0x164B18
CAM2_Y_AD = 0x15DEC8

OBJ_AD = 0x27BD70  # オブジェクトデータ開始位置
STOP_SITUATION_AD = 0x158600  # 停止状況データ開始位置
DAMAGE_AD = 0x157DD8  # ダメージアドレス開始位置
DAMAGE2_AD = 0x157E10  # ダメージアドレス開始位置
CONTL_FLAG_AD = 0x157DB8  # 操作フラグ
CONTL_FLAG2_AD = 0x157DBc  # 操作フラグ

for m in S_info:
    m.obj.ad = OBJ_AD
    m.stop_situation.ad = STOP_SITUATION_AD
    m.stop.ad = ANTEN_STOP_AD
    m.damage.ad = DAMAGE_AD
    m.damage2.ad = DAMAGE2_AD
    m.cam1_x.ad = CAM1_X_AD
    m.cam2_x.ad = CAM2_X_AD
    m.cam1_y.ad = CAM1_Y_AD
    m.cam2_y.ad = CAM2_Y_AD
    m.contl_flag.ad = CONTL_FLAG_AD
    m.contl_flag2.ad = CONTL_FLAG_AD

loop_address = PLR_STRUCT_BASE_ADDRESS
for n in P_info:
    #Full Character
    n.dmp.ad =          loop_address + 0x10 #Skip recording address at +0x07
    
    #State
    n.exist.ad =        loop_address + 0x00
    n.pattern.ad =      loop_address + 0x10
    n.state.ad =        loop_address + 0x14
    
    #Meters
    n.health.ad =       loop_address + 0xBC
    n.rhealth.ad =      loop_address + 0xC0
    n.circuit.ad =      loop_address + 0xE0
    
    #Movement
    n.x_posi.ad =       loop_address + 0x108
    n.y_posi1.ad =      loop_address + 0x10C
    n.y_posi2.ad =      loop_address + 0x118
    n.x_spd.ad =        loop_address + 0x11C
    n.y_spd.ad =        loop_address + 0x120
    n.x_acc.ad =        loop_address + 0x124
    n.y_acc.ad =        loop_address + 0x126
    n.momentum.ad =     loop_address + 0x138
    
    #Others
    n.shield_time.ad =  loop_address + 0x16C
    n.hitstop.ad =      loop_address + 0x172
    n.step_inv.ad =     loop_address + 0x185
    n.airtime.ad =      loop_address + 0x18A
    n.untechend.ad =    loop_address + 0x18E
    n.untech.ad =       loop_address + 0x190
    n.hitstun.ad =      loop_address + 0x1AC
    n.chstate.ad =      loop_address + 0x1FA
    n.grav.ad =         loop_address + 0x2E4
    n.utpen.ad =        loop_address + 0x2E8
    
    #Inputs
    n.dir_input.ad =    loop_address + 0x2EA
    n.button_input.ad = loop_address + 0x2ED
    n.macro_input.ad =  loop_address + 0x2EE
    
    #Pointers
    n.pat_st_pointer.ad =   loop_address + 0x31C
    n.anim_st_pointer.ad =  loop_address + 0x320
    n.atk_st_pointer.ad =   loop_address + 0x324

    loop_address += PLR_STRUCT_SIZE

loop_address_2 = ACTOR_STRUCT_BASE_ADDRESS
for o in A_info:
    #State
    o.exist.ad =            loop_address_2 + 0x00
    o.pattern.ad =          loop_address_2 + 0x10
    o.state.ad =            loop_address_2 + 0x14
    
    #Others
    o.owner.ad =            loop_address_2 + 0x2F4
    
    #Pointers
    o.atk_st_pointer.ad =   loop_address_2 + 0x324
    
    loop_address_2 += ACTOR_STRUCT_SIZE

P_info[0].tag_flag.ad =     0x1552A8
P_info[1].tag_flag.ad =     0x155DA4
P_info[2].tag_flag.ad =     0x1552A8
P_info[3].tag_flag.ad =     0x155DA4

P_info[0].motion.ad =       0x157FC0
P_info[1].motion.ad =       0x1581CC
P_info[2].motion.ad =       0x157FC0
P_info[3].motion.ad =       0x1581CC

P_info[0].anten_stop.ad =   0x158908
P_info[1].anten_stop.ad =   0x158908 + 0x30C
P_info[2].anten_stop.ad =   0x158908
P_info[3].anten_stop.ad =   0x158908 + 0x30C