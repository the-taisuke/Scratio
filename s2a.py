# -*- coding: utf-8 -*-
from server import *
import serial.tools.list_ports
import wx
import json
import os
import webbrowser

class s2a:
    def __init__(self):
        self.oflg = 0
        self.port = ""
        self.lang = 'ja'
        self.getportlist()
        self.openjson()

    def openjson(self):
        json_path = os.path.abspath("json/setting.json")
        f = open(json_path, 'r')
        self.jsonData = json.load(f)


    def getportlist(self):
        self.ports = []
        lists = list(serial.tools.list_ports.comports())
        for x in lists:
            self.ports.append(x[0])

        return self.ports

    def connectServer(self):
        self.server = server(8099)
        self.server.main()
        self.server.call_arduino(self.port)

    def click_button(self,event):
        if self.oflg == 0:
            self.connectServer()
            self.button.SetLabel(self.jsonData[self.lang][u"connecting"])
            self.oflg = 1
        else:
            self.server.close()
            self.button.SetLabel(self.jsonData[self.lang][u"connect"])
            self.oflg = 0

    def listbox_select(self,event):
        obj = event.GetEventObject()
        self.port = obj.GetStringSelection()

    def selectMenu(self,event):
        val = event.GetId()

        if val == 1 or val == 2:
            if val == 1:
                self.lang = 'ja'
            else:
                self.lang = 'en'
            self.s_text.SetLabel(self.jsonData[self.lang][u"serial"])
            if self.oflg == 0:
                self.button.SetLabel(self.jsonData[self.lang][u"connect"])
            else:
                self.button.SetLabel(self.jsonData[self.lang][u"connecting"])
        elif val == 3:
            webbrowser.open_new_tab(self.jsonData[self.lang][u"site"])
        elif val == 4:
            wx.MessageBox(self.jsonData['version'], 'Version', wx.OK)


    def main(self):
        app = wx.App()
        self.frame = wx.Frame(None, wx.ID_ANY, u'S2A',size=(300,200))

        application = wx.App()

        self.panel = wx.Panel(self.frame,wx.ID_ANY)
        self.panel.SetBackgroundColour("#AFAFAF")

        #add menu
        menu_lang = wx.Menu()
        self.menu_about = wx.Menu()
        self.menu_bar = wx.MenuBar()

        self.menu_bar.Append(menu_lang,u"Lang")
        menu_lang.AppendRadioItem(1,u"日本語")
        menu_lang.AppendRadioItem(2,u"English")

        self.menu_bar.Append(self.menu_about,u"Help")
        self.menu_about.Append(3,u"MySite")
        self.menu_about.Append(4,u"Version Info")
        self.frame.Bind(wx.EVT_MENU,self.selectMenu)

        self.s_text = wx.StaticText(self.panel,wx.ID_ANY,self.jsonData[self.lang][u"serial"])

        element_array = self.ports
        listbox = wx.ListBox(self.panel,wx.ID_ANY,choices=element_array,style=wx.LB_SINGLE)
        listbox.Bind(wx.EVT_LISTBOX,self.listbox_select)

        self.button = wx.Button(self.panel,wx.ID_ANY,self.jsonData[self.lang][u"connect"])
        self.button.Bind(wx.EVT_BUTTON,self.click_button)

        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(self.s_text,flag=wx.GROW|wx.LEFT|wx.TOP,border=10)
        layout.Add(listbox,flag=wx.GROW|wx.ALL,border=10)
        layout.Add(self.button,flag=wx.GROW|wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM,border=10)

        self.panel.SetSizer(layout)
        self.frame.SetMenuBar(self.menu_bar)
        self.frame.Show()
        application.MainLoop()

    def close(self):
        self.server.close()
        self.oflg = 0

if __name__ == '__main__':
    s2a = s2a()
    s2a.main()
