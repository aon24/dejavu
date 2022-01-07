window.sovaActions = window.sovaActions || {};
window.sovaActions.ilog = {
    recalc: {
        CAT: (doc, label) => {
			doc.changeDropList('SUBCAT');
		},
        SUBCAT: (doc, label) => getLogData(doc, doc.getField('cat') + '|' + label),
		LOG_0_6: (doc, num) => getLogData(doc, `&log=${num}`, true),
    }
};

// *** *** ***

let getLogData = (doc, keys, recalc) => {
    fetch(`api.get/getData?form=ilog&key=${keys}`, {method: 'get', credentials: 'include'})
        .then( response => response.text() )
        .then( txt => recalc ? doc.changeDropList('SUBCAT') : doc.setField('msg', txt) )
        .catch( err => doc.setField('msg', err.message) );
};

// *** *** ***












