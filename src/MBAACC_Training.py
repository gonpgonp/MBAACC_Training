from ctypes import windll
from struct import unpack
import os
import time
import keyboard
import cfg_cc
import ad_cc

import sub_cc
ad = ad_cc
cfg = cfg_cc
sub = sub_cc

sub.ex_cmd_enable()
os.system('mode con: cols=164 lines=14')
os.system('cls')
os.system('title MBAACC Training')
print('\x1b[1;1H' + '\x1b[?25l')
windll.winmm.timeBeginPeriod(1)  # タイマー精度を1msec単位にする

# 変数初期化
num_saves = 4
is_saved = [0] * num_saves
save_to_load = 0
flag1 = 0
ispaused = 0
start_time = time.time()
framestep = 0
extra_save = 1
    

def function_key():

    global num_saves
    global is_saved
    global save_to_load
    global flag1
    global ispaused
    global framestep
    global extra_save
    
    # セーブデータリセット
    if keyboard.is_pressed("F1"):
        if flag1 == 0:
            is_saved = [0] * num_saves
        elif flag1 == 100:
            sub.MAX_Damage_ini()
        flag1 += 1
    # 状況記憶
    elif keyboard.is_pressed("F2") or cfg.fn1_key.num == 1 or cfg.fn1_key.num == 3:
        if flag1 == 0:
            sub.sitMem(0)
            sub.pause()

            is_saved[0] = 1
            flag1 = 1

    elif cfg.fn2_key.num == 1 or cfg.fn2_key.num == 3:
        save_to_load = 0
        ispaused = 0
        if flag1 == 0:
            flag1 = 1
            if cfg.dummy_st.num == 5 or cfg.dummy_st.num == -1:
                sub.situationReset()
            sub.w_mem(ad.COMB_AFTER_TIMER_AD, b'\xFF')
    
    elif keyboard.is_pressed("F6") and is_saved[0] == 1:
        save_to_load = 0
        sub.situationReset()
    
    elif keyboard.is_pressed("F7"):
        if flag1 == 0:
            sub.sitMem(extra_save)
            sub.pause()

            is_saved[extra_save] = 1
            flag1 = 1
    
    elif keyboard.is_pressed("F8") and is_saved[extra_save] == 1:
        save_to_load = extra_save
        sub.situationReset()

    # デバッグ表示
    elif (keyboard.is_pressed(",")) and (keyboard.is_pressed(".")):
        if cfg.debug_flag == 0:
            cfg.debug_flag = 1
            os.system('mode con: cols=164 lines=19')

        elif cfg.debug_flag == 1:
            cfg.debug_flag = 0
            os.system('mode con: cols=164 lines=14')

        time.sleep(0.3)
    
    elif (keyboard.is_pressed("1")):
        extra_save = 1

    elif (keyboard.is_pressed("2")):
        extra_save = 2

    elif (keyboard.is_pressed("3")):
        extra_save = 3
    
    elif flag1 >= 1:
        flag1 = 0
        sub.play()


###############################################################
# メイン関数
###############################################################
# 実行中のすべてのＩＤ＋プロセス名取得

# ベースアドレス取得
sub.get_base_addres()

# FN1ボタンの無効化
sub.disable_fn1()

while 1:
    time.sleep(0.003)

    # MODEチェック
    sub.mode_check()

    if cfg.game_mode.num == 20:
        save_flag = 0

    function_key()

    # タイマーチェック
    sub.timer_check()

    # フレームの切り替わりを監視
    if (cfg.f_timer != cfg.f_timer2):

        cfg.f_timer2 = cfg.f_timer
        time.sleep(0.001)

        # 各種数値の取得
        sub.situationCheck()

        # ゲーム状況の取得
        sub.view_st()

        if cfg.f_timer == 1:
            sub.bar_ini()
            
            for i in range(0, num_saves):
                if save_to_load == i and is_saved[i] == 1:
                    sub.sitWrite(i)
                #elif save_to_load == 0 and is_saved[0] == 1:
                    # 状況再現
                    #sub.sitWrite(0)
            
    sub.view(extra_save)
