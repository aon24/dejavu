window.sovaActions = window.sovaActions || {};
window.sovaActions.info = {
    cmd: {
        tbHist: doc => {window.location.href='docopen?'+doc.dbAlias+'&'+doc.unid+'&read&history&Изменения'},
        tbProf: doc => {window.location.href='newdoc?' + doc.dbAlias + '&profile'},
    }
}