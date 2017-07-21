# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
## Description
"""
Core program to exchange datas.
"""
#-------------------------------------------------------------------------------

import sys
sys.dont_write_bytecode = True

import os
import re

import hou

from . import define as Define
reload(Define)


#-------------------------------------------------------------------------------
# Core API to access to Houdini Datas
#-------------------------------------------------------------------------------
class houManager(object):
    """Core API to access to Houdini Datas
    """


    def __init__(self):
        super(houManager, self).__init__()


    @classmethod
    def getCacheList(self):
        ## Init variable
        current_cache_nodes = []
        all_nodes = hou.pwd().allSubChildren()

        for node in all_nodes:

            for item in Define.CACHE_NODES:

                node_type = item.get("name")
                rwtype    = item.get("rwtype")

                if node.type().name().lower() == node_type:

                    eachNode_dict     = {}
                    node_path         = node.path()
                    node_type         = node.type().name().lower()
                    node_cat          = node.type().category().name()
                    cache_path        = self.getUnexpandedStringPath(node_path, node_type, node_cat)
                    evalCachePath     = self.getEvalStringPath(node_path, node_type)

                    eachNode_dict["name"]           = node.name()
                    eachNode_dict["node_path"]      = node_path
                    eachNode_dict["cache_path"]     = cache_path
                    #eachNode_dict["env"]            = self.analizeValiables(cache_path)
                    eachNode_dict["expanded_path"]  = evalCachePath
                    eachNode_dict["color"]          = node.color().rgb()
                    eachNode_dict["rwtype"]         = self.setIoType(node_path, rwtype, node_cat)
                    eachNode_dict["editable"]       = self.isEditable(node_path)
                    eachNode_dict["status"]         = self.setStatus(node, node_cat)

                    current_cache_nodes.append(eachNode_dict)

        return current_cache_nodes


    @classmethod
    def getUnexpandedStringPath(self, path, node_type, node_cat):
        for item in Define.CACHE_NODES:

            if not node_cat == item.get("cat"):
                continue

            if node_type == item.get("name"):
                parmName = item.get("parmName")
                break

        try:
            parmPath = path + '/' + parmName
            unExpPath = hou.parm(parmPath).unexpandedString()
            return unExpPath

        except:
            return "Error: definition error"


    @classmethod
    def getEvalStringPath(self, path, node_type):
        try:
            for item in Define.CACHE_NODES:
                if item.get("name") == node_type:
                    parmName = item.get("parmName")

            parmPath = path + '/' + parmName
            evalPath = hou.evalParm(parmPath)

            return evalPath
        except:
            return None


    @classmethod
    def analizeValiables(self, path):
        try:
            obj = re.search("$", path)

            if obj:
                pathTokens = path.split('/')
                return "-"
            else:
                return pathTokens[0]
        except:
            return None


    @classmethod
    def isEditable(self, path):
        pathTokens = path.split("/")

        while range(len(pathTokens)):
            pathTokens.pop(-1)
            node_path = '/'.join(pathTokens)

            if pathTokens >= 2:
                try:
                    node_type = hou.node(node_path).type().name().lower()
                except:
                    return True

                for neNodes in Define.NODES_EXCEPTION:
                    if node_type == neNodes:
                        return False

                for ceNodes in Define.CHILDNODES_EXCEPTION:
                    if node_type == ceNodes:
                        return False

            else:
                return True
                break


    @classmethod
    def setStatus(self, node, node_cat):

        error  = node.errors()

        if node_cat == "Sop":
            if node.isBypassed():
                return "bypassed"

            if not error == "":
                return "error"


    @classmethod
    def setIoType(self, path, rwtype, node_cat):

        if node_cat == "Driver":
            return "write"

        if rwtype[0] == "read":
            return rwtype[0]

        elif rwtype[0] == "write":
            return rwtype[0]

        elif rwtype[0] == "both":

            parm = path + '/' + rwtype[1]
            switch = hou.evalParm(parm)

            if switch in rwtype[2]:
                return "read"

            elif switch in rwtype[3]:
                return "write"

            else:
                return "both"
