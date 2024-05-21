import cpp_generate_tmpls
import enum_cpp_generate
import error_id_generate
import msg_id_body_generate
import ntf_cpp_generate
import ntf_data_generate
import req_cpp_generate
import res_cpp_generate
import res_data_cpp
import structure_cpp_generate

gener_file_functions = {
    cpp_generate_tmpls.ProtoMsgType.ENUM.value: enum_cpp_generate.generate_enum_cpp_files,
    cpp_generate_tmpls.ProtoMsgType.STRUCT.value: structure_cpp_generate.generate_struct_cpp_files,
    cpp_generate_tmpls.ProtoMsgType.REQ.value: req_cpp_generate.generate_req_cpp_file,
    cpp_generate_tmpls.ProtoMsgType.RES.value: res_cpp_generate.generate_resp_cpp_file,
    cpp_generate_tmpls.ProtoMsgType.RES_DATA.value: res_data_cpp.generate_resp_cpp_file,
    cpp_generate_tmpls.ProtoMsgType.NTF.value: ntf_cpp_generate.generate_push_cpp_file,
    cpp_generate_tmpls.ProtoMsgType.NTF_DATA.value: ntf_data_generate.generate_push_data_cpp_file,
    cpp_generate_tmpls.ProtoMsgType.MSG_ID_BODY.value: msg_id_body_generate.generate_msg_id_body_cpp_files,
    cpp_generate_tmpls.ProtoMsgType.ERROR_ID.value: error_id_generate.generate_msg_id_body_cpp_files,
}


def generate_ue_blue_print_file(gen_cpp_dir, cpp_file_name, pbstructs, pb_imports):
    gen_hpp_file_name = gen_cpp_dir + cpp_file_name + "_UE.h"
    gen_cpp_file_name = gen_cpp_dir + cpp_file_name + "_UE.cpp"
    hpp_file = open(gen_hpp_file_name, 'w', encoding="utf-8")
    cpp_file = open(gen_cpp_file_name, 'w', encoding="utf-8")
    print("###############  start create c++ file:", gen_hpp_file_name, gen_cpp_file_name)
    write_h_file_header(hpp_file, cpp_file_name, pb_imports)
    write_cpp_file_header(cpp_file, cpp_file_name)
    for pbstruct in pbstructs:
        if pbstruct.className == "MsgId":
            genner_func = gener_file_functions.get(cpp_generate_tmpls.ProtoMsgType.MSG_ID_BODY.value)
            gener_code(hpp_file, cpp_file, genner_func, pbstruct)
            continue
        if pbstruct.className == "ErrCode":
            genner_func = gener_file_functions.get(cpp_generate_tmpls.ProtoMsgType.ERROR_ID.value)
            gener_code(hpp_file, cpp_file, genner_func, pbstruct)
            continue

        if pbstruct.struct_type == cpp_generate_tmpls.ProtoMsgType.RES:
            genner_func = gener_file_functions.get(cpp_generate_tmpls.ProtoMsgType.RES_DATA.value)
            gener_code(hpp_file, cpp_file, genner_func, pbstruct)
        if pbstruct.struct_type == cpp_generate_tmpls.ProtoMsgType.NTF:
            genner_func = gener_file_functions.get(cpp_generate_tmpls.ProtoMsgType.NTF_DATA.value)
            gener_code(hpp_file, cpp_file, genner_func, pbstruct)

        genner_func = gener_file_functions.get(pbstruct.struct_type.value)
        gener_code(hpp_file, cpp_file, genner_func, pbstruct)


def gener_code(hpp_file, cpp_file, call_func, pbstruct):
    h_content, cpp_content = call_func(pbstruct)
    if h_content is not None:
        hpp_file.write(h_content)
    if cpp_content is not None:
        cpp_file.write(cpp_content)


def write_h_file_header(hpp_file, cpp_file_name, pb_imports):
    header = f"""// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: {cpp_file_name}.proto
#pragma once
#include "../Service/APIProtocol.h"
#include "{cpp_file_name}.pb.h"
"""
    for include_file in pb_imports:
        header += f"#include \"{include_file}.pb.h \"\n"
        header += f"#include \"{include_file}_UE.h \"\n"
    if cpp_file_name != "ProtoMsgId":
        header += f"#include \"{cpp_file_name}_UE.generated.h\"\n"
    hpp_file.write(header)


def write_cpp_file_header(cpp_file, cpp_file_name):
    header = f"""// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: {cpp_file_name}.proto
#include "{cpp_file_name}_UE.h"
    """
    if cpp_file_name != "ProtoMsgId" and cpp_file_name != "ProtoErrorCode":
        header += f"#include \"ProtoMsgId_UE.h\"\n"
    cpp_file.write(header)
