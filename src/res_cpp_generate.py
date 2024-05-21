import cpp_generate_tmpls


def generate_resp_cpp_file(pbstruct):
    cpp_tmpls = cpp_generate_tmpls.get_tmp(pbstruct.struct_type)
    return genner_h(cpp_tmpls.h, pbstruct), genner_cpp(cpp_tmpls.cpp, pbstruct)


def genner_h(template_code, pbstruct):
    template_code = template_code.replace("%CLASS_NAME%", pbstruct.className)
    fields = ""
    return template_code.replace("%FIELD_CODE%", fields)


def genner_cpp(template_code, pbstruct):
    return template_code.replace("%CLASS_NAME%", pbstruct.className)
