from ctypes import windll
import os
import time
import keyboard
import cfg_cc
import ad_cc
import save_cc

import sub_cc
ad = ad_cc
cfg = cfg_cc
sub = sub_cc

num_saves = 3
is_saved = [False] * num_saves
save_to_load = 0
lock_input = False


def setup():
    sub.ex_cmd_enable()
    sub.changeFontSize(7, 14)
    os.system('mode con: cols=161 lines=12')
    os.system('cls')
    os.system('title MBAACC Training')
    print('\x1b[1;1H' + '\x1b[?25l')
    windll.winmm.timeBeginPeriod(1)


def function_key():
    global num_saves
    global is_saved
    global save_to_load
    global lock_input

    if keyboard.is_pressed("F1"):
        is_saved = [False] * num_saves

    elif keyboard.is_pressed("F2") or cfg.fn1_key.num == 1 or cfg.fn1_key.num == 3:
        if not lock_input:
            sub.sitMem(cfg.save_slot)
            sub.pause()
            lock_input = True

            is_saved[cfg.save_slot] = True

    elif cfg.fn2_key.num == 1 or cfg.fn2_key.num == 3:
        if not lock_input:
            lock_input = True
            if cfg.dummy_st.num == 5 or cfg.dummy_st.num == -1:
                sub.situationReset()
    
    elif keyboard.is_pressed("F6") and is_saved[cfg.save_slot]:
        sub.situationReset()

    elif keyboard.is_pressed("F7"):
        if time.perf_counter() - cfg.last_key_time > 0.1:
            cfg.use_arrows = not cfg.use_arrows
            cfg.bar_offset = 0
            cfg.last_key_time = time.perf_counter()

    elif keyboard.is_pressed("right") and cfg.bar_offset > 0 and cfg.use_arrows:
        if time.perf_counter() - cfg.last_key_time > 0.05:
            cfg.bar_offset -= 1
            cfg.last_key_time = time.perf_counter()
    
    elif keyboard.is_pressed("left") and cfg.bar_offset < cfg.bar_num - 81 and cfg.use_arrows:
        if time.perf_counter() - cfg.last_key_time > 0.05:
            cfg.bar_offset += 1
            cfg.last_key_time = time.perf_counter()

    elif (keyboard.is_pressed(",")) and (keyboard.is_pressed(".")):
        cfg.debug_flag = not cfg.debug_flag
        os.system('cls')
        os.system(f'mode con: cols=161 lines={12 + 7 * cfg.debug_flag}')
        time.sleep(0.3)
    
    elif keyboard.is_pressed("1"):
        cfg.save_slot = 0
        save_to_load = 0

    elif keyboard.is_pressed("2"):
        cfg.save_slot = 1
        save_to_load = 1

    elif keyboard.is_pressed("3"):
        cfg.save_slot = 2
        save_to_load = 2

    elif keyboard.is_pressed("4"):
        print(save_cc.S_info[0].contl_flag.ad)
    
    elif lock_input:
        lock_input = False
        sub.play()


def main_loop():
    global num_saves
    global is_saved
    global save_to_load

    while 1:
        time.sleep(0.001)

        # MODEチェック
        sub.mode_check()

        if cfg.game_mode.num == 20:
            is_saved = [False] * num_saves

        function_key()

        # タイマーチェック
        sub.timer_check()

        # フレームの切り替わりを監視
        if cfg.f_timer != cfg.f_timer2:
            cfg.f_timer2 = cfg.f_timer
            time.sleep(0.001)

            # 各種数値の取得
            sub.situationCheck()

            if cfg.f_timer == 0:
                sub.bar_ini()

            # ゲーム状況の取得
            sub.view_st()

            if cfg.f_timer == 1:
                for i in range(0, num_saves):
                    if save_to_load == i and is_saved[i]:
                        sub.sitWrite(i)
                        sub.bar_ini()

        sub.view()


sub.get_base_address()
sub.disable_fn1()

setup()
main_loop()
