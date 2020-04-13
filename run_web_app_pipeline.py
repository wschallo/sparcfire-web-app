#import python libraries:
import os
import time
from shutil import copyfile

#import main function from web_app:
from run_web_app import main

#import unzip:
from unzip import unzip

#import time profiling:
from time_profile import get_current_string_time, get_current_epoch, get_average_time
#contants:
OUTPUT_DIR = "D:\\Galaxies\\sparcfire_web_app\\sparcfire_web_app_output_dir"
OUTPUT_FILE = "D:\\Galaxies\\sparcfire_web_app\\run_web_app_output.txt"

#helper functions:
def _list_gals_in_dir(the_dir):
    '''list galaxies in nested galaxy structure'''
    return [o for o in os.listdir(the_dir) if os.path.isdir(os.path.join(the_dir,o))]

def _make_dir_if_does_not_exist(folder):
    '''create dir if does not exist'''
    if not os.path.exists(folder):
        os.makedirs(folder)

def _get_zip_file_paths_in_dir(folder):
    '''find paths to zip files'''
    zip_file_paths = []
    for file_path in os.listdir(folder):
        if file_path.endswith(".zip"):
            zip_file_paths.append(os.path.join(folder, file_path))
    return zip_file_paths

def _get_galaxy_name_and_band_string(zip_path):
    '''get galaxy_name outputted by sparcfire (note not same as galaxy name)'''
    return zip_path.strip().split("\\")[-1].split(".")[0]

def _is_correct_csv_file(file_name,galaxy_name):
    '''check if the csv file is the right kind of csv file'''
    to_parse = file_name.strip().split("_")
    return len(to_parse) == 2 and galaxy_name in to_parse[0]

def _get_csv_file_path(extracted_to_path,galaxy_name):
    '''get csv file paths'''
    to_return = dict()
    for file_path in os.listdir(extracted_to_path):
        if file_path.endswith(".csv"):
            if _is_correct_csv_file(file_path,galaxy_name):
                to_return.update({file_path:os.path.join(extracted_to_path,file_path)})
    return to_return
                

def _unzip_files(unzip_file_list,directory_to_extract_to,galaxy_name):
    '''unzip all zip files in list and find location of csv files'''
    file_to_copy = dict()
    for each_zip in unzip_file_list:
        extract_gal_to = os.path.join(directory_to_extract_to,_get_galaxy_name_and_band_string(each_zip))
        _make_dir_if_does_not_exist(extract_gal_to)
        unzip(each_zip,extract_gal_to)
        file_name_to_file_path_dict = _get_csv_file_path(extract_gal_to,galaxy_name)
        file_to_copy.update(file_name_to_file_path_dict)
    return file_to_copy

def _copy_files(file_name_to_file_path_dict,folder_of_nested_galaxies,galaxy_name):
    '''copy csv files'''
    for each_file_name in file_name_to_file_path_dict:
        original_location = file_name_to_file_path_dict[each_file_name]
        new_location = os.path.join(folder_of_nested_galaxies,galaxy_name,each_file_name)
        copyfile(original_location, new_location)

def _print_start_string(galaxy_name,completed,total,task_completition_times):
    avg = get_average_time(task_completition_times)
    left = total - completed

    if avg < 0:
        eta_task = "unknown"
        eta_overall = "unknown"
    else:
        eta_task = "{} s".format(get_average_time(task_completition_times))
        eta_overall = "{} s".format(left * get_average_time(task_completition_times))

    print("Running on: {}/{} {} (eta={}, eta_left={})".format(completed+1,total,galaxy_name,eta_task,eta_overall))
    
#functions:
def pipeline(folder_of_nested_galaxies):
    '''run SpArcFiRe webapp on galaxies in nested folder, unzip files, and copy csv to input'''
    #1) get list of directories:
    list_of_galaxies = _list_gals_in_dir(folder_of_nested_galaxies)

    task_completition_times = []
    completed = 0
    total = len(list_of_galaxies)

    #2) run on each directory individually:
    for each_gal in list_of_galaxies:
        
        _print_start_string(each_gal,completed,total,task_completition_times)
        start_epoch = get_current_epoch()
        
        #)2.1 get input output path for specific galaxy:
        path_to_gal = os.path.join(folder_of_nested_galaxies, each_gal)
        path_to_output = os.path.join(OUTPUT_DIR,each_gal)

        #)2.2 create output dir. if needed:
        _make_dir_if_does_not_exist(path_to_output)

        #)2.3 Run SpArcFiRe web-app on all wavebands for a galaxy:
        main(path_to_gal,path_to_output,OUTPUT_FILE)

        #)2.4 locate all zip files in output directory:
        zip_file_paths = _get_zip_file_paths_in_dir(path_to_output)

        #2.5 find all csv file to copy:
        file_names_to_file_paths_to_copy = _unzip_files(zip_file_paths,path_to_output,each_gal)

        #2.6 copy csv files:
        _copy_files(file_names_to_file_paths_to_copy,folder_of_nested_galaxies,each_gal)
        end_epoch = get_current_epoch()

        task_completition_times.append(end_epoch-start_epoch)
        completed+=1

if __name__ == "__main__":
    FOLDER_OF_NESTED_GALAXIES = 'D:\\Galaxies\\spin_parity_input_galaxies'
    pipeline(FOLDER_OF_NESTED_GALAXIES)
