import os
import sys

import cpp_generate_tmpls
import proto_parse

IGNORE_FILES = {"BinServer", "inner"}


def ignored(file_name):
    for ignored_file in IGNORE_FILES:
        lower_file_name = file_name.lower()
        if lower_file_name.find(ignored_file.lower()) != -1:
            return True
    return False


if __name__ == "__main__":
    print("#####################  cur windows", os.getcwd())
    proto_dir = "../proto/"
    gen_cpp_dir = "../cpp/"
    tmpl_direct_path = "../tmpls/"
    if len(sys.argv) < 4:
        print("argv proto not enough", sys.argv)
    else:
        proto_dir = sys.argv[1]
        print("protoc dir =", proto_dir)
        tmpl_direct_path = sys.argv[2]
        print("tmp_direct_patch=", tmpl_direct_path)
        gen_cpp_dir = sys.argv[3]
        print("gen_cpp_dir =", gen_cpp_dir)

    cpp_generate_tmpls.load_tmpl(tmpl_direct_path)
    filenames = os.listdir(proto_dir)

    inner_file_name = "inner"
    for fileName in filenames:
        if ignored(fileName) is True:
            print("----------------ignored file = ", fileName)
            continue
        if fileName.endswith('.proto'):
            proto_parse.parse_proto_file_content(proto_dir, fileName)

    proto_parse.gener_ue_cpp_files(gen_cpp_dir)

# sys.stdin.readline()
