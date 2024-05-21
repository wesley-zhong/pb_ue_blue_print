import os

import consts as Const
import cpp_generate_tmpls
import generator
import utils

ignore_keys = {"syntax", "option", "//", "import"}
pb_to_cpp = {"string": "FString",
             "int32": "int32",
             "int": "int",
             "int8": "int8",
             "uint32": "int64",
             "int64": "int64",
             "float": "float",
             "double": "double",
             "bool": "bool",
             "enum": "enum"}
All_Pb_enum_Types = set()
ALL_PB_FILES = {}
MSG_ID_STRUCT_MAP = {}


def parse_proto_file_content(direct_path, filename):
    file_path = os.path.join(direct_path, filename)
    print("====================== start parse file:", filename)
    pb_structs = []
    pb_imports = []
    filename = filename[:-6]
    pb_file = PBFile(filename, pb_structs, pb_imports)
    ALL_PB_FILES[filename] = pb_file

    with open(file_path, 'r', encoding='UTF-8') as f:
        content = f.readlines()
        for line in content:
            line = line.strip()
            if line.startswith("import"):
                parser_file_imports(line, pb_file)
                continue
            processed_line = check_create_pb_struct(line, pb_structs)
            if processed_line is None:
                continue
            process_pb_line(processed_line, pb_structs)

    # record all enum types
    for pbstruct in pb_structs:
        if pbstruct.struct_type == cpp_generate_tmpls.ProtoMsgType.ENUM:
            All_Pb_enum_Types.add(pbstruct.className)


def parser_file_imports(str_imports, pb_file):
    str_imports = str_imports.replace("import", '')
    str_imports = str_imports.replace("\"", '')
    str_imports = str_imports.strip()
    str_imports = str_imports.split(".")[0]
    pb_file.pb_imports.append(str_imports)
    return


# 重新改写 type EType or FType  and create msgId to structure map
def reset_e_or_f_cpp_type():
    for filename, proto_file in ALL_PB_FILES.items():
        for pbstruct in proto_file.pb_structs:
            for attr in pbstruct.attributes:
                if attr.get(Const.USER_DEF_TYPE) is True:
                    if attr[Const.UE_TYPE] in All_Pb_enum_Types:
                        attr[Const.UE_TYPE] = "E" + attr[Const.UE_TYPE]
                    else:
                        attr[Const.UE_TYPE] = "F" + attr[Const.UE_TYPE]
                    attr[Const.SINGLE_TYPE] = attr[Const.UE_TYPE]
                if attr.get(Const.REPEATED) is True:
                    attr[Const.UE_TYPE] = "TArray<" + attr[Const.UE_TYPE] + ">"
               # re_order_class(pbstruct)


# def re_order_class(pbstruct):
#     for i, attr in enumerate(pbstruct.attributes):
#     # if attr.get(Const.USER_DEF_TYPE) is True:
#
#     return


def gener_ue_cpp_files(gen_cpp_dir):
    reset_e_or_f_cpp_type()
    for filename, proto_file in ALL_PB_FILES.items():
        generator.generate_ue_blue_print_file(gen_cpp_dir, filename, proto_file.pb_structs, proto_file.pb_imports)


def is_enum(user_type):
    if user_type in All_Pb_enum_Types:
        return True
    return False


def check_create_pb_struct(line, pb_structs):
    line = pre_process(line)
    if ignored(line):
        return None
    if line.startswith(Const.ENUM):
        liness = line.split()
        struct_name = liness[1]
        cur_global_struct = PBStruct(struct_name, cpp_generate_tmpls.ProtoMsgType.ENUM)
        pb_structs.append(cur_global_struct)
        return None
    if line.startswith(Const.MESSAGE):
        liness = line.split()
        struct_name = liness[1]
        if struct_name.lower().endswith(Const.REQ):
            cur_global_struct = PBStruct(struct_name, cpp_generate_tmpls.ProtoMsgType.REQ)
        elif struct_name.lower().endswith(Const.RES) or struct_name.lower().endswith("resp"):
            cur_global_struct = PBStruct(struct_name, cpp_generate_tmpls.ProtoMsgType.RES)
        elif struct_name.lower().endswith(Const.NTF) or struct_name.lower().endswith("push"):
            cur_global_struct = PBStruct(struct_name, cpp_generate_tmpls.ProtoMsgType.NTF)
        else:
            cur_global_struct = PBStruct(struct_name, cpp_generate_tmpls.ProtoMsgType.STRUCT)
        pb_structs.append(cur_global_struct)
        return None
    if line.endswith("}"):
        return None
    return line


def pre_process(line):
    line = line.replace("\r", "")
    line = line.replace("\n", "")
    line = line.replace(";", "")
    line = line.replace("{", "")
    stripped = line.strip()
    return stripped


def ignored(line):
    if len(line) <= 3:
        return True
    for key_word in ignore_keys:
        if line.startswith(key_word):
            return True
    return False


def process_pb_line(line, pb_structs):
    if len(line) < 3:
        print("XXXXXXXXXXXXXXXXXXX  error", line)
        return
    if len(pb_structs) == 0:
        print("eXXXXXXXXXXXXXXXXX  line = ", line)
    pb_struct = pb_structs[len(pb_structs) - 1]
    pb_struct.add_attribute(line)


class PBFile:
    def __init__(self, name, pb_structs, imports):
        self.name = name
        self.pb_structs = pb_structs
        self.pb_imports = imports


class PBStruct:
    def __init__(self, name, struct_type):
        self.className = name
        self.struct_type = struct_type
        self.attributes = []

    def add_attribute(self, pb_line):
        try:
            if self.struct_type == cpp_generate_tmpls.ProtoMsgType.ENUM:
                self.add_enum_atrribute(pb_line)
                return
            # repeated string new_name = 1; // 新的昵称
            pb_line_array = pb_line.split("=")
            type_name = pb_line_array[0]
            type_name_array = type_name.split()
            field_type = type_name_array[0]
            field_name = type_name_array[1]
            repeated = False
            # field_name_comments = type_name_array[1]
            user_defined_type = False
            if field_type == "repeated":
                repeated = True
                field_type = type_name_array[1]
                field_name = type_name_array[2]
            cpp_type = pb_to_cpp.get(field_type)
            if cpp_type is None:
                cpp_type = field_type
                user_defined_type = True
            pb_type = cpp_type
            single_type = cpp_type
            field_name_comments_array = pb_line_array[1].split("//")
            comments = ""
            if len(field_name_comments_array) > 1:
                comments = field_name_comments_array[1]

            field_name = field_name.lower()
            self.attributes.append(
                {Const.NAME: field_name, Const.UE_TYPE: cpp_type, Const.REPEATED: repeated,
                 Const.SINGLE_TYPE: single_type,
                 Const.PB_TYPE: pb_type, Const.USER_DEF_TYPE: user_defined_type, Const.COMMENT: comments})
        except IndexError as e:
            print("XXXXXXXXXXXXXXXXXX class_name= ", self.className, "parse failed = ", pb_line)
            print("Error:", e.message)

    def add_enum_atrribute(self, pb_line):
        type_name_comments_array = pb_line.split("//")
        type_name_array = type_name_comments_array[0].split("=")
        comments = ""
        name = type_name_array[0]
        value = type_name_array[1]
        if len(type_name_comments_array) > 1:
            comments = type_name_comments_array[1]
        self.attributes.append({Const.NAME: name, Const.VALUE: value, Const.COMMENT: comments})
        if self.className == "MsgId":
            class_name = utils.parser_body_class_by_comment(comments,'req')
            if class_name is not None:
                MSG_ID_STRUCT_MAP[class_name] = name
