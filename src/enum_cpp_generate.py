from jinja2 import Environment

import cpp_generate_tmpls


def generate_enum_cpp_files(pbstruct):
    cpp_tmpls = cpp_generate_tmpls.get_tmp(pbstruct.struct_type)
    return genner_h(cpp_tmpls.h, pbstruct, cpp_tmpls.engine), None


def genner_h(template_code, pbstruct, engine):
    # template_code = template_code.replace("%CLASS_NAME%", pbstruct.className)
    # fields = ""
    # for attr in pbstruct.attributes:
    #     if fields != "":
    #         fields += f"\n"
    #     fields += f"   {attr['name']} = {attr['value']},"
    #     if attr['comment'] != "":
    #         fields += f"//{attr["comment"]}"
    #
    # h = template_code.replace("%FIELD_CODE%", fields)
    # if engine is None:
    #     return h
    env = Environment()
    template = env.from_string(engine)
    render_code = template.render(pb_message=pbstruct)
    return "\n" + render_code
