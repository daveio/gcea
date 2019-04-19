"""GCEA"""

import pprint
import time
import os
import putiopy   # type: ignore
import colorama  # type: ignore


def read_config(filename):
    """read the config file and return a dict"""
    try:
        with open(filename, 'r') as conf_file:
            lines = conf_file.readlines()
            return dict([[token.strip() for token in line.split("=")]
                         for line in lines])
    except FileNotFoundError:
        print(
            "{0} not found. copy gcea.conf.example to {0}, edit, and retry"
            .format(filename)
        )
        exit(1)


def find_files(client, rdir_id=None):
    """Flatten a directory tree and return a list of files"""
    filelist = []
    if rdir_id is not None:
        root = client.File.list(rdir_id)
    else:
        root = client.File.list()
    dirs = []
    dirs = list(filter(lambda x: x.content_type == 'application/x-directory',
                       root))
    # files = []
    videos = list(filter(lambda x: x.content_type.startswith("video/"), root))
    for fdir in dirs:
        filelist.extend(find_files(client, fdir.id))
    filelist.extend(videos)
    return flatten(filelist)


def flatten(this_list):
    """Flatten nested lists inside a list"""
    values = []
    for entry in this_list:
        if isinstance(list, entry):
            return flatten(entry)
        # else
        values.append(entry)
    return values


def cli():
    """CLI entry point"""
    fore = colorama.Fore
    # bg = colorama.Back
    style = colorama.Style
    colorama.init()
    cfg = read_config("{0}/.gcea.conf".format(os.environ['HOME']))
    client = putiopy.Client(cfg['token'])
    vids = find_files(client)
    vids_pending = list(filter(lambda x: not x.is_mp4_available, vids))
    msg = "{0}Report{1}".format(fore.CYAN, style.RESET_ALL)
    print("               {0} | {1} videos total, {2} videos to consider"
          .format(msg, len(vids), len(vids_pending)))
    time.sleep(1)
    for vid in vids_pending:
        try:
            exception_occurred = False
            vid.convert_to_mp4()
        except putiopy.ClientError as err:
            exception_occurred = True
            if err.type == 'MAX_PENDING_CONVERSIONS':
                msg = "{0}Queue full{1}".format(fore.RED, style.RESET_ALL)
                print("           {0} | {1}{2}{3}".format(msg,
                                                          style.DIM,
                                                          vid.name,
                                                          style.RESET_ALL))
                exit(1)
            elif err.type == 'ConversionNotNeeded':
                msg = "{0}Conversion not needed{1}".format(fore.MAGENTA,
                                                           style.RESET_ALL)
                print("{0} | {1}".format(msg, vid.name))
            elif err.type == 'NotVideo':
                msg = "{0}File is not a video{1}".format(fore.MAGENTA,
                                                         style.RESET_ALL)
                print("  {0} | {1}".format(msg, vid.name))
            else:
                pprint.pprint(err)
        finally:
            if not exception_occurred:
                msg = "{0}Conversion started{1}".format(fore.GREEN,
                                                        style.RESET_ALL)
                print("   {0} | {1}".format(msg, vid.name))
    exit(0)
