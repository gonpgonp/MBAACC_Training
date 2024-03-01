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


def get_pid():
    dict_pids = {
        p.info["name"]: p.info["pid"]
        for p in psutil.process_iter(attrs=["name", "pid"])
    }
    return dict_pids


def get_base_address():
    cfg.pid = 0
    while cfg.pid == 0:
        dict_pids = get_pid()
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


def pointer_get(obj, parent, offset):
    obj.ad = parent.num + offset
    para_get_2(obj)


def para_set(obj):
    w_mem(obj.ad, obj.b_dat)


def ex_cmd_enable():
    INVALID_HANDLE_VALUE = -1
    STD_OUTPUT_HANDLE = -11
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004

    hOut = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    if hOut == INVALID_HANDLE_VALUE:
        return False
    dwMode = wintypes.DWORD()
    if windll.kernel32.GetConsoleMode(hOut, byref(dwMode)) == 0:
        return False
    dwMode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
    if windll.kernel32.SetConsoleMode(hOut, dwMode) == 0:
        return False
    return True


def changeFontSize(size_x, size_y):  # Changes the font size to *size* pixels (kind of, but not really. You'll have to try it to chack if it works for your purpose ;) )
    from ctypes import POINTER, WinDLL, Structure, sizeof, byref
    from ctypes.wintypes import BOOL, SHORT, WCHAR, UINT, ULONG, DWORD, HANDLE

    LF_FACESIZE = 32
    STD_OUTPUT_HANDLE = -11

    class COORD(Structure):
        _fields_ = [
            ("X", SHORT),
            ("Y", SHORT),
        ]

    class CONSOLE_FONT_INFOEX(Structure):
        _fields_ = [
            ("cbSize", ULONG),
            ("nFont", DWORD),
            ("dwFontSize", COORD),
            ("FontFamily", UINT),
            ("FontWeight", UINT),
            ("FaceName", WCHAR * LF_FACESIZE),
        ]

    kernel32_dll = WinDLL("kernel32.dll")

    get_last_error_func = kernel32_dll.GetLastError
    get_last_error_func.argtypes = []
    get_last_error_func.restype = DWORD

    get_std_handle_func = kernel32_dll.GetStdHandle
    get_std_handle_func.argtypes = [DWORD]
    get_std_handle_func.restype = HANDLE

    get_current_console_font_ex_func = kernel32_dll.GetCurrentConsoleFontEx
    get_current_console_font_ex_func.argtypes = [
        HANDLE,
        BOOL,
        POINTER(CONSOLE_FONT_INFOEX),
    ]
    get_current_console_font_ex_func.restype = BOOL

    set_current_console_font_ex_func = kernel32_dll.SetCurrentConsoleFontEx
    set_current_console_font_ex_func.argtypes = [
        HANDLE,
        BOOL,
        POINTER(CONSOLE_FONT_INFOEX),
    ]
    set_current_console_font_ex_func.restype = BOOL

    stdout = get_std_handle_func(STD_OUTPUT_HANDLE)
    font = CONSOLE_FONT_INFOEX()
    font.cbSize = sizeof(CONSOLE_FONT_INFOEX)

    font.dwFontSize.X = size_x
    font.dwFontSize.Y = size_y

    set_current_console_font_ex_func(stdout, False, byref(font))

def situationCheck():
    # 状況チェック
    para_get(cfg.fn1_key)
    para_get(cfg.fn2_key)
    para_get(cfg.dummy_st)
    para_get(cfg.recording_mode)
    para_get(cfg.stop)

    for n in cfg.P_info:
        #State
        para_get(n.exist)
        para_get(n.pattern)
        para_get(n.state)
        
        #Meters
        para_get(n.health)
        para_get(n.rhealth)
        para_get_f(n.gg)
        para_get_f(n.gq)
        para_get(n.circuit)
        para_get(n.f_count)
        
        #Movement
        para_get(n.x_pos)
        para_get(n.y_pos)
        para_get(n.x_spd)
        para_get(n.y_spd)
        para_get(n.x_acc)
        para_get(n.y_acc)
        para_get(n.momentum)
        
        #Others
        para_get(n.shield_time)
        para_get(n.hitstop)
        para_get(n.step_inv)
        para_get(n.untechend)
        para_get(n.untech)
        para_get(n.hitstun)
        para_get(n.chstate)
        para_get_f(n.grav)
        para_get(n.utpen)

        #Inputs
        para_get(n.air_dinput)
        para_get(n.raw_dinput)
        para_get(n.button_input)
        para_get(n.macro_input)
        para_get(n.on_right)

        #Pointers
        para_get(n.anim_st_pointer)
        para_get(n.atk_st_pointer)
        
        #Pointer Children
        pointer_get(n.st_pointer, n.anim_st_pointer, 0x38)
        pointer_get(n.st_sac, n.st_pointer, 0xC)
        pointer_get(n.st_invuln, n.st_pointer, 0xD)
        pointer_get(n.anim_box, n.anim_st_pointer, 0x42)

        #Addresses outside of character
        para_get(n.tag_flag)
        para_get(n.anten_stop)
        para_get(n.motion)

    for o in cfg.A_info:
        #State
        para_get(o.exist)
        para_get(o.pattern)
        para_get(o.state)
        
        #Others
        para_get(o.hitstop)
        para_get(o.owner)
        
        #Pointers
        para_get(o.atk_st_pointer)

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

    save_info.active1 = cfg.p1.active
    save_info.active2 = cfg.p2.active
    save_info.active3 = cfg.p3.active
    save_info.active4 = cfg.p4.active


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

    cfg.p1.active = save_info.active1
    cfg.p2.active = save_info.active2
    cfg.p3.active = save_info.active3
    cfg.p4.active = save_info.active4


def view_st():
    advantage_calc()
    
    is_input = (cfg.p1.raw_dinput.num != 0 or cfg.p2.raw_dinput.num != 0 or
    cfg.p1.button_input.num != 0 or cfg.p2.button_input.num != 0 or
    cfg.p1.macro_input.num != 0 or cfg.p2.macro_input.num != 0)
    
    # キャラの状況推移表示
    if (cfg.p1.motion.num != 0 or cfg.p1.hitstop.num != 0 or
            cfg.p2.motion.num != 0 or cfg.p2.hitstop.num != 0 or
            cfg.p3.atk_st_pointer.num != 0 or cfg.p4.atk_st_pointer.num != 0 or
            cfg.debug_flag == 1 and is_input):
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
            if n.atk_st_pointer.num != 0 and n.last_f_count != n.f_count.num and n.hitstop.num == 0:
                n.active += 1
            elif n.atk_st_pointer.num == 0 and cfg.anten == 0 and cfg.hitstop <= 1:  # 攻撃判定を出してないとき
                n.active = 0

            if n.atk_st_pointer.num != 0 and n.active == 0:
                    n.active = 1
        
        barcheck = True
        if cfg.debug_flag == 0:
            barcheck = cfg.anten == 0 and cfg.hitstop <= 1
        
        if barcheck:
            if cfg.bar_num < cfg.mem_range - 1:
                cfg.bar_num += 1
            if cfg.bar_num == cfg.mem_range - 1:
                for m in cfg.p_info:
                    m.barlist_1 = m.barlist_1[1:] + [""]
                    m.barlist_2 = m.barlist_2[1:] + [""]
                    m.barlist_3 = m.barlist_3[1:] + [""]
                    m.barlist_4 = m.barlist_4[1:] + [""]
                    m.barlist_5 = m.barlist_5[1:] + [""]

        # バー追加処理
        bar_add()

        for n in cfg.p_info:
            n.last_f_count = n.f_count.num

def advantage_calc():
    if cfg.p1.motion.num == 0 and cfg.p2.motion.num == 0:
        cfg.adv_flag = 0

    if cfg.p1.motion.num != 0 and cfg.p2.motion.num != 0:
        cfg.adv_flag = 1
        cfg.p1_adv = 0
        cfg.p2_adv = 0

    if cfg.adv_flag == 1:
        # 有利フレーム検証
        if (cfg.p1.motion.num == 0 and cfg.p2.motion.num != 0 and
                cfg.stop.num == 0 and cfg.p1.last_f_count != cfg.p2.f_count.num):
            cfg.p1_adv += 1

        # 不利フレーム検証
        if (cfg.p1.motion.num != 0 and cfg.p2.motion.num == 0 and
                cfg.stop.num == 0 and cfg.p2.last_f_count != cfg.p2.f_count.num):
            cfg.p2_adv += 1


def determineReset():
    bar_ini_flag = 0

    if cfg.bar_num >= cfg.bar_range:
        cfg.interval_time = 20

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
    if cfg.p1.hitstop.num != 0 and cfg.p2.hitstop.num != 0:
        cfg.hitstop += 1
    elif cfg.p1.hitstop.num == 0 or cfg.p2.hitstop.num == 0:
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

    atk =           get_font((255, 255, 255), (255,   0,   0))
    partner_atk =   get_font((255, 255, 255), (255, 128,   0))
    mot =           get_font((255, 255, 255), ( 65, 200,   0))
    grd_stun =      get_font((255, 255, 255), (170, 170, 170))
    hit_stun =      get_font((255, 255, 255), (140, 140, 140))
    thrown =        get_font((255, 255, 255), (110, 110, 110))
    fre =           get_font(( 92,  92,  92), (  0,   0,   0))
    jmp =           get_font((177, 177, 177), (241, 224, 132))
    seeld =         get_font((255, 255, 255), (145, 194, 255))
    inv =           get_font((140, 140, 140), (255, 255, 255))
    adv =           get_font((255, 255, 255), (  0,   0,   0))
    bunker =        get_font((255, 255, 255), (225, 184,   0))
    a_font =        get_font((255, 143, 169), (170,  27,  58))
    b_font =        get_font((255, 255, 137), (169,  91,   7))
    c_font =        get_font((143, 255, 195), ( 18, 132,  62))
    d_font =        get_font((137, 255, 255), ( 21,  66, 161))
    freeze =        get_font((255, 255, 255), ( 60,  60,  60))
    freeze2 =       get_font((255, 255, 255), ( 120, 80, 160))
    hit_stop =      get_font((255, 255, 255), ( 60,  80, 128))

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

    jmp_number = [34, 35, 36, 37]
    
    player_num = 0
    

    for n in cfg.p_info:
        font = ""
        num = ""
        #Bar 1
        if n.motion.num != 0:
            num = str(n.motion.num)
            font = mot
            
            if n.pattern.num in jmp_number:
                font = jmp

            elif n.pattern.num in hit_number:
                font = hit_stun
                if n.st_sac.num != 1:  #grounded
                    if (n.hitstun.num - 1) > 0:
                        num = str(n.hitstun.num - 1)
                elif n.st_sac.num == 1:  #airborne
                    if (n.untechend.num - n.untech.num) > 0:
                        num = str(n.untechend.num - n.untech.num)

            elif n.pattern.num in grd_number:
                font = grd_stun
                if n.st_sac.num != 1:  #grounded
                    if (n.hitstun.num - 1) > 0:
                        num = str(n.hitstun.num - 1)
                    else:
                        num = "P" #prox guard

        elif n.motion.num == 0:
            num = str(n.pattern.num)
            font = fre

            if cfg.adv_flag == 1:
                if player_num == 0:
                    font = adv
                    num = str(cfg.p1_adv)
                elif player_num == 1:
                    font = adv
                    num = str(cfg.p2_adv)

        if n.pattern.num == 350:  # 投げやられ
            font = thrown
            num = "T"

        elif n.anim_box.num == 12:  # バンカー　or 相殺
            font = bunker

        elif n.anim_box.num == 10 and n.shield_time.num > 0:  # シールド
            font = seeld

        elif n.anim_box.num == 1 or n.anim_box.num == 0 or n.step_inv.num != 0 or n.st_invuln.num == 3:  # 無敵中
            font = inv

        if cfg.stop.num != 0 and cfg.debug_flag == 1:
            font = freeze
        elif n.hitstop.num != 0:
            font = hit_stop
        elif cfg.p1.anten_stop.num != 0 or cfg.p2.anten_stop.num != 0:
            font = freeze2

        n.barlist_1[cfg.bar_num] = font + num.rjust(2, " ")[-2:] + DEF
        font = ""
        num = ""

        #Bar 2

        if n.st_sac.num == 1:  # 空中にいる場合:
            num = "^"

        if n.atk_st_pointer.num != 0:  # 攻撃判定を出しているとき
            font = atk
            num = str(n.active)
            if n.st_sac.num == 1:  # 空中にいる場合:
                font += "\x1b[4m"
            if cfg.stop.num != 0 and cfg.debug_flag == 1:
                font = freeze
            elif n.hitstop.num != 0:
                font = hit_stop


        n.barlist_2[cfg.bar_num] = font + num.rjust(2, " ")[-2:] + DEF
        num = ""
        font = ""
        
        #Bar 3
        bar3 = ""
        button_pressed = 0
        if n.button_input.num != 0 or n.macro_input.num != 0:
            button_pressed = 1
        
        if n.macro_input.num > 0:
            num = " E"
        else:
            num = "  "
        
        if ((n.button_input.num & 16) > 0):
            font = a_font
        elif button_pressed == 1:
            font = hit_stun
        else:
            font = DEF
        bar3 += font + num[0] + DEF
        
        if ((n.button_input.num & 32) > 0):
            font = b_font
        elif button_pressed == 1:
            font = hit_stun
        else:
            font = DEF
        bar3 += font + num[1] + DEF
        n.barlist_3[cfg.bar_num] = bar3

        #Bar 4
        bar4 = ""
        rev_input = [0, 3, 2, 1, 6, 0, 4, 9, 8, 7]
        if n.st_sac.num == 1:
            num = n.air_dinput.num
        elif n.on_right.num == 1:
            num = rev_input[n.raw_dinput.num]
        else:
            num = n.raw_dinput.num
        
        if num == 0:
            num = " ·"
        else:
            num = f" {num}"
        
        if (n.button_input.num & 64) > 0:
            font = c_font
        elif button_pressed == 1:
            font = hit_stun
        else:
            font = DEF
        
        side_switch = ""
        if (n.on_right.num != n.last_on_right) and cfg.bar_num > 1:
            side_switch = "\x1b[4m"
        
        bar4 += font + side_switch + num[0] + DEF
        
        if (n.button_input.num & 128) > 0:
            font = d_font
        elif button_pressed == 1:
            font = hit_stun
        else:
            font = DEF
        bar4 += font + side_switch + num[1] + DEF
        n.barlist_4[cfg.bar_num] = bar4
        
        n.last_on_right = n.on_right.num
        num = ""
        font = ""
        
        #Bar5
        
        count = 0
        
        for o in cfg.A_info:
            if o.owner.num == player_num and o.atk_st_pointer.num != 0 and o.exist.num == 1 and o.pattern.num not in range(0, 10):
                font = atk
                count += 1
                if cfg.stop.num != 0 and cfg.debug_flag == 1:
                    font = freeze
                elif o.hitstop.num != 0:
                    font = hit_stop
        
        if count > 0:
            num = str(count)
        else:
            num = ""
        
        if player_num < 2: #get partner attack
            if cfg.p_info[player_num + 2].atk_st_pointer.num != 0:
                font = partner_atk
                num = str(cfg.p_info[player_num + 2].active)
        
        n.barlist_5[cfg.bar_num] = font + num.rjust(2, " ")[-2:] + DEF
        num = ""
        font = ""
        
        player_num += 1


def bar_ini():

    cfg.reset_flag = 1

    for n in cfg.p_info:
        n.Bar_1 = ""
        n.Bar_2 = ""
        n.Bar_3 = ""
        n.Bar_4 = ""
        n.Bar_5 = ""

    cfg.bar_num = 0
    cfg.interval = 0
    cfg.bar_ini_flag2 = 0
    cfg.interval_time = cfg.bar_range
    cfg.bar_offset = 0

    for m in cfg.p_info:
        m.barlist_1 = [""] * cfg.mem_range
        m.barlist_2 = [""] * cfg.mem_range
        m.barlist_3 = [""] * cfg.mem_range
        m.barlist_4 = [""] * cfg.mem_range
        m.barlist_5 = [""] * cfg.mem_range


def view():
    END = '\x1b[0m' + '\x1b[49m' + '\x1b[K' + '\x1b[1E'
    CLEAR = '\x1b[0m' + '\x1b[K'
    
    column_headers = "\x1b[4m"
    for i in range(1, cfg.bar_range+1):
        if i % 10 != 0:
            column_headers += f"\x1b[0;4m {i%10}"
        else:
            column_headers += f"\x1b[4;48;5;238m{i%100:2}"
    
    x_p1 = cfg.p1.x_pos.num
    x_p2 = cfg.p2.x_pos.num
    xp_p1 = math.floor(cfg.p1.x_pos.num/128)
    xp_p2 = math.floor(cfg.p2.x_pos.num/128)
    
    xspd_p1_math = cfg.p1.x_spd.num
    xspd_p2_math = cfg.p2.x_spd.num
    xacc_p1 = cfg.p1.x_acc.num
    xacc_p2 = cfg.p2.x_acc.num
    
    momentum_p1_math = cfg.p1.momentum.num
    momentum_p2_math = cfg.p2.momentum.num
    xspdfinal_p1 = momentum_p1_math + xspd_p1_math
    xspdfinal_p2 = momentum_p2_math + xspd_p2_math

    y_p1 = cfg.p1.y_pos.num
    y_p2 = cfg.p2.y_pos.num
    yp_p1 = math.floor(cfg.p1.y_pos.num/128)
    yp_p2 = math.floor(cfg.p2.y_pos.num/128)
    
    yspd_p1 = cfg.p1.y_spd.num
    yspd_p2 = cfg.p2.y_spd.num
    yacc_p1 = cfg.p1.y_acc.num
    yacc_p2 = cfg.p2.y_acc.num
    
    pat1 = cfg.p1.pattern.num
    st1 = cfg.p1.state.num
    pat2 = cfg.p2.pattern.num
    st2 = cfg.p2.state.num

    health_p1 = cfg.p1.health.num
    health_p2 = cfg.p2.health.num
    
    circuit_p1 = cfg.p1.circuit.num
    circuit_p2 = cfg.p2.circuit.num

    dx = abs(cfg.p1.x_pos.num - cfg.p2.x_pos.num)
    dpx = abs(math.floor(cfg.p1.x_pos.num/128) - math.floor(cfg.p2.x_pos.num/128))
    dy = abs(cfg.p1.y_pos.num - cfg.p2.y_pos.num)
    dpy = abs(math.floor(cfg.p1.y_pos.num/128) - math.floor(cfg.p2.y_pos.num/128))

    for n in cfg.p_info:
        n.Bar_1 = ""
        n.Bar_2 = ""
        n.Bar_3 = ""
        n.Bar_4 = ""
        n.Bar_5 = ""

    if cfg.bar_num < cfg.bar_range:
        start = 0
    else:
        start = cfg.bar_num - (cfg.bar_range - 1) - cfg.bar_offset
    
    r = range(start, start + cfg.bar_range)

    for n in r:
        for m in cfg.p_info:
            m.Bar_1 += m.barlist_1[n]
            m.Bar_2 += m.barlist_2[n]
            m.Bar_3 += m.barlist_3[n]
            m.Bar_4 += m.barlist_4[n]
            m.Bar_5 += m.barlist_5[n]

    font1 = "\x1b[0m"
    font2 = "\x1b[7m"
    font3 = "\x1b[48;5;242m"

    f1 = '\x1b[7m[F1]reset\x1b[27m' if keyboard.is_pressed("F1") else '[F1]reset'
    f2 = f'\x1b[7m[F2]save {cfg.save_slot+1}\x1b[27m ' if keyboard.is_pressed("F2") else f'[F2]save {cfg.save_slot+1} '
    f6 = f'\x1b[7m[F6]load {cfg.save_slot+1}\x1b[27m' if keyboard.is_pressed("F6") else f'[F6]load {cfg.save_slot+1}'

    p1_info = '\x1b[?25l'
    p2_info = '\x1b[?25l'
    ex_info = '\x1b[?25l'

    state_str = '\x1b[1;1H' + '\x1b[?25l'

    p1_info += f'{font1}({x_p1:6}, {y_p1:6})' if cfg.bar_range >= 8 else ''
    p1_info += f'{font2}({xp_p1:4}, {yp_p1:4})' if cfg.bar_range >= 14 else ''
    p1_info += f'{font1}pat {pat1:3} [{st1:2}]' if cfg.bar_range >= 20 else ''
    p1_info += f'{font2}x-spd {xspdfinal_p1:5}' if cfg.bar_range >= 26 else ''
    p1_info += f'{font1}x-acc {xacc_p1:5}' if cfg.bar_range >= 31 else ''
    p1_info += f'{font2}y-spd {yspd_p1:5}' if cfg.bar_range >= 37 else ''
    p1_info += f'{font1}y-acc {yacc_p1:5}' if cfg.bar_range >= 42 else ''
    p1_info += f'{font2}hp {health_p1:5}' if cfg.bar_range >= 46 else ''
    p1_info += f'{font1}mc {circuit_p1:5}' if cfg.bar_range >= 50 else ''
    p1_info += f'   {font3}{f1} {f2} {f6}' if cfg.bar_range >= 68 else ''

    debughotkeys = '\x1b[7m[F7]extra\x1b[27m' if keyboard.is_pressed("F7") else '[F7]extra'

    p2_info += f'{font1}({x_p2:6}, {y_p2:6})' if cfg.bar_range >= 8 else ''
    p2_info += f'{font2}({xp_p2:4}, {yp_p2:4})' if cfg.bar_range >= 14 else ''
    p2_info += f'{font1}pat {pat2:3} [{st2:2}]' if cfg.bar_range >= 20 else ''
    p2_info += f'{font2}x-spd {xspdfinal_p2:5}' if cfg.bar_range >= 26 else ''
    p2_info += f'{font1}x-acc {xacc_p2:5}' if cfg.bar_range >= 31 else ''
    p2_info += f'{font2}y-spd {yspd_p2:5}' if cfg.bar_range >= 37 else ''
    p2_info += f'{font1}y-acc {yacc_p2:5}' if cfg.bar_range >= 42 else ''
    p2_info += f'{font2}hp {health_p2:5}' if cfg.bar_range >= 46 else ''
    p2_info += f'{font1}mc {circuit_p2:5}' if cfg.bar_range >= 50 else ''
    p2_info += f'   {font3}{debughotkeys}' if cfg.bar_range >= 68 else ''

    ex_info += f'({dx:6}, {dy:6})' if cfg.bar_range >= 8 else ''
    ex_info += f'{font2}({dpx:4}, {dpy:4})' if cfg.bar_range >= 14 else ''


    state_str += p1_info + END
    state_str += p2_info + END
    state_str += ex_info + END
    state_str += column_headers + END
    state_str += cfg.p1.Bar_1 + END
    state_str += cfg.p1.Bar_2 + END
    state_str += cfg.p1.Bar_5 + END
    state_str += cfg.p2.Bar_1 + END
    state_str += cfg.p2.Bar_2 + END
    state_str += cfg.p2.Bar_5 + CLEAR

    if cfg.debug_flag == 1:
        state_str += END + debug_view()
        
    print(state_str)


def debug_view():
    END = '\x1b[0m' + '\x1b[49m' + '\x1b[K' + '\x1b[1E'
    CLEAR = '\x1b[0m' + '\x1b[K'

    column_headers = "\x1b[4m"
    for i in range(1, cfg.bar_range+1):
        if i % 10 != 0:
            column_headers += f"\x1b[0;4m {i%10}"
        else:
            column_headers += f"\x1b[4;48;5;238m{i%100:2}"

    debug_str_3 = column_headers

    exflash_p1 = cfg.p1.anten_stop.num if cfg.p1.anten_stop.num > 0 else cfg.stop.num
    exflash_p2 = cfg.p2.anten_stop.num if cfg.p2.anten_stop.num > 0 else cfg.stop.num

    ch_map = [" ", "H", "L"]

    ch_p1 = ch_map[cfg.p1.chstate.num]
    ch_p2 = ch_map[cfg.p2.chstate.num]
    
    gg_p1 = round(cfg.p1.gg.num)
    gg_p2 = round(cfg.p2.gg.num)
    gq_p1 = round(cfg.p1.gq.num, 3)
    gq_p2 = round(cfg.p2.gq.num, 3)
    
    rhealth_p1 = cfg.p1.rhealth.num-cfg.p1.health.num
    rhealth_p2 = cfg.p2.rhealth.num-cfg.p2.health.num
    
    gravity_p1 = cfg.p1.grav.num
    gravity_p1 = max(0, round((gravity_p1 - 0.072) / 0.008))
    gravity_p1 -= math.floor(gravity_p1/60)
    gravity_p1 = math.ceil(gravity_p1/6)
    
    extra_grav_p1 = cfg.p1.utpen.num

    grav_hits_p1 = round(cfg.p1.grav.num / 0.008)
    
    gravity_p2 = cfg.p2.grav.num
    gravity_p2 = max(0, round((gravity_p2 - 0.072) / 0.008))
    gravity_p2 -= math.floor(gravity_p2/60)
    gravity_p2 = math.ceil(gravity_p2/6)
    
    extra_grav_p2 = cfg.p2.utpen.num

    grav_hits_p2 = round(cfg.p2.grav.num / 0.008)

    partner_mot_p1 = cfg.p3.pattern.num
    partner_pf_p1 = cfg.p3.state.num
    
    partner_mot_p2 = cfg.p4.pattern.num
    partner_pf_p2 = cfg.p4.state.num

    font1 = "\x1b[0m"
    font2 = "\x1b[7m"
    
    debug_str_p1 = f"ex {exflash_p1:3}" if cfg.bar_range >= 3 else ''
    debug_str_p1 += f"{font2}ch {ch_p1}" if cfg.bar_range >= 5 else ''
    debug_str_p1 += f"{font1}gg {gg_p1:5} [{gq_p1:.3f}]" if cfg.bar_range >= 13 else ''
    debug_str_p1 += f"{font2}rhp {rhealth_p1:5}" if cfg.bar_range >= 18 else ''
    debug_str_p1 += f"{font1}scaling {grav_hits_p1:2} [{gravity_p1:2},{extra_grav_p1:2}]" if cfg.bar_range >= 27 else ''
    debug_str_p1 += f"{font2}partner {partner_mot_p1:3} [{partner_pf_p1:2}]" if cfg.bar_range >= 35 else ''

    debug_str_p2 = f"ex {exflash_p2:3}" if cfg.bar_range >= 3 else ''
    debug_str_p2 += f"{font2}ch {ch_p2}" if cfg.bar_range >= 5 else ''
    debug_str_p2 += f"{font1}gg {gg_p2:5} [{gq_p2:.3f}]" if cfg.bar_range >= 13 else ''
    debug_str_p2 += f"{font2}rhp {rhealth_p2:5}" if cfg.bar_range >= 18 else ''
    debug_str_p2 += f"{font1}scaling {grav_hits_p2:2} [{gravity_p2:2},{extra_grav_p2:2}]" if cfg.bar_range >= 27 else ''
    debug_str_p2 += f"{font2}partner {partner_mot_p2:3} [{partner_pf_p2:2}]" if cfg.bar_range >= 35 else ''

    state_str = ""
    state_str += debug_str_p1 + END
    state_str += debug_str_p2 + END
    state_str += "\x1b[4m"
    state_str += debug_str_3 + END
    state_str += "\x1b[0m"

    state_str += cfg.p1.Bar_3 + END
    state_str += cfg.p1.Bar_4 + END
    state_str += cfg.p2.Bar_3 + END
    state_str += cfg.p2.Bar_4 + CLEAR
    

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
