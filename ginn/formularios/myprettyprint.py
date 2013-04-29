#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Basado en:
http://www.jjinno.com/2011/04/13/pretty-print-for-python-dictlisttuple/
"""

#import sys
 
def newline():
    return "\n"
    #sys.stdout.write('\n')
    #sys.stdout.flush()
 
def __type_quote(this):
    if type(this) == type(1): return str(this)
    else: return "'"+str(this)+"'"
 
def __has_children(parent):
    answer = False
    valid = [type([1,2]), type((1,2)), type({1:2})]
    if type(parent) == type([1,2]):
        for each in parent:
            if type(each) in valid: answer = True
    elif type(parent) == type((1,2)):
        answer = __has_children(list(parent))
    elif type(parent) == type({1:2}):
        for (clave, value) in parent.items():  # @UnusedVariable
            if type(value) in valid: answer = True
    return answer
 
def __print_list(lista, n=0, shrink=False, opener="[", closer="]"):
    s = ""
    assert type(lista) == type([])
    sp = "".join([" "]*n)
    valid = [type([1,2]), type((1,2)), type({1:2})]
 
    # find the max index (for spacing of the format string)
    size = len(lista)
    fstring = "%s  %-"+str(size)+"s: "
 
    # start printing stuff
    s += opener
    #sys.stdout.write(opener)
    #sys.stdout.flush()
    lista.sort()
    for index in range(len(lista)):
        s += newline()
        s += fstring % (sp, index)
        #sys.stdout.write(fstring%(sp, index))
        #sys.stdout.flush()
        this = lista[index]
        if not __has_children(this) and type(this) in valid:
            if type(this) == type([1,2]) and len(this) > 10 and shrink == True:
                s += "['%s', ... ,'%s']" % (this[0], this[-1])
                #sys.stdout.write("['%s', ... ,'%s']"%(this[0], this[-1]))
                #sys.stdout.flush()
            else:
                s += str(this)
                #sys.stdout.write(str(this))
                #sys.stdout.flush()
        elif type(this) == type([1,2]): __print_list(this, n+4+size)
        elif type(this) == type({1:2}): __print_dict(this, n+4+size)
        elif type(this) == type((1,2)): __print_tuple(this, n+4+size)
        else:
            s += str(this)
            #sys.stdout.write(str(this))
            #sys.stdout.flush()
    if len(lista) > 0:
        s += newline()
        s += "%s%s" % (sp, closer)
        #sys.stdout.write("%s%s"%(sp, closer))
    else: 
        s += "%s" % closer
        #sys.stdout.write("%s"%closer)
    #sys.stdout.flush()
    return s
 
def __print_dict(dicc, n=0, shrink=False):
    s = ""
    assert type(dicc) == type({1:2})
    sp = "".join([" "]*n)
    valid = [type([1,2]), type((1,2)), type({1:2})]
 
    # find the max key-size (for spacing of the format string)
    size = 0
    for key in dicc.keys():
        if len(str(key)) > size: size = len(str(key))
    fstring = "%s  %-"+str(size)+"s: "
 
    # start printing stuff
    s += "{"
    #sys.stdout.write("{")
    #sys.stdout.flush()
    keys = dicc.keys()
    keys.sort()
    for key in keys:
        s += newline()
        s += fstring % (sp, key)
        #sys.stdout.write(fstring%(sp, key))
        #sys.stdout.flush()
        this = dicc[key]
        if not __has_children(this) and type(this) in valid:
            if type(this) == type([1,2]) and len(this) > 10 and shrink == True:
                s += "[%s, ... ,%s]" % (__type_quote(this[0]),
                                        __type_quote(this[-1]))
                #sys.stdout.write("[%s, ... ,%s]"%(__type_quote(this[0]),
                #                                  __type_quote(this[-1])))
                #sys.stdout.flush()
            else:
                s += str(this)
                #sys.stdout.write(str(this))
                #sys.stdout.flush()
        elif type(this) == type([1,2]): __print_list(this, n+4+size)
        elif type(this) == type({1:2}): __print_dict(this, n+4+size)
        elif type(this) == type((1,2)): __print_tuple(this, n+4+size)
        else:
            s += __type_quote(this)
            #sys.stdout.write(__type_quote(this))
            #sys.stdout.flush()
    if len(dicc.keys()) > 0:
        s += newline()
        s += "%s}" % sp
        #sys.stdout.write("%s}"%sp)
    else: 
        s += "}"
        #sys.stdout.write("}")
    #sys.stdout.flush()
    return s
 
def __print_tuple(tup, n=0, shrink=False):
    assert type(tup) == type((1,2))
    return __print_list(list(tup), n, shrink, opener="(", closer=")")
 
def print_dict(d):
    s = __print_dict(d, shrink=True)
    s += newline()
    return s
 
def print_list(l):
    s = __print_list(l, shrink=True)
    s += newline()
    return s
 
def print_tuple(t):
    s = __print_tuple(t, shrink=True)
    s += newline()
    return s

