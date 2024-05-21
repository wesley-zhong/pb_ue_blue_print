import proto_parse
import cpp_generate_tmpls


def generate_push_data_cpp_file(pbstruct):
    cpp_tmpls = cpp_generate_tmpls.get_tmp(cpp_generate_tmpls.ProtoMsgType.RES_DATA)
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
    unpack_pb_functions = ""
    for attr in pbstruct.attributes:
        if attr['repeated'] is True:
            unpack_pb_functions += gener_repeated_code(attr)
            continue
        unpack_pb_functions += gener_from_pb_attribute(attr)  # f"   {attr['name']}= pbMessage.{attr['name']}();\n"

    template_code = template_code.replace("%CLASS_NAME%", pbstruct.className)
    return template_code.replace("%UnPack_FUNCTION_CODE%", unpack_pb_functions)


def gener_from_pb_attribute(attr):
    if attr['type'] == "FString":
        return f"   {attr['name']} = UTF8_TO_TCHAR(pbMessage.{attr['name']}().c_str());\n"
    if attr['user_def_type'] is True:
        if proto_parse.is_enum(attr['pb_type']):
            return f"   {attr['name']}= static_cast<E{attr['pb_type']}>(pbMessage.{attr['name']}());\n"
        return f"""   if (pbMessage.has_{attr['name']}()) {{
    {attr['pb_type']} data = pbMessage.{attr['name']}();
    {attr['name']}.FromPB(data);
    }}  
"""
    return f"   {attr['name']}= pbMessage.{attr['name']}();\n"


def gener_to_pb_attribute(attr):
    if attr['type'] == "FString":
        return f"    pbMessage.set_{attr['name']}(TCHAR_TO_UTF8(*{attr['name']}));\n"
    if attr['user_def_type'] is True:
        if proto_parse.is_enum(attr['pb_type']):
            return f"   pbMessage.set_{attr['name']}(static_cast<{attr['pb_type']}>({attr['name']}));\n"
        return f"""    {attr['pb_type']}* element = new  {attr['pb_type']};
    {attr['name']}.ToPB(*element);
    pbMessage.set_allocated_{attr['name']}(element);
"""
    return f"    pbMessage.set_{attr['name']}({attr['name']});\n"


def gener_repeated_code(attr):
    if attr['user_def_type'] is True:
        return gener_user_type_repeated_code(attr)
    return gener_sys_type_repeated_code(attr)


def gener_sys_type_repeated_code(attr):
    un_pack = f"""
for ( auto element :pbMessage.{attr['name']}()){{
    {attr['name']}.Add(element);
}}
 """
    if attr['single_type'] == "FString":
        un_pack = f"""
  for ( auto element :pbMessage.{attr['name']}()){{
    {attr['name']}.Add(UTF8_TO_TCHAR(*element->c_str()));
  }}
"""
    return un_pack


def gener_user_type_repeated_code(attr):
    un_pack = f"""
   for ( auto element :pbMessage.{attr['name']}()){{
    {attr['single_type']} _{attr['pb_type']};
    _{attr['pb_type']}.FromPB(element);
    {attr['name']}.Add( _{attr['pb_type']});
    }}
    """
    return un_pack
