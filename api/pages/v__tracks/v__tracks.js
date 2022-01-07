let [_pageX, _pageY] = [50, 0];

window.sovaActions = window.sovaActions || {};
window.sovaActions.v__tracks = {
    init: doc => doc.changeDropList('SUBCAT'),
	
    init2: doc => window._pyramid(doc),
	
    //*** *** ***

    recalc: {
        CAT: doc => doc.changeDropList('SUBCAT'),
        SUBCAT: (doc, label, opt, i) => doc.setField('viewTracks', {cat: doc.getField('CAT'), subCat: label || ''}),
    },
	// *** *** ***
	
    cmd: {
		realTime: (doc, dba) => {
		},
// *** *** ***
    },
};
// *** *** ***














