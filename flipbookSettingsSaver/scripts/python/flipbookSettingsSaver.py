import inspect
import toolutils
import zlib
import hutil.json
import hou

_settingNode = "_flipbook_setting"
#don't store the framerange since it's always $FSTART and $FEND
_ignore = {"stash","frameRange"}

"""
    convert list to json data
"""
def listToJson(data, compress=True):
    data = hutil.json.utf8Dumps(data)
    if(compress):
        data = zlib.compress(data)
    return data

"""
    convert json data to list
"""
def jsonToList(str_data, compress=True):
    if(compress):
        str_data = zlib.decompress(str_data)
    return hutil.json.utf8Loads(str_data)
"""
    default setting
"""
def default(setting):
    setting.overrideGamma(True)
    setting.gamma(2.2)
    setting.overrideLUT(False)
    setting.antialias(hou.flipbookAntialias.HighQuality)
    setting.resolution((1920,1080))
    setting.cropOutMaskOverlay(True)

"""
    returns the setting node object
"""
def getSettingNode():
    return hou.node(_settingNode)

"""
    get current viewer flipbook setting
"""
def getFlipbookSettings():
    return toolutils.sceneViewer().flipbookSettings()

"""
    convert flipbook settings to a dictionary list
"""
def settingsToList(settings):
    insp = inspect.getmembers(settings, inspect.ismethod)
    output={}
    for m in insp:
        name = m[0]
        if not (name.startswith('__') or name in _ignore):
            try:
                method = getattr(settings, name)
                value = method()
                if isinstance(value,hou.EnumValue):
                    value = repr(value)

                output[name] = value
            except:
                continue
    return output

"""
    convert dictionary list to flipbook settings object
"""
def listToSettings(settings,list):
    for key, value in list.items():
        method = getattr(settings, key)
        if isinstance(value,basestring) and len(value.split("."))>1 :
            enumVal=value.split(".")
            value = getattr(getattr(hou,enumVal[0]),enumVal[1])
        method(value)
    return settings

"""
    promp values for testing
"""
def prompt(data):
    hou.ui.displayMessage(repr(data))

"""
    initialize setting Node
"""
def load():
    #prompt("loaded settings")
    settingNode = hou.node("/obj/"+_settingNode)
    for pt in settingNode.parmTuples():
        pt.hide(1)
    settings = getFlipbookSettings()
    if(not settingNode):
        default(settings)
    else:
        listToSettings(settings,jsonToList(settingNode.userData("flipbooksetting"),0))

"""
    initialize setting Node
"""
def save():
    #prompt("saved settings")
    settingNode = hou.node("/obj/"+_settingNode)
    settings = getFlipbookSettings()
    if(not settingNode):
        obj = hou.node("/obj")
        settingNode = obj.createNode("geo", _settingNode, run_init_scripts=False, load_contents=False)
        settingNode.moveToGoodPosition
        settingNode.setColor(hou.Color(64/255,69/255,74/255))
        for pt in settingNode.parmTuples():
            pt.hide(1)
    settingNode.setUserData("flipbooksetting", listToJson(settingsToList(settings),0))
