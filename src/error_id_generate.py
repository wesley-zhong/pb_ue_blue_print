import cpp_generate_tmpls


def generate_msg_id_body_cpp_files(pbstruct):
    cpp_tmpls = cpp_generate_tmpls.get_tmp(cpp_generate_tmpls.ProtoMsgType.ERROR_ID)
    return genner_h(cpp_tmpls.h, pbstruct), None


def genner_h(template_code, pbstruct):
    headers = ""
    template_code = template_code.replace("%ALL_HEADERS_FIELD_CODE%", headers)
    template_code = template_code.replace("%CLASS_NAME%", pbstruct.className)
    msg_id_res_body_map = ""
    enum_name_value = ""
    for attr in pbstruct.attributes:
        enum_name_value += f"UPROPERTY(BlueprintReadOnly)\n"
        enum_name_value += f"int {attr['name']} ={attr['value']};\n"
        if msg_id_res_body_map != "":
            msg_id_res_body_map += f"\n"

        msg_id_res_body_map += f" {{{attr['name']}, \"{attr['comment']}\" }},"
        if attr['comment'] != "":
            msg_id_res_body_map += f"//{attr['comment']}"
        msg_id_res_body_map += "\n"

    template_code = template_code.replace("%MSG_ID_BODY_FIELD_CODE%", msg_id_res_body_map)
    return template_code.replace("%E_MSG_ID_BODY_FIELD_CODE%", enum_name_value)
