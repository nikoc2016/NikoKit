from NikoKit.NikoQt.NQKernel.NQGui import NQWidget, NQWindow


def register_all_widgets():
    NQWidget.NQWidgetRegistry.add(NQWidget.NQBasicWidget)
    NQWidget.NQWidgetRegistry.add(NQWindow.NQWindow)

register_all_widgets()
