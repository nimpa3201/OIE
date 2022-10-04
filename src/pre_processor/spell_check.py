from .hanspell import spell_checker


def get_process_field(root):
    process_field = []
    for child in root.iter("ProcessField"):
        for i in child:
            process_field.append(i.attrib.get("name"))
    return process_field

def hanspell(field,text):
    for doc in text:
        for key in field:
            pre_doc=doc[key]    
            pre_doc_bin = [i+"." for i in list(filter(None, pre_doc.replace(".","^").split("^")))]
            pre_doc_list=[""]
            spell_out=""
 
            for i in pre_doc_bin:
    
                if len(pre_doc_list[-1]) + len(i) < 500:
                    pre_doc_list[-1] += i
                else:
                    pre_doc_list.append(i)  

            for x in pre_doc_list:
                result = spell_checker.check(x)
                spell_out +=result.checked
                doc[key] = spell_out
    return text

def spell_main(root,text):
    process_field = get_process_field(root)
    return hanspell(process_field,text)

