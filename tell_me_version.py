import os
import re

VERSION_SCAN_DIR = r'c:\outdated_libs'

#e.g. "version 3.2.5"
pattern_tres_dot = re.compile(b"version\s\d[.]\d[.]\d[.]*")

#e.g. MISC_1.0
pattern_with_underscore = re.compile(b"[a-zA-Z0-9]*_\d[.]\d[.]{0,1}\d*")

so_files = []

#
#
#
for r, d, f in os.walk(VERSION_SCAN_DIR):
    #
    # r=root, d=directories, f = files
    #
    for file in f:
        if file.startswith("libQt"):
            continue
        if '.so' in file:
            so_files.append(os.path.join(r, file))
        else:   #or include all files no just .so
            so_files.append(os.path.join(r, file))

#
#
#
examine_file_list = []

for f in so_files:
    try:
        with open(f, 'rb') as the_file:
            s = b""
            s = the_file.read()

            # only ELF files
            if not s.startswith(b'\x7F\x45\x4C\x46'):
                continue

            r1 = re.findall(pattern_tres_dot, s)
            if len(r1):
                ver_info = f + "  " + r1[0].decode("utf-8")
                print(ver_info)
            else:
                r1 = re.findall(pattern_with_underscore, s)
                prev_ver_info = ""
                for i in range(len(r1)):
                    if len(r1[i]):
                        lib_filename = r1[i].decode("utf-8")
                        if lib_filename.startswith('GLIBC'):
                            continue
                        elif lib_filename.startswith("ARM_"):
                            continue
                        elif lib_filename.startswith("CXXABI"):
                            continue
                        elif lib_filename.startswith("GCC"):
                            continue
                        elif lib_filename.startswith("MOUNT_"):
                            continue
                        elif lib_filename.startswith("ALSA_"):
                            continue
                        elif lib_filename.startswith("ATTR"):
                            continue
                        elif lib_filename.startswith("BLKID"):
                            continue
                        elif lib_filename.startswith("MODUTIL"):
                            continue
                        # elif lib_filenme[:10]. isupper():
                        #    continue
                        else:
                            # don't print duplicates
                            ver_info = f + "  " + r1[i].decode("utf-8")
                            if ver_info == prev_ver_info:
                                continue
                            print(ver_info)
                            prev_ver_info = ver_info
    except:
        pass
