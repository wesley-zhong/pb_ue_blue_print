import cpp_generate_tmpls
import proto_parse


def generate_req_cpp_file(pbstruct):
    cpp_tmpls = cpp_generate_tmpls.get_tmp(pbstruct.struct_type)
    return genner_h(cpp_tmpls.h, pbstruct), genner_cpp(cpp_tmpls.cpp, pbstruct)


def genner_h(template_code, pbstruct):
    template_code = template_code.replace("%CLASS_NAME%", pbstruct.className)
    fields = ""
    for attr in pbstruct.attributes:
        fields += f"\n  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Example, Meta = (ExposeOnSpawn = true))"
        fields += f"\n  {attr['type']}  {attr['name']};"
        if attr['comment'] != "":
            fields += f" //{attr['comment']}"

    return template_code.replace("%FIELD_CODE%", fields)


def genner_cpp(template_code, pbstruct):
    template_code = template_code.replace("%CLASS_NAME%", pbstruct.className)
    pack_function = f"    {pbstruct.className} pbMessage;\n"
    cmd = proto_parse.MSG_ID_STRUCT_MAP.get(pbstruct.className)
    if cmd is None:
        print("Error:XXXXXXX structure: [---", pbstruct.className, "---] not found msgId")
        cmd = -1

    cmd_function = f"   return {cmd};\n"
    for attr in pbstruct.attributes:
        pack_function += gen_pack_attr(attr)  # f"    pbMessage.set_{attr['name']}({attr['name']});\n"

    pack_function += f"    mMessage = &pbMessage;\n    URequest::Pack();"

    template_code = template_code.replace("%PACK_FUNCTION_CODE%", pack_function)
    template_code = template_code.replace("%GET_CMD_FUNCTION_CODE%", cmd_function)
    return template_code


def gen_pack_attr(attr):
    if attr['repeated'] is True:
        if attr['user_def_type'] is True:
            return gen_user_type_loop_pack_attr(attr)
        else:
            return gen_sys_type_loop_pack_attr(attr)
    else:
        if attr['user_def_type'] is True:
            return gen_user_type_pack_attr(attr)
        else:
            return gen_sys_type_pack_attr(attr)


def gen_user_type_loop_pack_attr(attr):
    return f"""
    for (auto element : {attr['name']}) {{
       {attr['pb_type']}* bp_{attr['name']} = new  {attr['pb_type']};\n
       {attr['name']}.ToPB(* bp_{attr['name']});\n
  
        pbMessage.add_{attr['name']}(element);
    }}
"""


def gen_sys_type_loop_pack_attr(attr):
    return f"""
    for (auto element : {attr['name']}) {{
        pbMessage.add_{attr['name']}(element);
    }}
"""


def gen_user_type_pack_attr(attr):
    if proto_parse.is_enum(attr['pb_type']):
        return f"    pbMessage.set_{attr['name']}(static_cast<{attr['pb_type']}>({attr['name']}));\n"

    return f"""
     {attr['pb_type']}* pb_{attr['name']} = new  {attr['pb_type']};\n
     {attr['name']}.ToPB(*pb_{attr['name']});\n
      pbMessage.set_allocated_{attr['name']}(pb_{attr['name']});
"""


def gen_sys_type_pack_attr(attr):
    if attr['type'] == "FString":
        return f"    pbMessage.set_{attr['name']}(TCHAR_TO_UTF8(*{attr['name']}));\n"
    return f"    pbMessage.set_{attr['name']}({attr['name']});\n"
