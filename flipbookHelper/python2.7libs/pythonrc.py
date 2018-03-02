import flipbookSettingsSaver
import hou
def scene_event_callback(event_type):
    if event_type == hou.hipFileEventType.AfterLoad:
        #hou.ui.displayMessage("loaded")
        flipbookSettingsSaver.load()
    elif event_type == hou.hipFileEventType.BeforeSave:
        #hou.ui.displayMessage("saved")
        flipbookSettingsSaver.save()
        #hou.ui.displayMessage("The user loaded", buttons
        #print("The user loaded", hou.hipFile.path())


hou.hipFile.addEventCallback(scene_event_callback)
