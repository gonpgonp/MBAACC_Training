
import cfg_cc
import save_cc

cfg = cfg_cc
save = save_cc
P_info = cfg.P_info

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
save.stop.ad = save.stop_2.ad = cfg.stop.ad = ANTEN_STOP_AD = 0x162A48  # 全体停止
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

save.cam1_x.ad = save.cam1_x_2.ad = CAM1_X_AD = 0x164B14
save.cam2_x.ad = save.cam2_x_2.ad = CAM1_Y_AD = 0x15DEC4
save.cam1_y.ad = save.cam1_y_2.ad = CAM2_X_AD = 0x164B18
save.cam2_y.ad = save.cam2_y_2.ad = CAM2_Y_AD = 0x15DEC8

save.obj.ad = save.obj_2.ad = OBJ_AD = 0x27BD70  # オブジェクトデータ開始位置
save.stop_situation.ad = save.stop_situation_2.ad = STOP_SITUATION_AD = 0x158600  # 停止状況データ開始位置
save.damage.ad = save.damage_2.ad = DAMAGE_AD = 0x157DD8  # ダメージアドレス開始位置
save.damage2.ad = save.damage2_2.ad = DAMAGE2_AD = 0x157E10  # ダメージアドレス開始位置
save.contl_flag.ad = save.contl_flag_2.ad = CONTL_FLAG_AD = 0x157DB8  # 操作フラグ
save.contl_flag2.ad = save.contl_flag2_2.ad = CONTL_FLAG_AD = 0x157DBc  # 操作フラグ


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
