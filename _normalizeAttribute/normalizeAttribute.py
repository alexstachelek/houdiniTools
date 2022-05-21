
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

if 'Normalize_Attribute' not in child_type:
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

# Node $_obj_geo1_normalizeAttribute (Sop/Normalize_Attribute)
set _obj_geo1_normalizeAttribute = `run("opadd -e -n -u -v Normalize_Attribute normalizeAttribute")`
oplocate -x `$arg2 + 0` -y `$arg3 + 0` $_obj_geo1_normalizeAttribute
opparm $_obj_geo1_normalizeAttribute attributeName ( tester )
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_normalizeAttribute
opexprlanguage -s hscript $_obj_geo1_normalizeAttribute
opuserdata -n '___Version___' -v '' $_obj_geo1_normalizeAttribute
opuserdata -n 'wirestyle' -v 'rounded' $_obj_geo1_normalizeAttribute
opcf $_obj_geo1_normalizeAttribute

# Node $_obj_geo1_normalizeAttribute_output (Sop/output)
set _obj_geo1_normalizeAttribute_output = `run("opadd -e -n -v output output")`
oplocate -x `$arg2 + -1.1175870908687308e-08` -y `$arg3 + 1.0176674341330918` $_obj_geo1_normalizeAttribute_output
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_normalizeAttribute_output
opexprlanguage -s hscript $_obj_geo1_normalizeAttribute_output
opuserdata -n '___Version___' -v '19.0.622' $_obj_geo1_normalizeAttribute_output

# Node $_obj_geo1_normalizeAttribute_switchAttrType (Sop/switch)
set _obj_geo1_normalizeAttribute_switchAttrType = `run("opadd -e -n -v switch switchAttrType")`
oplocate -x `$arg2 + -2.0489096676269821e-08` -y `$arg3 + 2.5121876409385844` $_obj_geo1_normalizeAttribute_switchAttrType
chblockbegin
chadd -t 0 0 $_obj_geo1_normalizeAttribute_switchAttrType input
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../attributeType")' $_obj_geo1_normalizeAttribute_switchAttrType/input
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_normalizeAttribute_switchAttrType
opexprlanguage -s hscript $_obj_geo1_normalizeAttribute_switchAttrType
opuserdata -n '___Version___' -v '19.0.622' $_obj_geo1_normalizeAttribute_switchAttrType

# Node $_obj_geo1_normalizeAttribute_max (Sop/attribpromote)
set _obj_geo1_normalizeAttribute_max = `run("opadd -e -n -v attribpromote max")`
oplocate -x `$arg2 + -0.0034500062465667759` -y `$arg3 + 4.5129568687943262` $_obj_geo1_normalizeAttribute_max
opparm -V 19.0.622 $_obj_geo1_normalizeAttribute_max inname ( '`chs("../attributeName")`' ) outclass ( detail ) method ( max ) useoutname ( on ) outname ( '`chs("../attributeName")`_MAX' ) deletein ( off )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_normalizeAttribute_max
opexprlanguage -s hscript $_obj_geo1_normalizeAttribute_max
opuserdata -n '___Version___' -v '19.0.622' $_obj_geo1_normalizeAttribute_max

# Node $_obj_geo1_normalizeAttribute_min (Sop/attribpromote)
set _obj_geo1_normalizeAttribute_min = `run("opadd -e -n -v attribpromote min")`
oplocate -x `$arg2 + -0.0034500062465667725` -y `$arg3 + 5.2013883860721286` $_obj_geo1_normalizeAttribute_min
opparm -V 19.0.622 $_obj_geo1_normalizeAttribute_min inname ( '`chs("../attributeName")`' ) outclass ( detail ) method ( min ) useoutname ( on ) outname ( '`chs("../attributeName")`_MIN' ) deletein ( off )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_normalizeAttribute_min
opexprlanguage -s hscript $_obj_geo1_normalizeAttribute_min
opuserdata -n '___Version___' -v '19.0.622' $_obj_geo1_normalizeAttribute_min

# Node $_obj_geo1_normalizeAttribute_vector3 (Sop/attribwrangle)
set _obj_geo1_normalizeAttribute_vector3 = `run("opadd -e -n -v attribwrangle vector3")`
oplocate -x `$arg2 + -0.0030000077094880506` -y `$arg3 + 3.5144383860721295` $_obj_geo1_normalizeAttribute_vector3
opparm $_obj_geo1_normalizeAttribute_vector3  bindings ( 0 ) groupbindings ( 0 )
opparm $_obj_geo1_normalizeAttribute_vector3 class ( detail ) snippet ( 'string attrib = chs("../attributeName");\nstring attribMin = chs("../attributeName") + ("_MIN");\nstring attribMax = chs("../attributeName") + ("_MAX");\nvector min = detail(0, attribMin, 0);\nvector max = detail(0, attribMax, 0);\n\nint np = npoints(0);\n\nfor (int i=0; i<np; i++)\n{\n    vector oldValue = point(0, attrib, i);\n    vector newValue = fit(oldValue, min, max, set(0,0,0), set(1,1,1));\n    setpointattrib(0, attrib, i, newValue, "set");\n}' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_normalizeAttribute_vector3
opexprlanguage -s hscript $_obj_geo1_normalizeAttribute_vector3
opuserdata -n '___Version___' -v '' $_obj_geo1_normalizeAttribute_vector3

# Node $_obj_geo1_normalizeAttribute_float (Sop/attribwrangle)
set _obj_geo1_normalizeAttribute_float = `run("opadd -e -n -v attribwrangle float")`
oplocate -x `$arg2 + -2.7327066192052945` -y `$arg3 + 3.5144383860721295` $_obj_geo1_normalizeAttribute_float
opparm $_obj_geo1_normalizeAttribute_float  bindings ( 0 ) groupbindings ( 0 )
opparm $_obj_geo1_normalizeAttribute_float class ( detail ) snippet ( 'string attrib = chs("../attributeName");\nstring attribMin = chs("../attributeName") + ("_MIN");\nstring attribMax = chs("../attributeName") + ("_MAX");\nfloat min = detail(0, attribMin, 0);\nfloat max = detail(0, attribMax, 0);\n\nint np = npoints(0);\n\nfor (int i=0; i<np; i++)\n{\n    float oldValue = point(0, attrib, i);\n    float newValue = fit(oldValue, min, max, 0, 1);\n    setpointattrib(0, attrib, i, newValue, "set");\n}' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_normalizeAttribute_float
opexprlanguage -s hscript $_obj_geo1_normalizeAttribute_float
opuserdata -n '___Version___' -v '' $_obj_geo1_normalizeAttribute_float

# Node $_obj_geo1_normalizeAttribute_cleanupAttrs (Sop/attribdelete)
set _obj_geo1_normalizeAttribute_cleanupAttrs = `run("opadd -e -n -v attribdelete cleanupAttrs")`
oplocate -x `$arg2 + -0.0034500062465667725` -y `$arg3 + 1.6969615027161598` $_obj_geo1_normalizeAttribute_cleanupAttrs
opparm $_obj_geo1_normalizeAttribute_cleanupAttrs doptdel ( off ) dovtxdel ( off ) doprimdel ( off ) dtldel ( '`chs("../attributeName")`_MIN `chs("../attributeName")`_MAX' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_normalizeAttribute_cleanupAttrs
opexprlanguage -s hscript $_obj_geo1_normalizeAttribute_cleanupAttrs
opuserdata -n '___Version___' -v '' $_obj_geo1_normalizeAttribute_cleanupAttrs

# Node $_obj_geo1_normalizeAttribute_vector4 (Sop/attribwrangle)
set _obj_geo1_normalizeAttribute_vector4 = `run("opadd -e -n -v attribwrangle vector4")`
oplocate -x `$arg2 + 3.1203757769228329` -y `$arg3 + 3.5144383860721295` $_obj_geo1_normalizeAttribute_vector4
opparm $_obj_geo1_normalizeAttribute_vector4  bindings ( 0 ) groupbindings ( 0 )
opparm $_obj_geo1_normalizeAttribute_vector4 class ( detail ) snippet ( 'string attrib = chs("../attributeName");\nstring attribMin = chs("../attributeName") + ("_MIN");\nstring attribMax = chs("../attributeName") + ("_MAX");\nvector4 min = detail(0, attribMin, 0);\nvector4 max = detail(0, attribMax, 0);\n\nint np = npoints(0);\n\nfor (int i=0; i<np; i++)\n{\n    vector4 oldValue = point(0, attrib, i);\n    vector4 newValue = fit(oldValue, min, max, set(0,0,0,0), set(1,1,1,1));\n    setpointattrib(0, attrib, i, newValue, "set");\n}' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_normalizeAttribute_vector4
opexprlanguage -s hscript $_obj_geo1_normalizeAttribute_vector4
opuserdata -n '___Version___' -v '' $_obj_geo1_normalizeAttribute_vector4
oporder -e output switchAttrType max min vector3 float cleanupAttrs vector4 
opcf ..
opset -p on $_obj_geo1_normalizeAttribute

opcf $arg1
opwire -n $_obj_geo1_attribrandomize1 -0 $_obj_geo1_normalizeAttribute
opcf $_obj_geo1_normalizeAttribute
opwire -n $_obj_geo1_normalizeAttribute_cleanupAttrs -0 $_obj_geo1_normalizeAttribute_output
opwire -n $_obj_geo1_normalizeAttribute_float -0 $_obj_geo1_normalizeAttribute_switchAttrType
opwire -n $_obj_geo1_normalizeAttribute_vector3 -1 $_obj_geo1_normalizeAttribute_switchAttrType
opwire -n $_obj_geo1_normalizeAttribute_vector4 -2 $_obj_geo1_normalizeAttribute_switchAttrType
opwire -n $_obj_geo1_normalizeAttribute_min -0 $_obj_geo1_normalizeAttribute_max
opwire -n -i 0 -0 $_obj_geo1_normalizeAttribute_min
opwire -n $_obj_geo1_normalizeAttribute_max -0 $_obj_geo1_normalizeAttribute_vector3
opwire -n $_obj_geo1_normalizeAttribute_max -0 $_obj_geo1_normalizeAttribute_float
opwire -n $_obj_geo1_normalizeAttribute_switchAttrType -0 $_obj_geo1_normalizeAttribute_cleanupAttrs
opwire -n $_obj_geo1_normalizeAttribute_max -0 $_obj_geo1_normalizeAttribute_vector4
opcf ..

set oidx = 0
if ($argc >= 9 && "$arg9" != "") then
    set oidx = $arg9
endif

if ($argc >= 5 && "$arg4" != "") then
    set output = $_obj_geo1_normalizeAttribute
    opwire -n $output -$arg5 $arg4
endif
if ($argc >= 6 && "$arg6" != "") then
    set input = $_obj_geo1_normalizeAttribute
    if ($arg8) then
        opwire -n -i $arg6 -0 $input
    else
        opwire -n -o $oidx $arg6 -0 $input
    endif
endif
opcf $saved_path
'''
hou.hscript(h_preamble + h_extra_args + h_cmd)
