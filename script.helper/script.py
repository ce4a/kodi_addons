# -*- coding: utf-8 -*-
"script.helper"
import sys
import json
import xbmc
import xbmcaddon
import xbmcgui

#kodi-send -a 'RunScript("script.helper", passthrough)'
# add to keymap.xml
# <key id="XXX">RunScript("script.helper", passthrough)</key>

__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
__addonid__ = __addon__.getAddonInfo('id')
__cwd__ = __addon__.getAddonInfo('path').decode('utf-8')
__icon__ = __cwd__ + '/icon.png'

#datapath = xbmc.translatePath(ADDON.getAddonInfo('profile')).decode('utf-8')
#addonfolder = xbmc.translatePath(ADDON.getAddonInfo('path')).decode('utf-8')
#__debug__ = ADDON.getSetting('debug_mode')

class RPC(object):
    "RPC"
    def __init__(self):
        self._mid = 0

    def _id(self):
        self._mid += 1
        return self._mid

    def execute(self, method, *args, **kwargs):
        "execute"
        if len(args) == 1:
            args = args[0]
            params = kwargs # Use kwargs for param=value style
        else:
            args = kwargs
        params = {}
        params['jsonrpc'] = '2.0'
        params['id'] = self._id()
        params['method'] = method
        params['params'] = args

        cmd = json.dumps(params)
        #_log('RPC: execute %s'%(cmd))
        res = xbmc.executeJSONRPC(cmd)
        #_log('RPC: result %s'%(res))
        ret = json.loads(str(res))
        if 'error' in ret:
            _log('RPC ERROR: %s'%(ret['error']), xbmc.LOGWARNING)
            return None
        return ret['result']

def _log(message, level=xbmc.LOGNOTICE):
    xbmc.log(msg='%s: %s' % (__addonid__, message), level=level)

def _passthrough():
    rpc = RPC()
    ret = rpc.execute('Settings.GetSettingValue', {'setting':'audiooutput.passthrough'})
    passthrough = not ret['value']
    params = {'setting':'audiooutput.passthrough', 'value':passthrough}
    ret = rpc.execute('Settings.SetSettingValue', params)
    #_log('RPC: result %s'%(ret))
    if passthrough:
        msg = 'enabled'
    else:
        msg = 'disabled'
    _log('RPC: Passthrough %s'%(msg))
    xbmcgui.Dialog().notification(__addonname__, 'Passthrough: %s'%msg, __icon__, 3000)

def _main():
    args = len(sys.argv)

    cmd = None
    data = None
    if args > 1:
        cmd = sys.argv[1]
        if args > 2:
            data = sys.argv[2]
    if cmd == 'passthrough':
        _passthrough()
    else:
        _log('cmd=%s, data=%s'%(cmd, data))

if __name__ == '__main__':
    _main()
