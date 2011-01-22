from types import FunctionType
import re
import traceback

MAIN_TMPL = "<dl>%s</dl>"
ITEM_TMPL = "<dt>%s</dt><dd class='test_%s'><pre>%s</pre></dd>"

def runTest(func):
    try:
        func()
    except:
        return "FAIL<br>" + "".join(map(lambda(x): "%s<br/>" % (x,), traceback.format_exc().splitlines()))


def runTestsFromModule(mod):
    funcname_re = re.compile("^test_.+$")
    items_html = ""
    for f in filter(lambda(x): type(getattr(mod, x)) == FunctionType, 
            filter(lambda(x): funcname_re.match(x) != None, mod.__dict__)):
        ret = runTest(getattr(mod, f))
        if ret == None:
            items_html += ITEM_TMPL % (f, 'success', 'success')
        else:
            items_html += ITEM_TMPL % (f, 'failure', ret)
    return MAIN_TMPL % (items_html,)



