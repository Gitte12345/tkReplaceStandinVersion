# tkReplaceStandinVersion.py

from functools import partial 
import maya.cmds as cmds
import maya.mel as mel
import os
import json

'''
What it does:
    Replaces the version of the aiStandin path with the newVersion one.
    Be sure, the newVersion version exists on disc!

How to:
    - Select the standins you want to exchange.
    - Read Standin >> to check path and query the current version.
    - type in the desired newVersion version.
    - Replace Selected StandIns to adjust the path.

'''

def cHelp(*args):
    if cmds.window('win_tk_helpReplaceStandinVersion', exists=1):
            cmds.deleteUI('win_tk_helpReplaceStandinVersion')
    myWindow = cmds.window('win_tk_helpReplaceStandinVersion', s=1, t='help', wh=(200, 200))

    helpText = 'What it does:\n    Replaces the version of the aiStandin path with the newVersion one.\n    Be sure, the newVersion version exists on disc!\n\nHow to:\n    - Select the standins you want to exchange.\n    - Read Standin >> to check path and query the current version.\n    - type in the desired newVersion version.\n    - Replace Selected StandIns to adjust the path.'

    cmds.columnLayout(adj=1)
    cmds.text(helpText, al='left')
    cmds.showWindow(myWindow)


def cShrinkWin(windowToClose, *args):
    cmds.window(windowToClose, e=1, h=20)
    cmds.window(windowToClose, e=1, w=220)


def tkReadStandin(*args):
    path = ''
    mySel = cmds.ls(sl=1, l=0)
    if mySel[0]:
        if cmds.objectType(mySel[0], isType = 'aiStandIn'):
            path = cmds.getAttr(mySel[0] + '.dso')
        else:
            shps = cmds.listRelatives(mySel[0], s=1)
            for shp in shps:
                if cmds.objectType(shp, isType = 'aiStandIn'):
                    path = cmds.getAttr(shp + '.dso')

    if path:
        ass = path.split('/')[-1]
        cmds.textField('tfStandin', tx=ass, e=1)
        version = ass.split('_')[4][1:4]
        artist = ass.split('_')[5][0:3]
        print version
        print artist
        cmds.intField('ifStandinOldVersion', v=int(version), e=1)
        cmds.intField('ifStandinNewVersion', v=int(version), e=1)
        cmds.textField('tfStandinOldArtist', tx=artist, e=1)
        cmds.textField('tfStandinNewArtist', tx=artist, e=1)


def tkReplaceStandinVersion(action, *args):
    failList = []
    path = ''
    completePath = ''

    strOldArtist = cmds.textField('tfStandinOldArtist', tx=1, q=1)
    strNewArtist = cmds.textField('tfStandinNewArtist', tx=1, q=1)

    oldVersion = cmds.intField('ifStandinOldVersion', v=1, q=1)
    if oldVersion < 10:
        strOldVersion = 'v00' + str(oldVersion)
    elif oldVersion > 9 and oldVersion < 100:
        strOldVersion = 'v0' + str(oldVersion)
    else:
        strOldVersion = 'v' + str(oldVersion)

    newVersion = cmds.intField('ifStandinNewVersion', v=1, q=1)
    if newVersion < 10:
        strNewVersion = 'v00' + str(newVersion)
    elif newVersion > 9 and newVersion < 100:
        strNewVersion = 'v0' + str(newVersion)
    else:
        strNewVersion = 'v' + str(newVersion)

    mySel = cmds.ls(sl=1, l=1)

    for sel in mySel:
        if sel:
            if cmds.objectType(sel, isType = 'aiStandIn'):
                si = sel
                path = cmds.getAttr(sel + '.dso')
            else:
                shps = cmds.listRelatives(sel, s=1)
                for shp in shps:
                    if cmds.objectType(shp, isType = 'aiStandIn'):
                        path = cmds.getAttr(shp + '.dso')
                        si = shp

        filepath = path.split('/')[0:-1]

        for i in range(0, len(filepath)):
            completePath += filepath[i] + '/'

        filename = path.split('/')[-1]
        startingLetter = filename.split('/')[-1].split('_')[4]
        if startingLetter.startswith('v'):
            newVersionFilename = filename.replace(strOldVersion, strNewVersion)
            newVersionFilename = newVersionFilename.replace(strOldArtist, strNewArtist)
            replaceStandinText = completePath + newVersionFilename
            cmds.setAttr(si + '.dso', replaceStandinText, type = 'string')
        else:
            print 'version wrong'











def tkReplaceStandinVersionUI(*args):
    ver = 0.2
    colSilverGreen  = [0.33, 0.5, 0.33]
    colSilverRed    = [0.5, 0.39, 0.39]
    colSilverLight  = [0.39, 0.46, 0.50]
    colSilverDark   = [0.08, 0.09, 0.10]
    colSilverMid    = [0.23, 0.28, 0.30]
    windowStartHeight = 50
    windowStartWidth = 450
    bh1 = 22
    bh2 = 18
    if (cmds.window('win_tkReplaceStandinVersion', exists=1)):
        cmds.deleteUI('win_tkReplaceStandinVersion')
    myWindow = cmds.window('win_tkReplaceStandinVersion', t=('tkReplaceStandinVersion ' + str(ver)), s=1)
    
    cmds.columnLayout(adj=1, bgc=(colSilverMid[0], colSilverMid[1], colSilverMid[2]))
    cmds.frameLayout('flSwitchinstances', l='Replace Standin Version', bgc=(colSilverLight[0], colSilverLight[1], colSilverLight[2]), cll=1, cl=0, cc=partial(cShrinkWin, "win_tkReplaceStandinVersion"))
    cmds.columnLayout(adj=1)

    cmds.rowColumnLayout(bgc=(colSilverDark[0], colSilverDark[1], colSilverDark[2]), nc=2, cw=[(1,100), (2, 360)])

    cmds.button(l='Read Standin >>', c=partial(tkReadStandin, 'tfStandin'), bgc=(colSilverGreen[0], colSilverGreen[1], colSilverGreen[2]))
    cmds.textField('tfStandin', h=bh1, ed=0, bgc=(0, 0, 0))
    cmds.setParent('..')

    cmds.rowColumnLayout(bgc=(colSilverDark[0], colSilverDark[1], colSilverDark[2]), nc=5, cw=[(1,100), (2, 60), (3,100), (4, 60), (5, 140)])
    cmds.text(l='Replace Version', h=bh1, bgc=(colSilverLight[0], colSilverLight[1], colSilverLight[2]))
    cmds.intField('ifStandinOldVersion',  bgc=(0, 0, 0))
    cmds.text(l='With Version: ', h=bh1, bgc=(colSilverLight[0], colSilverLight[1], colSilverLight[2]))
    cmds.intField('ifStandinNewVersion', bgc=(0, 0, 0))
    cmds.text('', bgc=(colSilverLight[0], colSilverLight[1], colSilverLight[2]))


    cmds.text(l='Replace Artist', h=bh1, bgc=(colSilverLight[0], colSilverLight[1], colSilverLight[2]))
    cmds.textField('tfStandinOldArtist',  bgc=(0, 0, 0))
    cmds.text(l='With Artist: ', h=bh1, bgc=(colSilverLight[0], colSilverLight[1], colSilverLight[2]))
    cmds.textField('tfStandinNewArtist', bgc=(0, 0, 0))
    
    cmds.button(l='Replace Selected Standins', h=bh1, c=partial(tkReplaceStandinVersion), bgc=(colSilverRed[0], colSilverRed[1], colSilverRed[2]))
    cmds.setParent('..')
    cmds.button(l='Help', h=bh1, c=partial(cHelp))
    cmds.showWindow(myWindow)

tkReplaceStandinVersionUI()