import logging
import platform
import os
from functools import wraps
import datetime
import socket
import json
import time
import traceback
import threading


def exception_no_self_decorator(func):
    @wraps(func)
    def modified_func(*args, **kwargs):

        try:
            func_name = func.__name__

            got_log = True

            try:
                logger = logging.getLogger(func_name)
            except:
                got_log = False
                print('In exception_decorator for ' + str(func_name) +
                      '. Could not get log - print error!')

            try:
                return func(*args, **kwargs)
            except Exception as e:
                if got_log:
                    logger.critical('\n\n\n')
                    logger.critical(
                        'Exception decorator -- Critical error in ' + str(func_name))
                    logger.critical(e)
                    logger.critical(traceback.format_exc())
                    logger.critical('\n\n\n')
                else:
                    print('\n\n\n')
                    print('Exception decorator -- Critical error in ' +
                          str(func_name))
                    print(e)
                    print(traceback.format_exc())
                    print('\n\n\n')

        except Exception as e:
            try:
                print('Exception decorator -- Critical error in ' + str(func_name))
            except:
                print('Error with exception decorator - cannot print func_name')
            print(e)
            print(traceback.format_exc())

    return modified_func


@exception_no_self_decorator
def update_proxy_stats(gcp_serv, proxy_dict, loop_times_manager, logger, connection_type):

    # connection_type = one of proxy_error, proxy_attempt, proxy_complete
    prox = proxy_dict[gcp_serv]['externalIP']
    if prox not in loop_times_manager[connection_type]:
        loop_times_manager[connection_type][prox] = 1
    else:
        loop_times_manager[connection_type][prox] += 1


def timing_decorator(func):
    @wraps(func)
    def modified_func(*args, **kwargs):
        func_name = func.__name__
        logger = logging.getLogger(func_name)
        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        logger.info('Timing decorator -- Elapse time of ' + func_name + ' = ' +
                    str(format((end - start), '.2f')) + ' (sec), ' +
                    str(format(((end - start) / 60), '.2f')) + ' (min).')
        return value

    return modified_func


def exception_decorator(func):
    @wraps(func)
    def modified_func(self, *args, **kwargs):

        try:
            func_name = func.__name__

            got_log = True

            try:
                logger = logging.getLogger(func_name)
            except:
                got_log = False
                print('In exception_decorator for ' + str(func_name) +
                      '. Could not get log - print error!')

            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                if got_log:
                    logger.critical(
                        'Exception decorator -- Critical error in ' + str(func_name))
                    logger.critical(e)
                    logger.critical(traceback.format_exc())
                    logger.critical('')
                else:
                    print('Exception decorator -- Critical error in ' +
                          str(func_name))
                    print(e)
                    print(traceback.format_exc())
                    print('')

                try:
                    self.success = False

                    try:
                        logger.critical(
                            'Exception decorator -- Launching end_algo')
                    except:
                        print('Exception decorator -- Launching end_algo')

                    self.end_algo()

                except Exception as e:
                    if got_log:
                        logger.critical(
                            'Exception decorator -- Failed to kill algo')
                        logger.critical(e)
                        logger.critical(traceback.format_exc())
                        logger.critical('')
                    else:
                        print('Exception decorator -- Failed to kill algo')
                        print(e)
                        print(traceback.format_exc())
                        print('')

        except Exception as e:
            try:
                print('Exception decorator -- Critical error in ' + str(func_name))
            except:
                print('Error with exception decorator - cannot print func_name')
            print(e)
            print(traceback.format_exc())

    return modified_func


def func_start_message_decorator(func):
    @wraps(func)
    def modified_func(*args, **kwargs):
        func_name = func.__name__
        logger = logging.getLogger(func_name)
        logger.info('Start message decorator -- Starting ' + func_name + '!!')
        return func(*args, **kwargs)

    return modified_func


def func_status_message_decorator(func):
    @wraps(func)
    def modified_func(*args, **kwargs):
        func_name = func.__name__
        logger = logging.getLogger(func_name)
        logger.info('        Starting ' + func_name +
                    '!!  (From status message decorator)')
        value = func(*args, **kwargs)
        logger = logging.getLogger(func_name)
        logger.info('\n                     Finished ' +
                    func_name + '!!  (From status message decorator)\n')
        return value

    return modified_func


@exception_decorator
def print_or_log(input_str, logger=None, logger_type='info', q=None):
    if logger is not None:
        if logger_type == 'debug':
            logger.debug(input_str)
        elif logger_type == 'info':
            logger.info(input_str)
        elif logger_type == 'error':
            logger.error(input_str)
        elif logger_type == 'warning':
            logger.warning(input_str)
        elif logger_type == 'critical':
            logger.critical(input_str)
        else:
            logger.critical('should not be here reading queue')
    elif logger is None and q is None:
        print(input_str)

    if q is not None:
        q.put([logger_type, input_str])


@exception_decorator
def create_file_path_str(drive, folder_name, create_or_pull, os_platform=platform.system(), logger=None, user='dan'):
    # create_or_pull == 'create' OR 'pull'

    if os_platform == 'Windows':
        result_path = drive + ':/' + folder_name + '/'
    elif os_platform == 'Linux':
        result_path = '/home/' + user + '/' + folder_name + '/'
    else:
        result_path = None
        print_or_log('Error creating OS specific load paths.  Current OS: ' + os_platform, logger=logger,
                     logger_type='critical')

    result_path = os.path.join(result_path)

    if not os.path.exists(result_path) and create_or_pull == 'create':
        print_or_log(result_path + ' doesnt exist - create.', logger=logger)

        if os_platform == 'Linux':
            os.makedirs(result_path, mode=0o0777)
            shutil.chown(result_path, user='nobody', group='nogroup')
            os.system('chmod 777 -R ' + result_path)
    elif not os.path.exists(result_path) and create_or_pull == 'pull':
        print_or_log(result_path + ' doesnt exist to pull from!!',
                     logger=logger, logger_type='critical')
    elif os.path.exists(result_path) and create_or_pull == 'create':
        print_or_log(
            result_path + ' already exists -- dont need to create.', logger=logger)

    return result_path


@exception_decorator
def just_check_if_exists(full_path, logger=None, logger_type='debug', q=None):
    # include file extension for individual files! e.g., '.csv'
    path_str = os.path.join(full_path)

    if os.path.exists(path_str):
        print_or_log(path_str + ' exists!', logger,
                     logger_type=logger_type, q=q)
        return False
    else:
        print_or_log(path_str + ' does not exist',
                     logger, logger_type=logger_type, q=q)
        return True


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 8786))
    temp_ip1 = s.getsockname()[0]
    return temp_ip1


def list_options_q(question, options):

    try:
        list_of_options = {}
        for i, item in enumerate(options):
            list_of_options[i] = item

        temp_str = ''
        for key in list_of_options:
            temp_str = temp_str + '\n' + \
                str(key) + ': ' + str(list_of_options[key])

        entered_num = int(input("\n\n" + question + " " + temp_str + '\n'))
        print("You entered: " + str(list_of_options[entered_num]))
        return entered_num, list_of_options[entered_num]
    except KeyboardInterrupt:
        print('Caught ctrl + C!!  Exiting!')
    except:
        print('\nIncorrect key -- try again\n')
        return list_options_q(question, options)


def get_list_of_ip(pre_select=None):
    save_path_drive = 'D'

    if pre_select != 'self':
        if platform.system() == 'Linux':
            file_path = 'dask_mount/worker_lists/'
        else:
            file_path = 'dask_distributed_results/worker_lists/'

        file_path = create_file_path_str(save_path_drive, file_path, 'pull')

        files = os.listdir(file_path)
        files = files + ['self']

        if platform.system() == 'Linux':
            entered_num, selected_list = list_options_q(
                'Enter server group to use:', files)
        else:
            entered_num = 0
            selected_list = 'init'

        if selected_list != 'self':
            server_group = files[int(entered_num)]

            with open(file_path + server_group, 'r') as f:
                # f.readlines()  # will append in the list out
                out = [l.strip() for l in f]

            with open(file_path + 'worker_names.txt', 'r') as f:
                # f.readlines()  # will append in the list out
                name_list = [l.strip() for l in f]

            name_list_dict = {}
            for item in name_list:
                part = item.partition(':')
                ip = part[0]
                name = part[-1]
                name_list_dict[ip] = name

            list_of_ip = []
            txt_str = ''
            for item in out:
                if 'gcp' not in selected_list:
                    full_ip = '192.168.0.' + str(item)
                    txt_str = txt_str + full_ip + ' -- ' + \
                        name_list_dict[str(item)] + '\n'
                else:
                    full_ip = str(item)
                    txt_str = txt_str + full_ip + ' -- ' + str(item) + '\n'
                list_of_ip.append([full_ip])
        else:
            list_of_ip = [[get_local_ip()]]
            txt_str = 'Self selected -- IP = ' + str(list_of_ip) + '\n'
    else:
        list_of_ip = [[get_local_ip()]]
        txt_str = 'Self selected -- IP = ' + str(list_of_ip) + '\n'

    print('\nServer group to use:')
    # for item in list_of_ip:
    #    print(item)
    print(txt_str)
    print('\nNumber of servers in server group:')
    print(len(list_of_ip))

    return list_of_ip


@exception_no_self_decorator
def check_if_alive(target_dict, func_name, logger, logger_type='info', only_if_dead=False):

    something_is_alive = False
    alive_arry = []
    dead_arry = []
    for th_item in target_dict:
        try:
            if target_dict[th_item].is_alive():
                something_is_alive = True
                alive_arry.append(th_item)
            else:
                dead_arry.append(th_item)
                logger.debug(func_name + ' - ' + th_item + ' is dead!')
        except Exception as e:
            logger.critical(func_name + ' - something_is_alive error for ' +
                            th_item + '.  e = ' + str(e))
            logger.critical(traceback.format_exc())

    if only_if_dead:
        if len(dead_arry) > 0:
            logger_type = 'warning'
        else:
            logger_type = 'debug'

    print_or_log(func_name + ' - check_if_alive -- alive threads = ' + str(alive_arry) +
                 ' ---- dead threads = ' + str(dead_arry),
                 logger, logger_type=logger_type)

    return something_is_alive


@exception_no_self_decorator
#@timing_decorator
def thread_tracking(thread_list, allow_stragglers=True, max_time=300, straggler_count=-1, loop_pause_time=1,
                    logger=None, arry_type='list', use_desc=False, descript=None, logger_type='info'):

    start = time.time()
    number_of_threads = len(thread_list)
    original_number = number_of_threads

    elapse_time_str = 'init'

    count = 0
    elapse_time = 0

    early_break = False

    while number_of_threads > 0:
        current = time.time()

        temp_number_of_threads = 0

        active_items = []

        if arry_type == 'list':
            for t in thread_list:
                if t.isAlive():
                    temp_number_of_threads += 1
        else:
            for key in thread_list:
                if thread_list[key].isAlive():
                    temp_number_of_threads += 1
                    active_items.append(key)

        number_of_threads = temp_number_of_threads

        completed = original_number - number_of_threads

        if number_of_threads > 0:
            if count % 50 == 0:
                elapse_time = current - start
                elapse_time_str = str(format(elapse_time / 60, '.2f'))

                time_before_break = str(
                    format((max_time - elapse_time) / 60, '.2f'))

                temp_txt1 = 'Number of threads launched = ' + str(original_number) + \
                    '. Threads complete = ' + str(completed) + \
                    '. Number of threads alive = ' + str(number_of_threads) + \
                    '. Thread tracking elapsed time (min) = ' + elapse_time_str + \
                    '. Time before break (min) = ' + time_before_break
                temp_txt2 = 'Active items = ' + str(active_items)

                if not use_desc:
                    print_or_log(temp_txt1, logger=logger,
                                 logger_type=logger_type)
                    print_or_log(temp_txt2, logger=logger,
                                 logger_type=logger_type)
                else:
                    print_or_log(descript + ' -- ' + temp_txt1,
                                 logger=logger, logger_type=logger_type)
                    print_or_log(descript + ' -- ' + temp_txt2,
                                 logger=logger, logger_type=logger_type)

        if allow_stragglers:
            if number_of_threads < straggler_count:
                temp_txt = 'Breaking thread_tracking - number_of_threads < straggler_count = ' + \
                           str(number_of_threads) + \
                    ' < ' + str(straggler_count)
                print_or_log(temp_txt, logger=logger, logger_type=logger_type)
                early_break = True
                break
            elif max_time > 0 and float(elapse_time) > max_time:
                temp_txt = 'Breaking thread_tracking - been hanging too long' + \
                           '. Elapsed time so far (min) = ' + elapse_time_str + \
                           '. number_of_threads = ' + str(number_of_threads)
                print_or_log(temp_txt, logger=logger, logger_type=logger_type)
                early_break = True
                break
        time.sleep(loop_pause_time)
        count += 1
    if not early_break:
        temp_txt = 'Exiting thread_tracking - number_of_threads = ' + \
            str(number_of_threads)
        print_or_log(temp_txt, logger=logger, logger_type=logger_type)


def sleep_message_loop(time_to_sleep, message_interval=1, message=None, logger=None):
    sleep_loop_cnt = 0
    while sleep_loop_cnt < time_to_sleep:
        sleep_loop_cnt += 1
        if sleep_loop_cnt % message_interval == 0:
            print_or_log(message + ' Time to go = ' + str(time_to_sleep - sleep_loop_cnt) + ' (sec).',
                         logger, logger_type='info')
        time.sleep(1)


if __name__ == "__main__":
    placeholder = 0
