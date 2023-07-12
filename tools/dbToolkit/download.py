# -*- coding: utf-8 -*-

from tools.first import err, BASE_DIR
from tools.checkRights import notReader
from tools.dbToolkit.Book import docFromDB
from tools.httpMisc import urlKeys

import zlib
import os

# *** *** ***

def downloadFile(request):

    def _err(s):
        err(s, cat='error-download.py')
        return 400, None, s

    dcUK = urlKeys(request, 'downloadFile')
    # if notReader(dcUK.dbAlias, dcUK.userName):
        # return _err(f'uploadFile: Access denied for user {dcUK.userName}')

    try:
        if not docFromDB(dcUK):
            return _err(f'Can not get document: dbAlias={dcUK.dbAlias}&unid={dcUK.unid}')

        path = os.path.join(BASE_DIR, 'DB', 'files')

        tm = None
        for k, v in dcUK.doc.items():
            if k.startswith('FILES') and k.endswith(dcUK.idbl):
                tm = v.split('|')[5].split()[0]
                break
        if not tm:
            return _err(f'Invalid file-id: "{dcUK.idbl}"')

        fullname = os.path.join(path, tm, f'{dcUK.doc.ref or dcUK.doc.unid}_{dcUK.idbl}')
        with open(fullname, 'rb') as f:
            buf = f.read()

        if not buf:
            return _err('Zero-length file')

        if dcUK.fzip == 'Z':
            buf = zlib.decompress(buf)

        if 'charset' not in dcUK.mimetype and dcUK.utf:
            dcUK.mimetype += '; charset=UTF-8'

        return 200, dcUK.mimetype or 'Application/attachment', buf

    except Exception as ex:
        return _err(f'Exception (q={dcUK.query}): {ex}')

# *** *** ***
