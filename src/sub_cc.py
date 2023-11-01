from ctypes import windll, wintypes, byref
from struct import unpack, pack
import os
import time
import copy
import ctypes
import keyboard
import psutil
import math

import cfg_cc
import ad_cc
import save_cc
cfg = cfg_cc
ad = ad_cc
save = save_cc

wintypes = ctypes.wintypes
windll = ctypes.windll
create_string_buffer = ctypes.create_string_buffer
byref = ctypes.byref
WriteMem = windll.kernel32.WriteProcessMemory
ReadMem = windll.kernel32.ReadProcessMemory
OpenProcess = windll.kernel32.OpenProcess
Module32Next = windll.kernel32.Module32Next
Module32First = windll.kernel32.Module32First
CreateToolhelp32Snapshot = windll.kernel32.CreateToolhelp32Snapshot
CloseHandle = windll.kernel32.CloseHandle
sizeof = ctypes.sizeof

class MODULEENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize",             wintypes.DWORD),
        ("th32ModuleID",       wintypes.DWORD),
        ("th32ProcessID",      wintypes.DWORD),
        ("GlblcntUsage",       wintypes.DWORD),
        ("ProccntUsage",       wintypes.DWORD),
        ("modBaseAddr",        ctypes.POINTER(wintypes.BYTE)),
        ("modBaseSize",        wintypes.DWORD),
        ("hModule",            wintypes.HMODULE),
        ("szModule",           ctypes.c_byte * 256),
        ("szExePath",          ctypes.c_byte * 260),
    ]


def pidget():
    dict_pids = {
        p.info["name"]: p.info["pid"]
        for p in psutil.process_iter(attrs=["name", "pid"])
    }
    return dict_pids


def get_base_addres():
    cfg.pid = 0
    while cfg.pid == 0:
        dict_pids = pidget()
        try:
            cfg.pid = dict_pids["MBAA.exe"]
        except:
            os.system('cls')
            print("Waiting for MBAA to start")
            time.sleep(0.2)

    cfg.h_pro = OpenProcess(0x1F0FFF, False, cfg.pid)

    # MODULEENTRY32を取得
    snapshot = CreateToolhelp32Snapshot(0x00000008, cfg.pid)

    lpme = MODULEENTRY32()
    lpme.dwSize = sizeof(lpme)

    res = Module32First(snapshot, byref(lpme))

    while cfg.pid != lpme.th32ProcessID:
        res = Module32Next(snapshot, byref(lpme))

    b_baseAddr = create_string_buffer(8)
    b_baseAddr.raw = lpme.modBaseAddr

    cfg.base_ad = unpack('q', b_baseAddr.raw)[0]


def b_unpack(d_obj):
    num = 0
    num = len(d_obj)
    if num == 1:
        return unpack('b', d_obj.raw)[0]
    elif num == 2:
        return unpack('h', d_obj.raw)[0]
    elif num == 4:
        return unpack('l', d_obj.raw)[0]

def f_unpack(d_obj):
    return unpack('f', d_obj.raw)[0]

def r_mem(ad, b_obj):
    ReadMem(cfg.h_pro, ad + cfg.base_ad, b_obj, len(b_obj), None)
    return b_unpack(b_obj)


def r_mem_2(ad, b_obj):
    ReadMem(cfg.h_pro, ad, b_obj, len(b_obj), None)
    return b_unpack(b_obj)


def r_mem_f(ad, b_obj):
    ReadMem(cfg.h_pro, ad + cfg.base_ad, b_obj, len(b_obj), None)
    return f_unpack(b_obj)


def w_mem(ad, b_obj):
    WriteMem(cfg.h_pro, ad + cfg.base_ad, b_obj, len(b_obj), None)


def para_get(obj):
    obj.num = r_mem(obj.ad, obj.b_dat)


def para_get_2(obj):
    obj.num = r_mem_2(obj.ad, obj.b_dat)


def para_get_f(obj):
    obj.num  = r_mem_f(obj.ad, obj.b_dat)


def para_set(obj):
    w_mem(obj.ad, obj.b_dat)


def ex_cmd_enable():
    INVALID_HANDLE_VALUE = -1
    STD_INPUT_HANDLE = -10
    STD_OUTPUT_HANDLE = -11
    STD_ERROR_HANDLE = -12
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
    ENABLE_LVB_GRID_WORLDWIDE = 0x0010

    hOut = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    if hOut == INVALID_HANDLE_VALUE:
        return False
    dwMode = wintypes.DWORD()
    if windll.kernel32.GetConsoleMode(hOut, byref(dwMode)) == 0:
        return False
    dwMode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
    # dwMode.value |= ENABLE_LVB_GRID_WORLDWIDE
    if windll.kernel32.SetConsoleMode(hOut, dwMode) == 0:
        return False
    return True


def situationCheck():
    # 状況チェック
    para_get(cfg.directional_input)
    para_get(cfg.a_input)
    para_get(cfg.b_input)
    para_get(cfg.c_input)
    para_get(cfg.d_input)
    para_get(cfg.e_input)
    para_get(cfg.ab_input)
    para_get(cfg.fn1_key)
    para_get(cfg.fn2_key)
    para_get(cfg.dummy_st)
    para_get(cfg.recording_mode)
    para_get(cfg.stop)

    for n in cfg.P_info:
        if n.motion_type.num != 0:
            n.motion_type_old = n.motion_type.num
        para_get(n.motion_type)
        para_get(n.motion)
        para_get(n.pframe)
        para_get(n.health)
        para_get(n.rhealth)
        para_get(n.x_posi)
        para_get(n.y_posi1)
        para_get(n.y_posi2)
        para_get(n.x_spd)
        para_get(n.x_acc)
        para_get(n.momentum)
        para_get(n.y_spd)
        para_get(n.y_acc)
        para_get(n.air_flag)
        para_get(n.circuit)
        para_get(n.atk)
        para_get(n.step_inv)
        para_get(n.seeld)
        para_get(n.tag_flag)
        para_get(n.anten_stop)
        para_get(n.hitstop)
        para_get(n.stop)
        para_get(n.hitstun)
        para_get(n.untech)
        para_get(n.untechend)
        para_get(n.chstate)
        para_get_f(n.grav)
        para_get(n.utpen)
        n.hit.num = 0
        para_get(n.throw_inv)
        para_get(n.atk_st_pointer)
        n.atk_st.ad = n.atk_st_pointer.num + 0x42
        n.throw.ad = n.atk_st_pointer.num + 0x44
        para_get_2(n.atk_st)
        para_get_2(n.throw)

    tagCharacterCheck()


def tagCharacterCheck():

    if cfg.P1.tag_flag.num == 0:
        cfg.p_info[0] = cfg.p1 = cfg.P1
        cfg.p_info[2] = cfg.p3 = cfg.P3

    elif cfg.P1.tag_flag.num == 1:
        cfg.p_info[0] = cfg.p1 = cfg.P3
        cfg.p_info[2] = cfg.p3 = cfg.P1

    if cfg.P2.tag_flag.num == 0:
        cfg.p_info[1] = cfg.p2 = cfg.P2
        cfg.p_info[3] = cfg.p4 = cfg.P4

    elif cfg.P2.tag_flag.num == 1:
        cfg.p_info[1] = cfg.p2 = cfg.P4
        cfg.p_info[3] = cfg.p4 = cfg.P2

def sitMem(n):
    save_info = save.S_info[n]
    
    save_info.P_info = copy.deepcopy(cfg.P_info)
    
    for i in save_info.P_info:
        para_get(i.dmp)
    
    para_get(save_info.obj)
    para_get(save_info.stop_situation)
    para_get(save_info.stop)
    para_get(save_info.damage)
    para_get(save_info.damage2)
    para_get(save_info.cam1_x)
    para_get(save_info.cam2_x)
    para_get(save_info.cam1_y)
    para_get(save_info.cam2_y)
    para_get(save_info.contl_flag)
    para_get(save_info.contl_flag2)
    
def sitWrite(n):
    save_info = save.S_info[n]
    
    for i in save_info.P_info:
        para_set(i.dmp)
    
    para_set(save_info.obj)
    para_set(save_info.stop_situation)
    para_set(save_info.stop)
    para_set(save_info.damage)
    para_set(save_info.damage2)
    para_set(save_info.cam1_x)
    para_set(save_info.cam2_x)
    para_set(save_info.cam1_y)
    para_set(save_info.cam2_y)
    para_set(save_info.contl_flag)
    para_set(save_info.contl_flag2)

def view_st():

    # 全体フレームの取得
    overall_calc()

    # 技の発生フレームの取得
    firstActive_calc()

    # 硬直差の取得
    advantage_calc()

    # キャラの状況推移表示
    if (cfg.p1.motion.num != 0 or cfg.p1.hitstop.num != 0 or cfg.p1.hit.num != 0 or
            cfg.p2.motion.num != 0 or cfg.p2.hitstop.num != 0 or cfg.p2.hit.num != 0) or (
            cfg.debug_flag == 1 and cfg.directional_input.num != 0):

        cfg.reset_flag = 0
        cfg.bar_flag = 1
        cfg.interval = 0
    else:
        cfg.bar_flag = 0
        cfg.interval += 1

    # バーリセット判定
    determineReset()

    # 表示管理　表示するものが無くても前回の表示からインターバルの間は無条件で表示する
    if cfg.interval_time >= cfg.interval and cfg.reset_flag == 0:
        cfg.bar_flag = 1

    if cfg.bar_flag == 1:

        stop_flame_calc()

        # 攻撃判定持続計算
        for n in cfg.p_info:
            if n.atk.num != 0 and cfg.anten == 0 and cfg.hitstop == 0:  # 攻撃判定を出しているとき
                n.active += 1
            elif n.atk.num == 0 and cfg.anten == 0 and cfg.hitstop <= 1:  # 攻撃判定を出してないとき
                n.active = 0
        
        barcheck = True
        if cfg.debug_flag == 0:
            barcheck = cfg.anten == 0 and cfg.hitstop <= 1
        
        if barcheck:
            cfg.bar_num += 1
            if cfg.bar_num == cfg.bar_range:
                cfg.bar_num = 0
                cfg.Bar80_flag = 1

        # バー追加処理
        bar_add()


def firstActive_calc():

    # 計測開始の確認
    if cfg.p2.hitstop.num != 0 and cfg.p1.act_flag == 0 and cfg.p1.hit.num == 0:
        cfg.p1.act = cfg.p1.zen
        cfg.p1.act_flag = 1

    if cfg.p1.hitstop.num != 0 and cfg.p2.act_flag == 0 and cfg.p2.hit.num == 0:
        cfg.p2.act = cfg.p2.zen
        cfg.p2.act_flag = 1

    if cfg.p1.motion.num == 0 and cfg.p1.atk.num == 0:
        cfg.p1.act_flag = 0

    if cfg.p2.motion.num == 0 and cfg.p2.atk.num == 0:
        cfg.p2.act_flag = 0


def advantage_calc():
    if cfg.p1.hit.num == 0 and cfg.p2.hit.num == 0 and cfg.p1.motion.num == 0 and cfg.p2.motion.num == 0:
        cfg.DataFlag1 = 0

    if (cfg.p1.hit.num != 0 or cfg.p1.motion.num != 0) and (cfg.p2.hit.num != 0 or cfg.p2.motion.num != 0):
        cfg.DataFlag1 = 1
        cfg.advantage_f = 0

    if cfg.DataFlag1 == 1:

        # 有利フレーム検証
        if (cfg.p1.hit.num == 0 and cfg.p1.motion.num == 0) and (cfg.p2.hit.num != 0 or cfg.p2.motion.num != 0):
            cfg.advantage_f += 1

        # 不利フレーム検証
        if (cfg.p1.hit.num != 0 or cfg.p1.motion.num != 0) and (cfg.p2.hit.num == 0 and cfg.p2.motion.num == 0):
            cfg.advantage_f -= 1


def overall_calc():
    # 全体フレームの取得
    if cfg.p1.motion.num != 0:
        cfg.p1.zen = cfg.p1.motion.num

    if cfg.p2.motion.num != 0:
        cfg.p2.zen = cfg.p2.motion.num


def determineReset():
    bar_ini_flag = 0

    if cfg.Bar80_flag == 1:
        cfg.interval_time = 10

    # インターバル後の初期化
    if cfg.interval_time <= cfg.interval:
        cfg.bar_ini_flag2 = 1

    # 表示するときリセット
    if cfg.bar_ini_flag2 == 1 and cfg.bar_flag == 1:
        bar_ini_flag = 1

    # 即時リセット
    if bar_ini_flag == 1:
        bar_ini()


def stop_flame_calc():

    # 暗転判定処理
    if cfg.stop.num != 0 and cfg.debug_flag == 0:
        cfg.anten += 1
    elif (cfg.p1.anten_stop.num != 0 or cfg.p2.anten_stop.num != 0) and cfg.debug_flag == 0:
        #cfg.anten += 1
        cfg.anten = 0
    else:
        cfg.anten = 0

    # ヒットストップ処理
    if (cfg.p1.hitstop.num != 0 and cfg.p2.hitstop.num != 0):
        cfg.hitstop += 1
    elif (cfg.p1.hitstop.num == 0 or cfg.p2.hitstop.num == 0):
        cfg.hitstop = 0


def text_font(rgb):
    Text_font_str = "\x1b[38;2;" + str(rgb[0]) + ";" + str(rgb[1]) + ";" + str(rgb[2]) + "m"
    return Text_font_str


def bg_font(rgb):
    bg_font_str = "\x1b[48;2;" + str(rgb[0]) + ";" + str(rgb[1]) + ";" + str(rgb[2]) + "m"
    return bg_font_str


def get_font(text_rgb, bg_rgb):
    return text_font(text_rgb) + bg_font(bg_rgb)


def bar_add():

    DEF = '\x1b[0m'
    FC_DEF = '\x1b[39m'
    BC_DEF = '\x1b[49m'

    atk = get_font((255, 255, 255), (255, 0, 0))
    mot = get_font((255, 255, 255), (65, 200, 0))
    grd_stun = get_font((255, 255, 255), (140, 140, 140))
    hit_stun = get_font((255, 255, 255), (140, 140, 140))
    fre = get_font((92, 92, 92), (0, 0, 0))
    jmp = get_font((177, 177, 177), (241, 224, 132))
    seeld = get_font((255, 255, 255), (145, 194, 255))
    inv = get_font((180, 180, 180), (255, 255, 255))
    inv_atk = get_font((255, 255, 255), (255, 160, 160))
    adv = get_font((255, 255, 255), (0, 0, 0))
    bunker = get_font((255, 255, 255), (225, 184, 0))
    bunker_atk = get_font((255, 255, 255), (225, 102, 0))
    air = get_font((125, 127, 168), (125, 127, 168))
    throw_number = [350]  # 投げやられ
    a_font = get_font((255, 143, 169), (170, 27, 58))
    b_font = get_font((255, 255, 137), (169, 91, 7))
    c_font = get_font((143, 255, 195), (18, 132, 62))
    d_font = get_font((137, 255, 255), (21, 66, 161))
    freeze = get_font((255, 255, 255), (60, 60, 60))

    hit_number = [
        26,  # 立吹っ飛び
        29,  # 足払いやられ
        30,  # 垂直吹っ飛び
        354,  # 小バウンド
        900,  # 立やられ
        901,  # 立やられ
        902,  # 屈やられ
        903,  # やられ
        904,  # やられ
        905,  # 屈大やられ
        906,  # 立大やられ
        907,  # 立大やられ２
        908  # 屈大やられ2
    ]
    grd_number = [
        17,  # 屈ガード
        18,  # 立ガード
        19,  # 空中ガード
    ]

    ignore_number = [0, 10, 11, 12, 13, 14, 15, 20, 16, 594]

    jmp_number = [34, 35, 36, 37]

    for n in cfg.p_info:

        if n.motion.num != 0:
            num = str(n.motion.num)
            font = mot
            for list_a in jmp_number:  # ジャンプ移行中
                if n.motion_type.num == list_a:
                    font = jmp
                    break

            for list_a in hit_number:  # ヒット中
                if n.motion_type.num == list_a:
                    font = hit_stun
                    if n.air_flag.num == 0 and n.y_posi1.num == 0 and n.y_posi2.num == 0:  # 地上にいる場合
                        if (n.hitstun.num - 1) > 0:
                            num = str(n.hitstun.num - 1)
                    elif n.air_flag.num == 150 or n.y_posi1.num != 0 or n.y_posi2.num != 0:  # 空中にいる場合:
                        if (n.untechend.num - n.untech.num) > 0:
                            num = str(n.untechend.num - n.untech.num)
                    break

            for list_a in grd_number:  # ガード中
                if n.motion_type.num == list_a:
                    font = grd_stun
                    if n.air_flag.num == 0 and n.y_posi1.num == 0 and n.y_posi2.num == 0:  # 地上にいる場合
                            if (n.hitstun.num - 1) > 0:
                                num = str(n.hitstun.num - 1)
                            else:
                                num = "0"
                    break

        elif n.motion.num == 0:
            num = str(n.motion_type.num)
            font = fre

            if cfg.DataFlag1 == 1:
                if n == cfg.p_info[0] or n == cfg.p_info[1]:
                    font = adv
                    num = str(abs(cfg.advantage_f))

        if n.motion_type.num == 350:  # 投げやられ
            font = hit_stun

        elif n.atk_st.num == 12:  # バンカー　or 相殺
            font = bunker

        elif (n.atk_st.num == 10) and n.atk.num == 0:  # シールド
            font = seeld

        elif n.atk_st.num == 1 or n.atk_st.num == 0 or n.step_inv.num != 0:  # 無敵中
            font = inv
        
        if cfg.stop.num != 0 and cfg.debug_flag == 1:
            font = freeze
        
        n.barlist_1[cfg.bar_num] = font + num.rjust(2, " ")[-2:] + DEF

        font = ""
        num = ""
        
        if n.air_flag.num == 150 or n.y_posi1.num != 0 or n.y_posi2.num != 0:  # 空中にいる場合:
            num = "^"
        elif cfg.p1.anten_stop.num != 0 or cfg.p2.anten_stop.num != 0:
            num = "*"

        if n.atk.num != 0:  # 攻撃判定を出しているとき
            font = atk
            num = str(n.active)
            if n.air_flag.num == 150 or n.y_posi1.num != 0 or n.y_posi2.num != 0:  # 空中にいる場合:
                font += "\x1b[4m"

        if cfg.p1.anten_stop.num != 0 or cfg.p2.anten_stop.num != 0:
            font += "\x1b[38;2;160;200;200m"

        n.barlist_2[cfg.bar_num] = font + num.rjust(2, " ")[-2:] + DEF
        
        #num = str(n.motion_type.num)
        bar3 = ""
        button_pressed = 0
        if cfg.a_input.num > 0 or cfg.b_input.num > 0 or cfg.c_input.num > 0 or cfg.d_input.num > 0 or cfg.e_input.num > 0 or cfg.ab_input.num > 0:
            button_pressed = 1
        else:
            button_pressed = 0
        
        if cfg.e_input.num > 0 and cfg.ab_input.num > 0:
            num = "EF"
        elif cfg.e_input.num > 0:
            num = "E "
        elif cfg.ab_input.num > 0:
            num = " F"
        else:
            num = "  "
        
        if cfg.a_input.num > 0:
            font = a_font
        elif button_pressed == 1:
            font = hit_stun
        else:
            font = DEF
        bar3 += font + num[0] + DEF
        
        if cfg.b_input.num > 0:
            font = b_font
        elif button_pressed == 1:
            font = hit_stun
        else:
            font = DEF
        bar3 += font + num[1] + DEF
        n.barlist_3[cfg.bar_num] = bar3

        #num = str(n.rigid_f.num)
        bar4 = ""
        num = cfg.directional_input.num
        if cfg.directional_input.num < 0:
            num += 128
        num = str(num).rjust(2, " ")[-2:]
        if num == " 0":
            num = " ."
        
        if cfg.c_input.num > 0:
            font = c_font
        elif button_pressed == 1:
            font = hit_stun
        else:
            font = DEF
        bar4 += font + num[0] + DEF
        font = DEF
        
        if cfg.d_input.num > 0:
            font = d_font
        elif button_pressed == 1:
            font = hit_stun
        else:
            font = DEF
        bar4 += font + num[1] + DEF
        n.barlist_4[cfg.bar_num] = bar4


def bar_ini():
    cfg.reset_flag = 1

    for n in cfg.p_info:
        n.Bar_1 = ""
        n.Bar_2 = ""
        n.Bar_3 = ""
        n.Bar_4 = ""

    cfg.st_Bar = ""
    cfg.bar_num = 0
    cfg.interval = 0
    cfg.interval2 = 0
    cfg.bar_ini_flag2 = 0
    cfg.Bar80_flag = 0
    cfg.interval_time = 80

    for n in range(cfg.bar_range):
        for m in cfg.p_info:
            m.barlist_1[n] = ""
            m.barlist_2[n] = ""
            m.barlist_3[n] = ""
            m.barlist_4[n] = ""

        cfg.st_barlist[n] = ""

def view():
    END = '\x1b[0m' + '\x1b[49m' + '\x1b[K' + '\x1b[1E'
    
    x_p1 = str(cfg.p1.x_posi.num).rjust(6, " ")
    x_p2 = str(cfg.p2.x_posi.num).rjust(6, " ")
    xp_p1 = str(math.floor(cfg.p1.x_posi.num/128)).rjust(6, " ")
    xp_p2 = str(math.floor(cfg.p2.x_posi.num/128)).rjust(6, " ")
    xspd_p1_math = cfg.p1.x_spd.num
    xspd_p2_math = cfg.p2.x_spd.num
    xspd_p1 = str(xspd_p1_math).rjust(6, " ")
    xspd_p2 = str(xspd_p2_math).rjust(6, " ")
    xacc_p1 = str(cfg.p1.x_acc.num).rjust(6, " ")
    xacc_p2 = str(cfg.p2.x_acc.num).rjust(6, " ")
    
    momentum_p1_math = cfg.p1.momentum.num
    momentum_p2_math = cfg.p2.momentum.num
    xspdfinal_p1 = str(momentum_p1_math + xspd_p1_math).rjust(6, " ")
    xspdfinal_p2 = str(momentum_p2_math + xspd_p2_math).rjust(6, " ")

    y_p1 = str(cfg.p1.y_posi1.num).rjust(6, " ")
    y_p2 = str(cfg.p2.y_posi1.num).rjust(6, " ")    
    yp_p1 = str(math.floor(cfg.p1.y_posi1.num/128)).rjust(6, " ")
    yp_p2 = str(math.floor(cfg.p2.y_posi1.num/128)).rjust(6, " ")
    yspd_p1 = str(cfg.p1.y_spd.num).rjust(6, " ")
    yspd_p2 = str(cfg.p2.y_spd.num).rjust(6, " ")
    yacc_p1 = str(cfg.p1.y_acc.num).rjust(6, " ")
    yacc_p2 = str(cfg.p2.y_acc.num).rjust(6, " ")
    
    pat1 = str(cfg.p1.motion_type.num).rjust(6, " ")
    pf1 = str(cfg.p1.pframe.num).rjust(8, " ")
    pat2 = str(cfg.p2.motion_type.num).rjust(6, " ")
    pf2 = str(cfg.p2.pframe.num).rjust(8, " ")

    zen_P1 = str(cfg.p1.zen).rjust(6, " ")
    zen_P2 = str(cfg.p2.zen).rjust(6, " ")

    health_p1 = str(cfg.p1.health.num).rjust(7, " ")
    health_p2 = str(cfg.p2.health.num).rjust(7, " ")
    
    circuit_p1 = str(cfg.p1.circuit.num).rjust(6, " ")
    circuit_p2 = str(cfg.p2.circuit.num).rjust(6, " ")

    act_P1 = str(cfg.p1.act).rjust(7, " ")
    act_P2 = str(cfg.p2.act).rjust(7, " ")

    advantage_f = str(cfg.advantage_f).rjust(6, " ")

    kyori = cfg.p1.x_posi.num - cfg.p2.x_posi.num
    trange = cfg.p1.x_posi.num - cfg.p2.x_posi.num
    prange = math.floor(cfg.p1.x_posi.num/128) - math.floor(cfg.p2.x_posi.num/128)

    for n in cfg.p_info:
        n.Bar_1 = ""
        n.Bar_2 = ""
        n.Bar_3 = ""
        n.Bar_4 = ""

    cfg.st_Bar = ""

    temp = cfg.bar_num

    for n in range(cfg.bar_range):
        temp += 1
        if temp == cfg.bar_range:
            temp = 0

        for m in cfg.p_info:
            m.Bar_1 += m.barlist_1[temp]
            m.Bar_2 += m.barlist_2[temp]
            m.Bar_3 += m.barlist_3[temp]
            m.Bar_4 += m.barlist_4[temp]

        cfg.st_Bar += cfg.st_barlist[temp]

    if kyori < 0:
        kyori = kyori * -1
    kyori = kyori / (21845)
    kyori = str(kyori)[:5]
    
    if trange < 0:
        trange = trange * -1
    trange = str(trange)
    
    if prange < 0:
        prange = prange * -1
    prange = str(prange)

    state_str = '\x1b[1;1H' + '\x1b[?25l'

    state_str += f'1P|({x_p1},'
    state_str += f' {y_p1})'
    state_str += f' |Pattern{pat1}'
    state_str += f' |Frame{pf1}'
    state_str += f' |Health{health_p1}'
    state_str += f' |Circuit{circuit_p1}'

    if keyboard.is_pressed("F1"):
        f1 = '  \x1b[007m' + '[F1]Reset' + '\x1b[0m'
    else:
        f1 = '  [F1]Reset'

    if keyboard.is_pressed("F2"):
        f2 = '  \x1b[007m' + '[F2]Save state' + '\x1b[0m'
    else:
        f2 = '  [F2]Save state'

    if keyboard.is_pressed("F6"):
        f6 = '  \x1b[007m' + '[F6]Load state' + '\x1b[0m'
    else:
        f6 = '  [F6]Load state'

    if keyboard.is_pressed("F7"):
        f7 = '  \x1b[007m' + '[F7]Save state 2' + '\x1b[0m'
    else:
        f7 = '  [F7]Save state 2'

    if keyboard.is_pressed("F8"):
        f8 = '  \x1b[007m' + '[F8]Load state 2' + '\x1b[0m'
    else:
        f8 = '  [F8]Load state 2'

    state_str += '   ' + f1 + '       ' + f2 + '  ' + f6 + END
    
    state_str += "\x1b[4m"
    state_str += f'  |({xp_p1},'
    state_str += f' {yp_p1})'
    state_str += f' |X-Speed{xspdfinal_p1}'
    state_str += f' |X-Accel{xacc_p1}'
    state_str += f' |Y-Speed{yspd_p1}'
    state_str += f' |Y-Accel{yacc_p1}'
    state_str += "\x1b[4m"
    state_str += END

    state_str += f'2P|({x_p2},'
    state_str += f' {y_p2})'
    state_str += f' |Pattern{pat2}'
    state_str += f' |Frame{pf2}'
    state_str += f' |Health{health_p2}'
    state_str += f' |Circuit{circuit_p2}'
    
    if keyboard.is_pressed(",") and keyboard.is_pressed("."):
        debughotkeys = '  \x1b[007m' + '[,.]Toggle Debug' + '\x1b[0m'
    else:
        debughotkeys = '  [,.]Toggle Extra Info'
    
    state_str += '   ' + f7 + f8 + debughotkeys + END
    
    state_str += "\x1b[4m"
    state_str += f'  |({xp_p2},'
    state_str += f' {yp_p2})'
    state_str += f' |X-Speed{xspdfinal_p2}'
    state_str += f' |X-Accel{xacc_p2}'
    state_str += f' |Y-Speed{yspd_p2}'
    state_str += f' |Y-Accel{yacc_p2}'
    state_str += "\x1b[4m"
    state_str += END

    state_str += '  |Advantage' + advantage_f
    state_str += '  Range ' + trange.rjust(7, " ")
    state_str += ' P-Range ' + prange.rjust(5, " ") + END

    tempstr = "\x1b[4m"
    for i in range(1,81):
        if i < 10:
            tempstr += " "
        tempstr += str(i)
        if i % 2 == 1:
            tempstr += "\x1b[4;48;5;238m"
        else:
            tempstr += "\x1b[0;4m"


    state_str += '  |' + tempstr + END
    state_str += '1P|' + cfg.p1.Bar_1 + END
    state_str += '  |' + cfg.p1.Bar_2 + END
    state_str += '2P|' + cfg.p2.Bar_1 + END
    state_str += '  |' + cfg.p2.Bar_2 + END

    if cfg.debug_flag == 1:
        state_str = degug_view(state_str)

    print(state_str)


def degug_view(state_str):
    END = '\x1b[0m' + '\x1b[49m' + '\x1b[K' + '\x1b[1E'
    tempstr = "\x1b[4m"
    for i in range(1,81):
        if i < 10:
            tempstr += " "
        tempstr += str(i)
        if i % 2 == 1:
            tempstr += "\x1b[4;48;5;238m"
        else:
            tempstr += "\x1b[0;4m"
    # os.system('mode con: cols=166 lines=15')
    debug_str_3 = '  |' + tempstr
    #debug_str_3 = "  |frame timer" + str(cfg.f_timer).rjust(7, " ")
    #debug_str_3 += " bar_num " + str(cfg.bar_num).rjust(7, " ")
    #debug_str_3 += " anten " + str(cfg.anten).rjust(8, " ")
    #debug_str_3 += " stop " + str(cfg.stop.num).rjust(11, " ")
    if (cfg.p1.anten_stop.num > 0):
        exflash_p1 = str(cfg.p1.anten_stop.num).rjust(4, " ")
    else:
        exflash_p1 = str(cfg.stop.num).rjust(4, " ")

    if (cfg.p2.anten_stop.num > 0):
        exflash_p2 = str(cfg.p2.anten_stop.num).rjust(4, " ")
    else:
        exflash_p2 = str(cfg.stop.num).rjust(4, " ")

    hitstop_p1 = str(cfg.p1.hitstop.num).rjust(4, " ")
    hitstop_p2 = str(cfg.p2.hitstop.num).rjust(4, " ")
    
    debug_str_p1 = f"1P|EX Flash{exflash_p1}"
    debug_str_p2 = f"2P|EX Flash{exflash_p2}"
    debug_str_p1 += f" |Hitstop{hitstop_p1}"
    debug_str_p2 += f" |Hitstop{hitstop_p2}"
    
    if(cfg.p1.chstate.num == 2):
        ch_p1 = "Low".rjust(6, " ")
    elif(cfg.p1.chstate.num == 1):
        ch_p1 = "High".rjust(6, " ")
    else:
        ch_p1 = "None".rjust(6, " ")

    if(cfg.p2.chstate.num == 2):
        ch_p2 = "Low".rjust(6, " ")
    elif(cfg.p2.chstate.num == 1):
        ch_p2 = "High".rjust(6, " ")
    else:
        ch_p2 = "None".rjust(6, " ")
        
    debug_str_p1 += f" |Counter{ch_p1}"
    debug_str_p2 += f" |Counter{ch_p2}"
    #debug_str_p1 += " y_posi " + str(cfg.p1.y_posi2.num).rjust(7, " ")
    #debug_str_p2 += " y_posi " + str(cfg.p2.y_posi2.num).rjust(7, " ")
    #debug_str_p1 += " |tag_flag " + str(cfg.p1.tag_flag.num).rjust(7, " ")
    #debug_str_p2 += " |tag_flag " + str(cfg.p2.tag_flag.num).rjust(7, " ")
    
    rhealth_p1 = str(cfg.p1.rhealth.num-cfg.p1.health.num).rjust(6, " ")
    rhealth_p2 = str(cfg.p2.rhealth.num-cfg.p2.health.num).rjust(6, " ")
    
    debug_str_p1 += f" |Red Health{rhealth_p1}"
    debug_str_p2 += f" |Red Health{rhealth_p2}"
    
    gravity_p1 = cfg.p1.grav.num
    gravity_p1 = max(0, round((gravity_p1 - 0.072) / 0.008))
    gravity_p1 -= math.floor(gravity_p1/60)
    gravity_p1 = math.ceil(gravity_p1/6)
    gravity_p1 = str(gravity_p1).rjust(2, " ")
    
    extra_grav_p1 = str(cfg.p1.utpen.num).rjust(2, " ")

    grav_hits_p1 = str(round(cfg.p1.grav.num / 0.008)).rjust(3, " ")
    
    gravity_p2 = cfg.p2.grav.num
    gravity_p2 = max(0, round((gravity_p2 - 0.072) / 0.008))
    gravity_p2 -= math.floor(gravity_p2/60)
    gravity_p2 = math.ceil(gravity_p2/6)
    gravity_p2 = str(gravity_p2).rjust(2, " ")
    
    extra_grav_p2 = str(cfg.p2.utpen.num).rjust(2, " ")

    grav_hits_p2 = str(round(cfg.p2.grav.num / 0.008)).rjust(3, " ")
    
    debug_str_p1 += f" |Penalty{grav_hits_p1} ({gravity_p1} + {extra_grav_p1})"
    debug_str_p2 += f" |Penalty{grav_hits_p2} ({gravity_p2} + {extra_grav_p2})"
    
    partner_mot_p1 = str(cfg.p3.motion_type.num).rjust(4, " ")
    partner_pf_p1 = str(cfg.p3.pframe.num).rjust(3, " ")
    
    partner_mot_p2 = str(cfg.p4.motion_type.num).rjust(4, " ")
    partner_pf_p2 = str(cfg.p4.pframe.num).rjust(3, " ")
    
    debug_str_p1 += f" |Partner{partner_mot_p1} ({partner_pf_p1})"
    debug_str_p2 += f" |Partner{partner_mot_p2} ({partner_pf_p2})"
    # debug_str_p2 += " interval " + str(cfg.interval).rjust(7, " ")
    # debug_str_p2 += " Bar80_flag " + str(cfg.Bar80_flag).rjust(7, " ")
    # debug_str_p1 += "anten_stop.ad " + str(cfg.P_info[0].motion_type.ad).rjust(7, " ")

    state_str += debug_str_p1 + END
    state_str += debug_str_p2 + END
    state_str += "\x1b[4m"
    state_str += debug_str_3 + END
    state_str += "\x1b[0m"
    # state_str += '1P|' + cfg.p1.Bar_2 + END
    state_str += '1P|' + cfg.p1.Bar_3 + END
    state_str += '1P|' + cfg.p1.Bar_4 + END

    return state_str


def situationReset():

    # 状況をリセット
    w_mem(ad.RESET_AD, b'\xff')


def pause():

    # 一時停止
    w_mem(ad.ANTEN_STOP_AD, b'\xff')


def play():

    # 再生
    w_mem(ad.ANTEN_STOP_AD, b'\x00')


def mode_check():
    para_get(cfg.game_mode)


def timer_check():
    cfg.f_timer = r_mem(ad.TIMER_AD, cfg.b_timer)


def MAX_Damage_ini():
    w_mem(ad.MAX_DAMAGE_AD, b'\x00\x00\x00\x00')


def disable_fn1():
    disable_fn1_1_AD = 0x0041F654
    disable_fn1_2_AD = 0x0041F652

    WriteMem(cfg.h_pro, disable_fn1_1_AD, b'\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90', 12, None)
    WriteMem(cfg.h_pro, disable_fn1_2_AD, b'\x90\x90', 2, None)
