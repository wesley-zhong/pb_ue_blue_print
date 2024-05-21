import os
from enum import Enum


class ProtoMsgType(Enum):
    ENUM = 1
    STRUCT = 2
    REQ = 3
    RES = 4
    RES_DATA = 5
    NTF = 6
    NTF_DATA = 7
    MSG_ID_BODY = 8
    ERROR_ID = 9


templs = {}


def load_tmpl(directPath):
    filenames = os.listdir(directPath)
    for fileName in filenames:
        if fileName.endswith(".tmpl"):
            file_path = os.path.join(directPath, fileName)
            with open(file_path, 'r', encoding='UTF-8') as f:
                content = f.read()
                if fileName.startswith('enum_UE.tmpl'):
                    check_create_tmp(ProtoMsgType.ENUM).h = content
                if fileName.startswith('enum_UE_engine'):
                    check_create_tmp(ProtoMsgType.ENUM).engine = content

                if fileName.startswith("req_UE_h"):
                    check_create_tmp(ProtoMsgType.REQ).h = content
                if fileName.startswith("req_UE_cpp"):
                    check_create_tmp(ProtoMsgType.REQ).cpp = content

                if fileName.startswith("res_UE_h"):
                    check_create_tmp(ProtoMsgType.RES).h = content
                if fileName.startswith("res_UE_cpp"):
                    check_create_tmp(ProtoMsgType.RES).cpp = content

                if fileName.startswith("res_data_UE_cpp"):
                    check_create_tmp(ProtoMsgType.RES_DATA).cpp = content
                if fileName.startswith("res_data_UE_h"):
                    check_create_tmp(ProtoMsgType.RES_DATA).h = content

                if fileName.startswith("struct_UE_h"):
                    check_create_tmp(ProtoMsgType.STRUCT).h = content
                if fileName.startswith("struct_UE_cpp"):
                    check_create_tmp(ProtoMsgType.STRUCT).cpp = content
                if fileName.startswith("struct_UE_engine"):
                    check_create_tmp(ProtoMsgType.STRUCT).engine = content

                if fileName.startswith("ntf_UE_h"):
                    check_create_tmp(ProtoMsgType.NTF).h = content
                if fileName.startswith("ntf_UE_cpp"):
                    check_create_tmp(ProtoMsgType.NTF).cpp = content

                if fileName.startswith("ntf_data_UE_cpp"):
                    check_create_tmp(ProtoMsgType.NTF_DATA).cpp = content
                if fileName.startswith("ntf_data_UE_h"):
                    check_create_tmp(ProtoMsgType.NTF_DATA).h = content

                if fileName.startswith("msg_id_body_gen_UE_h"):
                    check_create_tmp(ProtoMsgType.MSG_ID_BODY).h = content
                if fileName.startswith("msg_id_body_gen_UE_cpp"):
                    check_create_tmp(ProtoMsgType.MSG_ID_BODY).cpp = content

                if fileName.startswith("error_id_gen_UE_h"):
                    check_create_tmp(ProtoMsgType.ERROR_ID).h = content
                if fileName.startswith("error_id_gen_UE_cpp"):
                    check_create_tmp(ProtoMsgType.ERROR_ID).cpp = content


class PbCppTmpl:
    def __init__(self):
        self.cpp = None
        self.h = None
        self.engine = None

    def set_h(self, h):
        self.h = h

    def set_cpp(self, cpp):
        self.cpp = cpp


def check_create_tmp(file_type):
    tmpl = templs.get(file_type)
    if tmpl is None:
        templs[file_type] = tmpl = PbCppTmpl()
    return tmpl


def get_enum_tmpl(first_des, pb_msg):
    if first_des == 'enum':
        return templs[ProtoMsgType.ENUM]


def get_tmp(pb_type):
    return templs[pb_type]
