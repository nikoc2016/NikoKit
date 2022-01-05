from NikoKit.NikoQt.NQKernel.NQGui import NQWidget, NQWidgetLaunchPad, NQWindow, NQWindowLogin


def register_all_widgets():
    NQWidget.NQWidgetRegistry.add(NQWidget.NQBasicWidget)
    NQWidget.NQWidgetRegistry.add(NQWidgetLaunchPad.NQWidgetLaunchPad)

    NQWidget.NQWidgetRegistry.add(NQWindow.NQWindow)
    NQWidget.NQWidgetRegistry.add(NQWindowLogin.NQWindowLogin)


register_all_widgets()
