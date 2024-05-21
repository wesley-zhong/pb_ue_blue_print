import cpp_generate_tmpls
import proto_parse


def generate_struct_cpp_files(pbstruct):
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
        fields += "\n\n"

    return template_code.replace("%FIELD_CODE%", fields)


def genner_cpp(template_code, pbstruct):
    from_pb_functions = ""
    to_pb_function = ""
    for attr in pbstruct.attributes:
        if attr['repeated'] is True:
            from_pb, to_pb = gener_repeated_code(attr)
            from_pb_functions += from_pb
            to_pb_function += to_pb
            continue
        from_pb_functions += gener_from_pb_attribute(attr)  # f"   {attr['name']}= pbMessage.{attr['name']}();\n"
        to_pb_function += gener_to_pb_attribute(attr)  # f"    pbMessage.set_{attr['name']}({attr['name']});\n"

    template_code = template_code.replace("%CLASS_NAME%", pbstruct.className)
    template_code = template_code.replace("%FROM_PB_FUNCTION_CODE%", from_pb_functions)
    return template_code.replace("%TO_PB_FUNCTION_CODE%", to_pb_function)


def gener_from_pb_attribute(attr):
    if attr['type'] == "FString":
        return f"   {attr['name']}=  UTF8_TO_TCHAR(pbMessage.{attr['name']}().c_str());\n"
    if attr['user_def_type'] is True:
        if proto_parse.is_enum(attr['pb_type']):
            return f"   {attr['name']}= static_cast<E{attr['pb_type']}>(pbMessage.{attr['name']}());\n"
        return f"""   if (pbMessage.has_{attr['name']}()) {{
    {attr['pb_type']} data = pbMessage.{attr['name']}();
    {attr['name']}.FromPB(data);
    }}  
"""
    # if attr['type'] == "enum":
    # return f"   {attr['name']}= static_cast<{attr['type']}>(pbMessage.{attr['name']}());\n"
    return f"   {attr['name']}= pbMessage.{attr['name']}();\n"


def gener_to_pb_attribute(attr):
    if attr['type'] == "FString":
        return f"    pbMessage.set_{attr['name']}(TCHAR_TO_UTF8(*{attr['name']}));\n"
    if attr['user_def_type'] is True:
        if proto_parse.is_enum(attr['pb_type']):
            return f"   pbMessage.set_{attr['name']}(static_cast<{attr['pb_type']}>({attr['name']}));\n"
        return f"""    {attr['pb_type']}* pb_{attr['name']} = new  {attr['pb_type']};
    {attr['name']}.ToPB(*pb_{attr['name']});
    pbMessage.set_allocated_{attr['name']}(pb_{attr['name']});
"""

    return f"    pbMessage.set_{attr['name']}({attr['name']});\n"


def gener_repeated_code(attr):
    if attr['user_def_type'] is True:
        return gener_user_type_repeated_code(attr)
    return gener_sys_type_repeated_code(attr)


def gener_sys_type_repeated_code(attr):
    from_pb = f"""
for ( auto element :pbMessage.{attr['name']}()){{
    {attr['name']}.Add(element);
}}
 """
    if attr['single_type'] == "FString":
        from_pb = f"""
  for ( auto element :pbMessage.{attr['name']}()){{
    {attr['name']}.Add(UTF8_TO_TCHAR(*element.c_str()));
  }}
"""

    to_pb = f"""
  for (auto element : {attr['name']}){{
    pbMessage.add_{attr['name']}(element);
   }}
"""
    if attr['single_type'] == "FString":
        to_pb = f"""
  for (auto element : {attr['name']}){{
    pbMessage.add_{attr['name']}(TCHAR_TO_UTF8(*element));
   }}
"""
    return from_pb, to_pb


def gener_user_type_repeated_code(attr):
    from_pb = f"""
      for ( auto element :pbMessage.{attr['name']}()){{
        {attr['single_type']} _{attr['single_type']};
        _{attr['single_type']}.FromPB(element);
        {attr['name']}.Add( _{attr['single_type']});
        }}
    """
    to_pb = f"""
      for ( auto element : {attr['name']}){{
        {attr['pb_type']}* _{attr['pb_type']}=pbMessage.add_{attr['name']}();
        element.ToPB(*_{attr['pb_type']});
        }}
    """
    return from_pb, to_pb
