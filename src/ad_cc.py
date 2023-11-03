
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
cfg.directional_input.ad = 0x371398
cfg.a_input.ad = 0x371399
cfg.b_input.ad = 0x37139A
cfg.c_input.ad = 0x37139B
cfg.d_input.ad = 0x37139C
cfg.e_input.ad = 0x37139D
cfg.ab_input.ad = 0x37139E
cfg.fn1_key.ad = FN1_KEY_AD = 0x37144C  # BUTTON_FN1
cfg.fn2_key.ad = FN2_KEY_AD = 0x37144D  # BUTTON_FN2 リセットキー
cfg.dummy_st.ad = DUMMY_STATUS_AD = 0x34D7F8
# STATUS_STAND( 0 )STATUS_JUMP( 1 )#STATUS_CROUCH( 2 )
# STATUS_CPU( 3 )#STATUS_MANUAL( 4 )#STATUS_DUMMY( 5 )
#STATUS_RECORD( -1 )
cfg.recording_mode.ad = RECORDING_MODE_AD = 0x155137
cfg.stop.ad = ANTEN_STOP_AD = 0x162A48  # 全体停止
cfg.game_mode.ad = GAME_MODE_AD = 0x14EEE8

TRAINING_PAUSE_AD = 0x162A64  # メニュー画面開いているとき
MAX_DAMAGE_AD = 0x157E0C
CIRCUIT_POSITION = 0x15DEF0
RESET_AD = 0x15DEC3  # リセット FF
COMB_AFTER_TIMER_AD = 0x36E708

PLR_STRUCT_SIZE = 0xAFC  # 3084
DAT_P1_AD = 0x155140  # 1Pデータ開始位置
DAT_P2_AD = DAT_P1_AD + PLR_STRUCT_SIZE
DAT_P3_AD = DAT_P2_AD + PLR_STRUCT_SIZE
DAT_P4_AD = DAT_P3_AD + PLR_STRUCT_SIZE

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

temp = 0
for n in P_info:
    n.dmp.ad = 0x155140 + temp
    n.motion_type.ad = 0x155140 + temp
    n.pframe.ad = 0x155144 + temp
    n.health.ad = 0x1551EC + temp
    n.rhealth.ad = 0x1551F0 + temp
    n.atk.ad = 0x155454 + temp
    n.step_inv.ad = 0x1552B5 + temp
    n.x_posi.ad = 0x155140 + 0xF8 + temp
    n.y_posi1.ad = 0x15523C + temp
    n.y_posi2.ad = 0x155248 + temp
    n.x_spd.ad = 0x15524C + temp
    n.x_acc.ad = 0x155254 + temp
    n.momentum.ad = 0x155268 + temp
    n.y_spd.ad = 0x155250 + temp
    n.y_acc.ad = 0x155256 + temp
    n.air_flag.ad = 0x155256 + temp
    n.circuit.ad = 0x155210 + temp
    n.hitstun.ad = 0x1552DC + temp
    n.untech.ad = 0x1552C0 + temp
    n.untechend.ad = 0x1552BE + temp
    n.chstate.ad = 0x15532A + temp
    n.grav.ad = 0x155414 + temp
    n.utpen.ad = 0x155418 + temp

    n.hitstop.ad = 0x155140 + 0x162 + temp
    n.atk_st_pointer.ad = 0x155450 + temp
    n.throw_inv.ad = 0x155149 + temp
    n.rigid_f.ad = 0x1552DC + temp

    temp += PLR_STRUCT_SIZE

temp2 = 0
for o in A_info:
    o.state.ad = 0x27BDFC + temp2
    o.despawn_check.ad = 0x027BE08 + temp2
    o.owner.ad = 0x27C0DC + temp2
    o.atk_data.ad = 0x27C10C + temp2
    
    temp2 += ACTOR_STRUCT_SIZE

P_info[0].tag_flag.ad = 0x1552A8
P_info[1].tag_flag.ad = 0x155DA4
P_info[2].tag_flag.ad = 0x1552A8
P_info[3].tag_flag.ad = 0x155DA4

P_info[0].anten_stop.ad = 0x158908
P_info[1].anten_stop.ad = 0x158908 + 0x30C
P_info[2].anten_stop.ad = 0x158908
P_info[3].anten_stop.ad = 0x158908 + 0x30C

P_info[0].motion.ad = 0x157FC0
P_info[1].motion.ad = 0x1581CC
P_info[2].motion.ad = 0x157FC0
P_info[3].motion.ad = 0x1581CC
