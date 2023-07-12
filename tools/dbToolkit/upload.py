# -*- coding: utf-8 -*-

from tools.common import now
from tools.first import err, BASE_DIR
from tools.httpMisc import urlKeys

from tools.checkRights import notEditor
# from .Book import getDB

import zlib, uuid, os

_noCompress = b'compressed|.jpg|.jpeg|.gif|.pdf|.png|.arj|octet-stream|.zip|.rar|.7z|.dll|.exe|.avi|.mkv|.mp3|.mp4'.split(b'|')

# *** *** ***

def uploadFile(request):

    def _err(s):
        err(s, cat='error-upload.py')
        return 400, None, s

    dcUK = urlKeys(request, 'uploadFile')
    # if notEditor(dcUK.dbAlias, dcUK.userName):
        # return _err(f'uploadFile: Access denied for user {dcUK.userName}')

    try:

        ln = int(dcUK.length, 10)
        buf = dcUK.input.read(ln)

        tm = f"{now('-')}_{dcUK.date_crt}"

        i = buf.find(b'\r\n\r\n', 0, 1000)
        if i < 0:
            return _err('invalid rfile-header')

        i += 4
        rfileHeader = buf[:i]
        hLen = rfileHeader.find(b'\r\n')
        ln -= i + hLen + 4

        if any(c in rfileHeader for c in _noCompress) or ln > 10000000:
            bf = buf[i:i + ln]
            fzip = '0'
        else:
            bf = zlib.compress(buf[i:i + ln])
            fzip = 'Z'

        path = os.path.join(BASE_DIR, 'DB', 'files', tm.split()[0])
        os.makedirs(path, exist_ok=True)

        idbl = uuid.uuid4().hex.upper()
        with open(os.path.join(path, f'{dcUK.unid}_{idbl}'), 'bw') as f:
            f.write(bf)

        return 200, None, '&'.join([idbl, 'default', tm, fzip])

    except Exception as ex:
        return _err(f'Exception: {ex}')

# *** *** ***
