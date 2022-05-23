
import sys
import toolutils

outputitem = None
inputindex = -1
inputitem = None
outputindex = -1

num_args = 1
h_extra_args = ''
pane = toolutils.activePane(kwargs)
if not isinstance(pane, hou.NetworkEditor):
    pane = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    if pane is None:
       hou.ui.displayMessage(
               'Cannot create node: cannot find any network pane')
       sys.exit(0)
else: # We're creating this tool from the TAB menu inside a network editor
    pane_node = pane.pwd()
    if "outputnodename" in kwargs and "inputindex" in kwargs:
        outputitem = pane_node.item(kwargs["outputnodename"])
        inputindex = kwargs["inputindex"]
        h_extra_args += 'set arg4 = "' + kwargs["outputnodename"] + '"\n'
        h_extra_args += 'set arg5 = "' + str(inputindex) + '"\n'
        num_args = 6
    if "inputnodename" in kwargs and "outputindex" in kwargs:
        inputitem = pane_node.item(kwargs["inputnodename"])
        outputindex = kwargs["outputindex"]
        h_extra_args += 'set arg6 = "' + kwargs["inputnodename"] + '"\n'
        h_extra_args += 'set arg9 = "' + str(outputindex) + '"\n'
        num_args = 9
    if "autoplace" in kwargs:
        autoplace = kwargs["autoplace"]
    else:
        autoplace = False
    # If shift-clicked we want to auto append to the current
    # node
    if "shiftclick" in kwargs and kwargs["shiftclick"]:
        if inputitem is None:
            inputitem = pane.currentNode()
            outputindex = 0
    if "nodepositionx" in kwargs and             "nodepositiony" in kwargs:
        try:
            pos = [ float( kwargs["nodepositionx"] ),
                    float( kwargs["nodepositiony"] )]
        except:
            pos = None
    else:
        pos = None

    if not autoplace and not pane.listMode():
        if pos is not None:
            pass
        elif outputitem is None:
            pos = pane.selectPosition(inputitem, outputindex, None, -1)
        else:
            pos = pane.selectPosition(inputitem, outputindex,
                                      outputitem, inputindex)

    if pos is not None:
        if "node_bbox" in kwargs:
            size = kwargs["node_bbox"]
            pos[0] -= size[0] / 2
            pos[1] -= size[1] / 2
        else:
            pos[0] -= 0.573625
            pos[1] -= 0.220625
        h_extra_args += 'set arg2 = "' + str(pos[0]) + '"\n'
        h_extra_args += 'set arg3 = "' + str(pos[1]) + '"\n'
h_extra_args += 'set argc = "' + str(num_args) + '"\n'

pane_node = pane.pwd()
child_type = pane_node.childTypeCategory().nodeTypes()

if 'Edge_Damage' not in child_type:
   hou.ui.displayMessage(
           'Cannot create node: incompatible pane network type')
   sys.exit(0)

# First clear the node selection
pane_node.setSelected(False, True)

h_path = pane_node.path()
h_preamble = 'set arg1 = "' + h_path + '"\n'
h_cmd = r'''
if ($argc < 2 || "$arg2" == "") then
   set arg2 = 0
endif
if ($argc < 3 || "$arg3" == "") then
   set arg3 = 0
endif
# Automatically generated script
# $arg1 - the path to add this node
# $arg2 - x position of the tile
# $arg3 - y position of the tile
# $arg4 - input node to wire to
# $arg5 - which input to wire to
# $arg6 - output node to wire to
# $arg7 - the type of this node
# $arg8 - the node is an indirect input
# $arg9 - index of output from $arg6

\set noalias = 1
set saved_path = `execute("oppwf")`
opcf $arg1

# Node $_obj_edgeDamage_edgeDamage (Sop/Edge_Damage)
set _obj_edgeDamage_edgeDamage = `run("opadd -e -n -u -v Edge_Damage edgeDamage")`
oplocate -x `$arg2 + 0` -y `$arg3 + 0` $_obj_edgeDamage_edgeDamage
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_edgeDamage_edgeDamage
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage
opuserdata -n '___Version___' -v '' $_obj_edgeDamage_edgeDamage
opuserdata -n 'wirestyle' -v 'rounded' $_obj_edgeDamage_edgeDamage
opcf $_obj_edgeDamage_edgeDamage

# Node $_obj_edgeDamage_edgeDamage_VOP (Sop/attribvop)
set _obj_edgeDamage_edgeDamage_VOP = `run("opadd -e -n -v attribvop VOP")`
oplocate -x `$arg2 + 2.99655` -y `$arg3 + 0.739236` $_obj_edgeDamage_edgeDamage_VOP
opspareds '    parm {         name    "bindgroup"         baseparm         label   "Group"         export  none         bindselector uvselect "Modify Points"             "Select the points to affect and press Enter to complete."             0 1 0xffffffff 0 bindgrouptype 0     }     parm {         name    "bindgrouptype"         baseparm         label   "Group Type"         export  none     }     parm {         name    "bindclass"         baseparm         label   "Run Over"         export  none     }     parm {         name    "vex_numcount"         baseparm         label   "Number Count"         export  none     }     parm {         name    "vex_threadjobsize"         baseparm         label   "Thread Job Size"         export  none     }     group {         name    "stdswitcher3"         label   "Vex Setup"          parm {             name    "vexsrc"             baseparm             label   "Vex Source"             export  all         }         parm {             name    "shoppath"             baseparm             label   "Shop Path"             export  all         }         parm {             name    "script"             baseparm             label   "Script"             export  all         }         parm {             name    "clear"             baseparm             label   "Re-load VEX Functions"             export  all         }         parm {             name    "vexsnippet"             baseparm             label   "Snippet"             export  none         }         parm {             name    "vex_strict"             baseparm             label   "Enforce Prototypes"             export  none         }         parm {             name    "vex_exportlist"             baseparm             label   "Attributes to Create"             export  none         }         parm {             name    "vop_compiler"             baseparm             label   "Compiler"             export  none         }         parm {             name    "vop_forcecompile"             baseparm             label   "Force Compile"             export  none         }         parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_multithread"             baseparm             label   "Enable Multithreading"             export  none         }     }      group {         name    "stdswitcher3_1"         label   "Attribute Bindings"          parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }         parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }     }      parm {         name    "ptnum"         label   "Point Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "vtxnum"         label   "Vertex Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "primnum"         label   "Primitive Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "id"         label   "Id"         type    integer         invisible         default { "-1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numpt"         label   "Number of Points"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numvtx"         label   "Number of Vertices"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numprim"         label   "Number of Prims"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Time"         label   "Time"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "TimeInc"         label   "Time Inc"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Frame"         label   "Frame"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "life"         label   "Life"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "age"         label   "Age"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput2"         label   "Second Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput3"         label   "Third Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput4"         label   "Fourth Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput1"         label   "First Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "uv"         label   "UV"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "P"         label   "P"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "v"         label   "Velocity"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "force"         label   "Force"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Cd"         label   "Cd"         type    float         invisible         size    3         default { "1" "1" "1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "N"         label   "N"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "scale"         label   "Scale"         type    float         default { "0.125" }         range   { -1 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "rough"         label   "Roughness"         type    float         default { "0.5" }         hidewhen "{ fractal == none }"         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "offset"         label   "Offset"         type    float         size    4         default { "0" "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "freq"         label   "Frequency"         type    float         size    4         default { "1" "1" "1" "1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     } ' $_obj_edgeDamage_edgeDamage_VOP
opparm $_obj_edgeDamage_edgeDamage_VOP  bindings ( 0 ) groupbindings ( 0 )
chblockbegin
chadd -t 0 0 $_obj_edgeDamage_edgeDamage_VOP scale
chkey -t 0 -v 0.050000000000000003 -m 0 -a 0 -A 0 -T a  -F 'ch("../displacementScale")' $_obj_edgeDamage_edgeDamage_VOP/scale
chadd -t 0 0 $_obj_edgeDamage_edgeDamage_VOP rough
chkey -t 0 -v 0.5 -m 0 -a 0 -A 0 -T a  -F 'ch("../roughness")' $_obj_edgeDamage_edgeDamage_VOP/rough
chadd -t 0 0 $_obj_edgeDamage_edgeDamage_VOP offset1
chkey -t 0 -v 19 -m 0 -a 0 -A 0 -T a  -F 'ch("../noiseOffsetx")' $_obj_edgeDamage_edgeDamage_VOP/offset1
chadd -t 0 0 $_obj_edgeDamage_edgeDamage_VOP offset2
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../noiseOffsety")' $_obj_edgeDamage_edgeDamage_VOP/offset2
chadd -t 0 0 $_obj_edgeDamage_edgeDamage_VOP offset3
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../noiseOffsetz")' $_obj_edgeDamage_edgeDamage_VOP/offset3
chadd -t 0 0 $_obj_edgeDamage_edgeDamage_VOP freq1
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../noiseFrequencyx")' $_obj_edgeDamage_edgeDamage_VOP/freq1
chadd -t 0 0 $_obj_edgeDamage_edgeDamage_VOP freq2
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../noiseFrequencyy")' $_obj_edgeDamage_edgeDamage_VOP/freq2
chadd -t 0 0 $_obj_edgeDamage_edgeDamage_VOP freq3
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../noiseFrequencyz")' $_obj_edgeDamage_edgeDamage_VOP/freq3
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_edgeDamage_edgeDamage_VOP
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_VOP
opuserdata -n '___Version___' -v '19.0.622' $_obj_edgeDamage_edgeDamage_VOP
opuserdata -n 'sidefx::parm_filter_text_pattern' -v ' f' $_obj_edgeDamage_edgeDamage_VOP
opuserdata -n 'wirestyle' -v 'rounded' $_obj_edgeDamage_edgeDamage_VOP
opcf $_obj_edgeDamage_edgeDamage_VOP

# Node $_obj_edgeDamage_edgeDamage_VOP_geometryvopglobal1 (Vop/geometryvopglobal::2.0)
set _obj_edgeDamage_edgeDamage_VOP_geometryvopglobal1 = `run("opadd -e -n -v geometryvopglobal::2.0 geometryvopglobal1")`
oplocate -x `$arg2 + -0.275364` -y `$arg3 + 3.67056` $_obj_edgeDamage_edgeDamage_VOP_geometryvopglobal1
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_edgeDamage_edgeDamage_VOP_geometryvopglobal1
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_VOP_geometryvopglobal1
opuserdata -n '___Version___' -v '' $_obj_edgeDamage_edgeDamage_VOP_geometryvopglobal1

# Node $_obj_edgeDamage_edgeDamage_VOP_geometryvopoutput1 (Vop/geometryvopoutput)
set _obj_edgeDamage_edgeDamage_VOP_geometryvopoutput1 = `run("opadd -e -n -v geometryvopoutput geometryvopoutput1")`
oplocate -x `$arg2 + 9.6097199999999994` -y `$arg3 + 3.67056` $_obj_edgeDamage_edgeDamage_VOP_geometryvopoutput1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_edgeDamage_edgeDamage_VOP_geometryvopoutput1
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_VOP_geometryvopoutput1
opuserdata -n '___Version___' -v '' $_obj_edgeDamage_edgeDamage_VOP_geometryvopoutput1

# Node $_obj_edgeDamage_edgeDamage_VOP_noise (Vop/unifiednoise_static::3.0)
set _obj_edgeDamage_edgeDamage_VOP_noise = `run("opadd -e -n -v unifiednoise_static::3.0 noise")`
oplocate -x `$arg2 + 1.70668` -y `$arg3 + 3.67056` $_obj_edgeDamage_edgeDamage_VOP_noise
opparm $_obj_edgeDamage_edgeDamage_VOP_noise fractal ( fBm )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_edgeDamage_edgeDamage_VOP_noise
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_VOP_noise
opuserdata -n '___Version___' -v '' $_obj_edgeDamage_edgeDamage_VOP_noise

# Node $_obj_edgeDamage_edgeDamage_VOP_displace (Vop/displacenml)
set _obj_edgeDamage_edgeDamage_VOP_displace = `run("opadd -e -n -v displacenml displace")`
oplocate -x `$arg2 + 7.6454000000000004` -y `$arg3 + 3.67056` $_obj_edgeDamage_edgeDamage_VOP_displace
opparm $_obj_edgeDamage_edgeDamage_VOP_displace scale ( 0.125 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_edgeDamage_edgeDamage_VOP_displace
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_VOP_displace
opuserdata -n '___Version___' -v '' $_obj_edgeDamage_edgeDamage_VOP_displace

# Node $_obj_edgeDamage_edgeDamage_VOP_fit1 (Vop/fit)
set _obj_edgeDamage_edgeDamage_VOP_fit1 = `run("opadd -e -n -v fit fit1")`
oplocate -x `$arg2 + 5.6445299999999996` -y `$arg3 + 3.67056` $_obj_edgeDamage_edgeDamage_VOP_fit1
opparm $_obj_edgeDamage_edgeDamage_VOP_fit1 destmin ( -1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_edgeDamage_edgeDamage_VOP_fit1
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_VOP_fit1
opuserdata -n '___Version___' -v '' $_obj_edgeDamage_edgeDamage_VOP_fit1

# Node $_obj_edgeDamage_edgeDamage_VOP_scale (Vop/parameter)
set _obj_edgeDamage_edgeDamage_VOP_scale = `run("opadd -e -n -v parameter scale")`
oplocate -x `$arg2 + 2.9508299999999998` -y `$arg3 + 4.67056` $_obj_edgeDamage_edgeDamage_VOP_scale
opparm -V 19.0.622 $_obj_edgeDamage_edgeDamage_VOP_scale parmname ( scale ) parmlabel ( Scale ) floatdef ( 0.125 ) rangeflt ( -1 1 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_edgeDamage_edgeDamage_VOP_scale
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_VOP_scale
opuserdata -n '___Version___' -v '19.0.622' $_obj_edgeDamage_edgeDamage_VOP_scale

# Node $_obj_edgeDamage_edgeDamage_VOP_rough (Vop/parameter)
set _obj_edgeDamage_edgeDamage_VOP_rough = `run("opadd -e -n -v parameter rough")`
oplocate -x `$arg2 + -1.5933200000000001` -y `$arg3 + 6.2705599999999997` $_obj_edgeDamage_edgeDamage_VOP_rough
opparm -V 19.0.622 $_obj_edgeDamage_edgeDamage_VOP_rough parmname ( rough ) parmlabel ( Roughness ) floatdef ( 0.5 ) exportcontext ( cvex ) hidewhen ( '{ fractal == none }' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_edgeDamage_edgeDamage_VOP_rough
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_VOP_rough
opuserdata -n '___Version___' -v '19.0.622' $_obj_edgeDamage_edgeDamage_VOP_rough

# Node $_obj_edgeDamage_edgeDamage_VOP_offset (Vop/parameter)
set _obj_edgeDamage_edgeDamage_VOP_offset = `run("opadd -e -n -v parameter offset")`
oplocate -x `$arg2 + -2.79332` -y `$arg3 + 8.67056` $_obj_edgeDamage_edgeDamage_VOP_offset
opparm -V 19.0.622 $_obj_edgeDamage_edgeDamage_VOP_offset parmname ( offset ) parmlabel ( Offset ) parmtype ( float4 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_edgeDamage_edgeDamage_VOP_offset
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_VOP_offset
opuserdata -n '___Version___' -v '19.0.622' $_obj_edgeDamage_edgeDamage_VOP_offset

# Node $_obj_edgeDamage_edgeDamage_VOP_freq (Vop/parameter)
set _obj_edgeDamage_edgeDamage_VOP_freq = `run("opadd -e -n -v parameter freq")`
oplocate -x `$arg2 + -2.8933200000000001` -y `$arg3 + 8.8705599999999993` $_obj_edgeDamage_edgeDamage_VOP_freq
opparm -V 19.0.622 $_obj_edgeDamage_edgeDamage_VOP_freq parmname ( freq ) parmlabel ( Frequency ) parmtype ( float4 ) float4def ( 1 1 1 1 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_edgeDamage_edgeDamage_VOP_freq
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_VOP_freq
opuserdata -n '___Version___' -v '19.0.622' $_obj_edgeDamage_edgeDamage_VOP_freq

# Node $_obj_edgeDamage_edgeDamage_VOP_multiply1 (Vop/multiply)
set _obj_edgeDamage_edgeDamage_VOP_multiply1 = `run("opadd -e -n -v multiply multiply1")`
oplocate -x `$arg2 + 3.6725599999999998` -y `$arg3 + 3.67056` $_obj_edgeDamage_edgeDamage_VOP_multiply1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_edgeDamage_edgeDamage_VOP_multiply1
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_VOP_multiply1
opuserdata -n '___Version___' -v '19.0.622' $_obj_edgeDamage_edgeDamage_VOP_multiply1

# Node $_obj_edgeDamage_edgeDamage_VOP_bind1 (Vop/bind)
set _obj_edgeDamage_edgeDamage_VOP_bind1 = `run("opadd -e -n -v bind bind1")`
oplocate -x `$arg2 + 1.70668` -y `$arg3 + 5.3034400000000002` $_obj_edgeDamage_edgeDamage_VOP_bind1
opparm -V 19.0.622 $_obj_edgeDamage_edgeDamage_VOP_bind1 parmname ( mask ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_edgeDamage_edgeDamage_VOP_bind1
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_VOP_bind1
opuserdata -n '___Version___' -v '19.0.622' $_obj_edgeDamage_edgeDamage_VOP_bind1
opcf ..
opcf ..
opcf $_obj_edgeDamage_edgeDamage
opcf $_obj_edgeDamage_edgeDamage_VOP
oporder -e geometryvopglobal1 geometryvopoutput1 noise displace fit1 scale rough offset freq multiply1 bind1 
opcf ..

# Node $_obj_edgeDamage_edgeDamage_remesh (Sop/remesh::2.0)
set _obj_edgeDamage_edgeDamage_remesh = `run("opadd -e -n -v remesh::2.0 remesh")`
oplocate -x `$arg2 + 3` -y `$arg3 + 1.4664900000000001` $_obj_edgeDamage_edgeDamage_remesh
chblockbegin
chadd -t 0 0 $_obj_edgeDamage_edgeDamage_remesh targetsize
chkey -t 0 -v 0.10000000000000001 -m 0 -a 0 -A 0 -T a  -F 'ch("../remeshDensity")' $_obj_edgeDamage_edgeDamage_remesh/targetsize
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_edgeDamage_edgeDamage_remesh
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_remesh
opuserdata -n '___Version___' -v '19.0.622' $_obj_edgeDamage_edgeDamage_remesh

# Node $_obj_edgeDamage_edgeDamage_normals (Sop/normal)
set _obj_edgeDamage_edgeDamage_normals = `run("opadd -e -n -v normal normals")`
oplocate -x `$arg2 + 3` -y `$arg3 + -0.65496299999999996` $_obj_edgeDamage_edgeDamage_normals
opparm -V 19.0.622 $_obj_edgeDamage_edgeDamage_normals cuspangle ( 0 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_edgeDamage_edgeDamage_normals
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_normals
opuserdata -n '___Version___' -v '19.0.622' $_obj_edgeDamage_edgeDamage_normals

# Node $_obj_edgeDamage_edgeDamage_output (Sop/output)
set _obj_edgeDamage_edgeDamage_output = `run("opadd -e -n -v output output")`
oplocate -x `$arg2 + 0.13905100000000001` -y `$arg3 + -3.4883799999999998` $_obj_edgeDamage_edgeDamage_output
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_edgeDamage_edgeDamage_output
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_output
opuserdata -n '___Version___' -v '19.0.622' $_obj_edgeDamage_edgeDamage_output

# Node $_obj_edgeDamage_edgeDamage_boolean (Sop/boolean::2.0)
set _obj_edgeDamage_edgeDamage_boolean = `run("opadd -e -n -v boolean::2.0 boolean")`
oplocate -x `$arg2 + 0.13905100000000001` -y `$arg3 + -1.3005` $_obj_edgeDamage_edgeDamage_boolean
opparm -V 19.0.622 $_obj_edgeDamage_edgeDamage_boolean booleanop ( intersect )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_edgeDamage_edgeDamage_boolean
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_boolean
opuserdata -n '___Version___' -v '19.0.622' $_obj_edgeDamage_edgeDamage_boolean

# Node $_obj_edgeDamage_edgeDamage_attrDelete (Sop/attribdelete)
set _obj_edgeDamage_edgeDamage_attrDelete = `run("opadd -e -n -v attribdelete attrDelete")`
oplocate -x `$arg2 + 2.99655` -y `$arg3 + 0.042615899999999998` $_obj_edgeDamage_edgeDamage_attrDelete
opparm $_obj_edgeDamage_edgeDamage_attrDelete doptdel ( off ) dovtxdel ( off ) primdel ( class ) dodtldel ( off )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_edgeDamage_edgeDamage_attrDelete
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_attrDelete
opuserdata -n '___Version___' -v '' $_obj_edgeDamage_edgeDamage_attrDelete

# Node $_obj_edgeDamage_edgeDamage_matchSize (Sop/matchsize)
set _obj_edgeDamage_edgeDamage_matchSize = `run("opadd -e -n -v matchsize matchSize")`
oplocate -x `$arg2 + -1.11759e-08` -y `$arg3 + 3.6712600000000002` $_obj_edgeDamage_edgeDamage_matchSize
opparm $_obj_edgeDamage_edgeDamage_matchSize size ( 10 10 10 ) doscale ( on ) stashxform ( on )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_edgeDamage_edgeDamage_matchSize
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_matchSize
opuserdata -n '___Version___' -v '' $_obj_edgeDamage_edgeDamage_matchSize

# Node $_obj_edgeDamage_edgeDamage_restoreSize (Sop/matchsize)
set _obj_edgeDamage_edgeDamage_restoreSize = `run("opadd -e -n -v matchsize restoreSize")`
oplocate -x `$arg2 + 0.13905100000000001` -y `$arg3 + -2.8162199999999999` $_obj_edgeDamage_edgeDamage_restoreSize
opparm $_obj_edgeDamage_edgeDamage_restoreSize restorexform ( on )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_edgeDamage_edgeDamage_restoreSize
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_restoreSize
opuserdata -n '___Version___' -v '' $_obj_edgeDamage_edgeDamage_restoreSize

# Node $_obj_edgeDamage_edgeDamage_INPUT (Sop/null)
set _obj_edgeDamage_edgeDamage_INPUT = `run("opadd -e -n -v null INPUT")`
oplocate -x `$arg2 + -1.11759e-08` -y `$arg3 + 6.0196500000000004` $_obj_edgeDamage_edgeDamage_INPUT
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_edgeDamage_edgeDamage_INPUT
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_INPUT
opuserdata -n '___Version___' -v '19.0.622' $_obj_edgeDamage_edgeDamage_INPUT

# Node $_obj_edgeDamage_edgeDamage_connectivity (Sop/connectivity)
set _obj_edgeDamage_edgeDamage_connectivity = `run("opadd -e -n -v connectivity connectivity")`
oplocate -x `$arg2 + -1.11759e-08` -y `$arg3 + 3.04331` $_obj_edgeDamage_edgeDamage_connectivity
opparm -V 19.0.622 $_obj_edgeDamage_edgeDamage_connectivity connecttype ( prim )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_edgeDamage_edgeDamage_connectivity
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_connectivity
opuserdata -n '___Version___' -v '19.0.622' $_obj_edgeDamage_edgeDamage_connectivity

# Node $_obj_edgeDamage_edgeDamage_end (Sop/block_end)
set _obj_edgeDamage_edgeDamage_end = `run("opadd -e -n -v block_end end")`
oplocate -x `$arg2 + 0.140651` -y `$arg3 + -2.07694` $_obj_edgeDamage_edgeDamage_end
opparm -V 19.0.622 $_obj_edgeDamage_edgeDamage_end itermethod ( pieces ) method ( merge ) class ( primitive ) attrib ( class ) blockpath ( ../begin ) templatepath ( ../begin ) singlepass ( 8 )
opcolor -c 0.75 0.40000000596046448 0 $_obj_edgeDamage_edgeDamage_end
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c on -e on -b off $_obj_edgeDamage_edgeDamage_end
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_end
opuserdata -n '___Version___' -v '19.0.622' $_obj_edgeDamage_edgeDamage_end

# Node $_obj_edgeDamage_edgeDamage_begin (Sop/block_begin)
set _obj_edgeDamage_edgeDamage_begin = `run("opadd -e -n -v block_begin begin")`
oplocate -x `$arg2 + 0.0016000000000000001` -y `$arg3 + 2.34552` $_obj_edgeDamage_edgeDamage_begin
opparm -V 19.0.622 $_obj_edgeDamage_edgeDamage_begin method ( piece ) blockpath ( ../end )
opcolor -c 0.75 0.40000000596046448 0 $_obj_edgeDamage_edgeDamage_begin
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c on -e on -b off $_obj_edgeDamage_edgeDamage_begin
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_begin
opuserdata -n '___Version___' -v '19.0.622' $_obj_edgeDamage_edgeDamage_begin

# Node $_obj_edgeDamage_edgeDamage_polyfill1 (Sop/polyfill)
set _obj_edgeDamage_edgeDamage_polyfill1 = `run("opadd -e -n -v polyfill polyfill1")`
oplocate -x `$arg2 + -1.3522e-08` -y `$arg3 + 0.739236` $_obj_edgeDamage_edgeDamage_polyfill1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_edgeDamage_edgeDamage_polyfill1
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_polyfill1
opuserdata -n '___Version___' -v '19.0.622' $_obj_edgeDamage_edgeDamage_polyfill1

# Node $_obj_edgeDamage_edgeDamage_addMaskIfDoesntExist (Sop/attribwrangle)
set _obj_edgeDamage_edgeDamage_addMaskIfDoesntExist = `run("opadd -e -n -v attribwrangle addMaskIfDoesntExist")`
oplocate -x `$arg2 + 4.32599` -y `$arg3 + 5.1544699999999999` $_obj_edgeDamage_edgeDamage_addMaskIfDoesntExist
opparm $_obj_edgeDamage_edgeDamage_addMaskIfDoesntExist  bindings ( 0 ) groupbindings ( 0 )
opparm $_obj_edgeDamage_edgeDamage_addMaskIfDoesntExist snippet ( 'if (!haspointattrib(0, "mask"))\n{\n    f@mask = 1;\n}' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_edgeDamage_edgeDamage_addMaskIfDoesntExist
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_addMaskIfDoesntExist
opuserdata -n '___Version___' -v '' $_obj_edgeDamage_edgeDamage_addMaskIfDoesntExist

# Node $_obj_edgeDamage_edgeDamage_transferMask (Sop/attribtransfer)
set _obj_edgeDamage_edgeDamage_transferMask = `run("opadd -e -n -v attribtransfer transferMask")`
oplocate -x `$arg2 + -0.0034500099999999999` -y `$arg3 + 4.2622200000000001` $_obj_edgeDamage_edgeDamage_transferMask
opparm -V 19.0.622 $_obj_edgeDamage_edgeDamage_transferMask primitiveattribs ( off ) pointattriblist ( mask )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_edgeDamage_edgeDamage_transferMask
opexprlanguage -s hscript $_obj_edgeDamage_edgeDamage_transferMask
opuserdata -n '___Version___' -v '19.0.622' $_obj_edgeDamage_edgeDamage_transferMask
oporder -e VOP remesh normals output boolean attrDelete matchSize restoreSize INPUT connectivity end begin polyfill1 addMaskIfDoesntExist transferMask 
opcf ..
opset -p on $_obj_edgeDamage_edgeDamage

opcf $arg1
opcf $_obj_edgeDamage_edgeDamage
opwire -n $_obj_edgeDamage_edgeDamage_remesh -0 $_obj_edgeDamage_edgeDamage_VOP
opcf $_obj_edgeDamage_edgeDamage_VOP
opwire -n $_obj_edgeDamage_edgeDamage_VOP_displace -0 $_obj_edgeDamage_edgeDamage_VOP_geometryvopoutput1
opwire -n $_obj_edgeDamage_edgeDamage_VOP_geometryvopglobal1 -0 $_obj_edgeDamage_edgeDamage_VOP_noise
opwire -n $_obj_edgeDamage_edgeDamage_VOP_freq -1 $_obj_edgeDamage_edgeDamage_VOP_noise
opwire -n $_obj_edgeDamage_edgeDamage_VOP_offset -2 $_obj_edgeDamage_edgeDamage_VOP_noise
opwire -n $_obj_edgeDamage_edgeDamage_VOP_rough -14 $_obj_edgeDamage_edgeDamage_VOP_noise
opwire -n $_obj_edgeDamage_edgeDamage_VOP_fit1 -2 $_obj_edgeDamage_edgeDamage_VOP_displace
opwire -n $_obj_edgeDamage_edgeDamage_VOP_scale -3 $_obj_edgeDamage_edgeDamage_VOP_displace
opwire -n $_obj_edgeDamage_edgeDamage_VOP_multiply1 -0 $_obj_edgeDamage_edgeDamage_VOP_fit1
opwire -n $_obj_edgeDamage_edgeDamage_VOP_noise -0 $_obj_edgeDamage_edgeDamage_VOP_multiply1
opwire -n $_obj_edgeDamage_edgeDamage_VOP_bind1 -1 $_obj_edgeDamage_edgeDamage_VOP_multiply1
opcf ..
opwire -n $_obj_edgeDamage_edgeDamage_begin -0 $_obj_edgeDamage_edgeDamage_remesh
opwire -n $_obj_edgeDamage_edgeDamage_attrDelete -0 $_obj_edgeDamage_edgeDamage_normals
opwire -n $_obj_edgeDamage_edgeDamage_restoreSize -0 $_obj_edgeDamage_edgeDamage_output
opwire -n $_obj_edgeDamage_edgeDamage_polyfill1 -0 $_obj_edgeDamage_edgeDamage_boolean
opwire -n $_obj_edgeDamage_edgeDamage_normals -1 $_obj_edgeDamage_edgeDamage_boolean
opwire -n $_obj_edgeDamage_edgeDamage_VOP -0 $_obj_edgeDamage_edgeDamage_attrDelete
opwire -n $_obj_edgeDamage_edgeDamage_transferMask -0 $_obj_edgeDamage_edgeDamage_matchSize
opwire -n $_obj_edgeDamage_edgeDamage_end -0 $_obj_edgeDamage_edgeDamage_restoreSize
opwire -n -i 0 -0 $_obj_edgeDamage_edgeDamage_INPUT
opwire -n $_obj_edgeDamage_edgeDamage_matchSize -0 $_obj_edgeDamage_edgeDamage_connectivity
opwire -n $_obj_edgeDamage_edgeDamage_boolean -0 $_obj_edgeDamage_edgeDamage_end
opwire -n $_obj_edgeDamage_edgeDamage_connectivity -0 $_obj_edgeDamage_edgeDamage_begin
opwire -n $_obj_edgeDamage_edgeDamage_begin -0 $_obj_edgeDamage_edgeDamage_polyfill1
opwire -n $_obj_edgeDamage_edgeDamage_INPUT -0 $_obj_edgeDamage_edgeDamage_addMaskIfDoesntExist
opwire -n -i 1 -1 $_obj_edgeDamage_edgeDamage_addMaskIfDoesntExist
opwire -n $_obj_edgeDamage_edgeDamage_INPUT -0 $_obj_edgeDamage_edgeDamage_transferMask
opwire -n $_obj_edgeDamage_edgeDamage_addMaskIfDoesntExist -1 $_obj_edgeDamage_edgeDamage_transferMask
opcf ..

set oidx = 0
if ($argc >= 9 && "$arg9" != "") then
    set oidx = $arg9
endif

if ($argc >= 5 && "$arg4" != "") then
    set output = $_obj_edgeDamage_edgeDamage
    opwire -n $output -$arg5 $arg4
endif
if ($argc >= 6 && "$arg6" != "") then
    set input = $_obj_edgeDamage_edgeDamage
    if ($arg8) then
        opwire -n -i $arg6 -0 $input
    else
        opwire -n -o $oidx $arg6 -0 $input
    endif
endif
opcf $saved_path
'''
hou.hscript(h_preamble + h_extra_args + h_cmd)
