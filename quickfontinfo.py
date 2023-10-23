#!/usr/bin/env python3

import os
import platform
import wx
from fontTools.ttLib import TTFont, TTCollection

APPVERSION = "0.1"
FILEEXT = [".ttf", ".otf", ".ttc", ".otc"]
TTFKEYS = ["glyf"]
OTFKEYS = ["CFF ", "CFF2"]

class FontType:
    UNKNOWN = -1
    TTF = 0
    OTF = 1

class FontInfo:
    def __init__(self, fontFilename, fontNum=-1):
        font = TTFont(fontFilename, fontNumber=fontNum)
        nametable = font['name']
        os2table = font['OS/2']

        self.fontType = self.getFontType(font)
        self.fontFamily = getNameInfo(1, nametable)
        self.fontSubfamily = getNameInfo(2, nametable)
        self.fontWeight = os2table.usWeightClass
        self.fontFullname = getNameInfo(4, nametable)
        self.fontVersion = getNameInfo(5, nametable)
        self.fontPostscript = getNameInfo(6, nametable)
        font.close()

    def getFontType(self, font):
        keys = font.keys()
        if any(x in TTFKEYS for x in keys):
            return FontType.TTF
        elif any(x in OTFKEYS for x in keys):
            return FontType.OTF
        else:
            return FontType.UNKNOWN

class MainFrame(wx.Frame):
    openedFolder = "."
    openedFontType = FontType.UNKNOWN
    
    def __init__(self):
        super().__init__(parent=None, title=f"Quick Font Info v{APPVERSION}")
        panel = wx.Panel(self)
        self.sizerWindow = wx.BoxSizer(wx.VERTICAL)
        self.sizerMain = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerLeft = wx.BoxSizer(wx.VERTICAL)
        self.sizerRight = wx.BoxSizer(wx.VERTICAL)
        self.sizerFontChoice = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerFontInfo = wx.BoxSizer(wx.VERTICAL)
        self.sizerControls = wx.BoxSizer(wx.HORIZONTAL)

        # font files list
        self.fileListListBox = wx.ListBox(panel)
        self.sizerLeft.Add(self.fileListListBox, 1, wx.ALL | wx.EXPAND, 0)

        # open buttons and the directory label
        self.openFileButton = wx.Button(panel, label="Open file")
        self.sizerControls.Add(self.openFileButton, 0, wx.ALL, 0)
        self.openFolderButton = wx.Button(panel, label="Open folder")
        self.sizerControls.Add(self.openFolderButton, 0, wx.LEFT, 8)
        self.openSystemFontsButton = wx.Button(panel, label="System fonts")
        self.sizerControls.Add(self.openSystemFontsButton, 0, wx.LEFT, 8)
        self.openedFolderLabel = wx.StaticText(panel, label="")
        self.sizerControls.Add(self.openedFolderLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 8)
        
        # font selection for collection files
        self.fontSelectLabel = wx.StaticText(panel, label="Font:")
        self.sizerFontChoice.Add(self.fontSelectLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 0)
        self.fontSelectChoice = wx.Choice(panel)
        self.sizerFontChoice.Add(self.fontSelectChoice, 0, wx.LEFT, 8)
        self.sizerRight.Add(self.sizerFontChoice, 0, wx.BOTTOM | wx.EXPAND, 8)

        # font information
        self.familyLabel = wx.StaticText(panel, label="Font Family:")
        self.sizerFontInfo.Add(self.familyLabel, 0, wx.TOP, 0)
        self.familyTextCtrl = wx.TextCtrl(panel, style=wx.TE_READONLY)
        self.sizerFontInfo.Add(self.familyTextCtrl, 0, wx.TOP | wx.EXPAND, 2)
        self.typeLabel = wx.StaticText(panel, label="Font Subfamily (type):")
        self.sizerFontInfo.Add(self.typeLabel, 0, wx.TOP, 8)
        self.typeTextCtrl = wx.TextCtrl(panel, style=wx.TE_READONLY)
        self.sizerFontInfo.Add(self.typeTextCtrl, 0, wx.TOP | wx.EXPAND, 2)
        self.weightLabel = wx.StaticText(panel, label="Weight:")
        self.sizerFontInfo.Add(self.weightLabel, 0, wx.TOP, 8)
        self.weightTextCtrl = wx.TextCtrl(panel, style=wx.TE_READONLY)
        self.sizerFontInfo.Add(self.weightTextCtrl, 0, wx.TOP | wx.EXPAND, 2)
        self.fullNameLabel = wx.StaticText(panel, label="Full name:")
        self.sizerFontInfo.Add(self.fullNameLabel, 0, wx.TOP, 8)
        self.fullNameTextCtrl = wx.TextCtrl(panel, style=wx.TE_READONLY)
        self.sizerFontInfo.Add(self.fullNameTextCtrl, 0, wx.TOP | wx.EXPAND, 2)
        self.versionLabel = wx.StaticText(panel, label="Version:")
        self.sizerFontInfo.Add(self.versionLabel, 0, wx.TOP, 8)
        self.versionTextCtrl = wx.TextCtrl(panel, style=wx.TE_READONLY)
        self.sizerFontInfo.Add(self.versionTextCtrl, 0, wx.TOP | wx.EXPAND, 2)
        self.psNameLabel = wx.StaticText(panel, label="PostScript name:")
        self.sizerFontInfo.Add(self.psNameLabel, 0, wx.TOP, 8)
        self.psNameTextCtrl = wx.TextCtrl(panel, style=wx.TE_READONLY)
        self.sizerFontInfo.Add(self.psNameTextCtrl, 0, wx.TOP | wx.EXPAND, 2)
        self.highlightCheckBox = wx.CheckBox(panel, label="Highlight the full font face name")
        self.sizerFontInfo.Add(self.highlightCheckBox, 0, wx.TOP, 16)
        self.faceNameCopyButton = wx.Button(panel, label="Copy the font face name to clipboard")
        self.sizerFontInfo.Add(self.faceNameCopyButton, 0, wx.TOP, 8)
        self.sizerRight.Add(self.sizerFontInfo, 0, wx.TOP | wx.EXPAND, 0)

        self.sizerMain.Add(self.sizerLeft, 1, wx.ALL | wx.EXPAND, 8)
        self.sizerMain.Add(self.sizerRight, 2, wx.ALL | wx.EXPAND, 8)
        self.sizerWindow.Add(self.sizerMain, 1, wx.ALL | wx.EXPAND, 0)
        self.sizerWindow.Add(self.sizerControls, 0, wx.LEFT | wx.BOTTOM, 8)
        panel.SetSizer(self.sizerWindow)

        # setting default values and binding events
        self.fontSelectLabel.Shown = False
        self.fontSelectChoice.Shown = False
        self.highlightCheckBox.Value = True
        if platform.system() != "Windows":
            # the 'system fonts' button is a windows-only feature for now, other platforms require dealing with the structure of their font folders
            self.openSystemFontsButton.Shown = False
        self.fileListListBox.Bind(wx.EVT_LISTBOX, self.fileListListBoxOnSelection)
        self.fontSelectChoice.Bind(wx.EVT_CHOICE, self.fontSelectChoiceOnChange)
        self.highlightCheckBox.Bind(wx.EVT_CHECKBOX, self.highlightCheckBoxOnClick)
        self.faceNameCopyButton.Bind(wx.EVT_BUTTON, self.faceNameCopyButtonOnClick)
        self.openFileButton.Bind(wx.EVT_BUTTON, self.openFileButtonOnClick)
        self.openFolderButton.Bind(wx.EVT_BUTTON, self.openFolderButtonOnClick)
        self.openSystemFontsButton.Bind(wx.EVT_BUTTON, self.openSystemFontsButtonOnClick)

        self.SetSize(wx.Size(860, 540))
        self.Show()
    
    def showInfo(self, fontPath):
        self.familyTextCtrl.Value = ""
        self.typeTextCtrl.Value = ""
        self.weightTextCtrl.Value = ""
        self.fullNameTextCtrl.Value = ""
        self.versionTextCtrl.Value = ""
        self.psNameTextCtrl.Value = ""
        self.openedFontType = FontType.UNKNOWN
        self.fontSelectChoice.Clear()
        try:
            with open(fontPath, 'rb') as file:
                if file.read(4) == b'ttcf':
                    # it's a collection
                    fontC = TTCollection(fontPath, lazy=True)
                    for f in fontC:
                        fontFullname = getNameInfo(4, f['name'])
                        self.fontSelectChoice.Append(str(fontFullname))
                    self.fontSelectChoice.Selection = 0
                    self.fontSelectLabel.Shown = True
                    self.fontSelectChoice.Shown = True
                    self.sizerRight.Layout()
                    font = FontInfo(fontPath, fontNum=0)
                else:
                    # not a collection
                    self.fontSelectLabel.Shown = False
                    self.fontSelectChoice.Shown = False
                    self.sizerRight.Layout()
                    font = FontInfo(fontPath)
        except Exception as err:
            errDlg = wx.MessageDialog(self, f"Error while trying to read the font data: {err}", "Error", wx.OK | wx.ICON_ERROR)
            errDlg.ShowModal()
            return
        self.familyTextCtrl.Value = str(font.fontFamily)
        self.typeTextCtrl.Value = str(font.fontSubfamily)
        self.weightTextCtrl.Value = str(font.fontWeight)
        self.fullNameTextCtrl.Value = str(font.fontFullname)
        self.versionTextCtrl.Value = str(font.fontVersion)
        self.psNameTextCtrl.Value = str(font.fontPostscript)
        self.openedFontType = font.fontType
        self.highlightFFName(self.openedFontType)
    
    def highlightFFName(self, fontType):
        # highlights the full font face name
        if self.highlightCheckBox.Value:
            match fontType:
                case FontType.TTF:
                    self.fullNameTextCtrl.SetBackgroundColour(wx.Colour(168,255,200))
                    self.psNameTextCtrl.SetBackgroundColour(wx.NullColour)
                case FontType.OTF:
                    self.fullNameTextCtrl.SetBackgroundColour(wx.NullColour)
                    self.psNameTextCtrl.SetBackgroundColour(wx.Colour(168,255,200))
                case _:
                    self.fullNameTextCtrl.SetBackgroundColour(wx.NullColour)
                    self.psNameTextCtrl.SetBackgroundColour(wx.NullColour)
        else:
            self.fullNameTextCtrl.SetBackgroundColour(wx.NullColour)
            self.psNameTextCtrl.SetBackgroundColour(wx.NullColour)
        self.fullNameTextCtrl.Refresh()
        self.psNameTextCtrl.Refresh()

    def fileListListBoxOnSelection(self, event):
        fontFile = f"{self.openedFolder}/{event.EventObject.Items[event.EventObject.Selection]}"
        self.showInfo(fontFile)

    def fontSelectChoiceOnChange(self, event):
        # switching between the fonts in a collection
        fontFile = f"{self.openedFolder}/{self.fileListListBox.Items[self.fileListListBox.Selection]}"
        font = FontInfo(fontFile, fontNum=event.EventObject.Selection)
        self.familyTextCtrl.Value = str(font.fontFamily)
        self.typeTextCtrl.Value = str(font.fontSubfamily)
        self.weightTextCtrl.Value = str(font.fontWeight)
        self.fullNameTextCtrl.Value = str(font.fontFullname)
        self.versionTextCtrl.Value = str(font.fontVersion)
        self.psNameTextCtrl.Value = str(font.fontPostscript)
        self.openedFontType = font.fontType
        self.highlightFFName(self.openedFontType)
    
    def highlightCheckBoxOnClick(self, event):
        self.highlightFFName(self.openedFontType)
    
    def faceNameCopyButtonOnClick(self, event):
        # copies the full font face name to clipboard 
        # Flush() allows it to stay after the app is closed, but not in all cases: https://docs.wxwidgets.org/3.2.0/classwx_clipboard.html#a10997196ffd3b2cf8d823033f291f932
        if wx.TheClipboard.Open():
            match self.openedFontType:
                case FontType.TTF:
                    wx.TheClipboard.SetData(wx.TextDataObject(self.fullNameTextCtrl.Value))
                    wx.TheClipboard.Flush()
                case FontType.OTF:
                    wx.TheClipboard.SetData(wx.TextDataObject(self.psNameTextCtrl.Value))
                    wx.TheClipboard.Flush()
                case _:
                    errDlg = wx.MessageDialog(self, f"Valid font type has not been detected.\nNothing was copied.", "Info", wx.OK | wx.ICON_INFORMATION)
                    errDlg.ShowModal()
            wx.TheClipboard.Close()

    def openFileButtonOnClick(self, event):
        extWithAsterisk = ["*" + s for s in FILEEXT]
        extLine = ", ".join(extWithAsterisk)
        extCard = ";".join(extWithAsterisk)
        with wx.FileDialog(self, "Open font file", wildcard=f"Font files ({extLine})|{extCard}", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
            try:
                with open(path, 'rb') as file:
                    self.openedFolder = os.path.dirname(file.name)
                    self.fileListListBox.Clear()
                    self.fileListListBox.Append(os.path.basename(file.name))
                    self.fileListListBox.SetSelection(0)
                    self.showInfo(path)
                    self.openedFolderLabel.SetLabel(f"Current file: {path}")
            except IOError:
                errDlg = wx.MessageDialog(self, f"Cannot open file {path}", "Error", wx.OK | wx.ICON_ERROR)
                errDlg.ShowModal()
                return

    def openFolderButtonOnClick(self, event):
        with wx.DirDialog(self, "Open font folder", style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as folderDialog:
            if folderDialog.ShowModal() == wx.ID_CANCEL:
                return
            self.openedFolder = folderDialog.GetPath()
            self.fileListListBox.Clear()
            self.openedFolderLabel.SetLabel(f"Current folder: {self.openedFolder}")
            for file in os.listdir(self.openedFolder):
                if any(file.lower().endswith(x) for x in FILEEXT):
                    self.fileListListBox.Append(file)
            if len(self.fileListListBox.Items) > 0:
                self.fileListListBox.SetSelection(0)
                fontFile = f"{self.openedFolder}/{self.fileListListBox.Items[0]}"
                self.showInfo(fontFile)

    def openSystemFontsButtonOnClick(self, event):
        self.openedFolder = "C:\\Windows\\Fonts"
        self.fileListListBox.Clear()
        self.openedFolderLabel.SetLabel(f"Current folder: {self.openedFolder}")
        for file in os.listdir(self.openedFolder):
            if any(file.lower().endswith(x) for x in FILEEXT):
                self.fileListListBox.Append(file)
        if len(self.fileListListBox.Items) > 0:
            self.fileListListBox.SetSelection(0)
            fontFile = f"{self.openedFolder}/{self.fileListListBox.Items[0]}"
            self.showInfo(fontFile)

def getNameInfo(nameId, nametable):
    # returns name from the font nametable, using Windows platform ID and Unicode BMP encoding ID
    # more info about the IDs: https://learn.microsoft.com/en-us/typography/opentype/spec/name#platform-encoding-and-language-ids
    return nametable.getName(nameId, 3, 1)

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()
