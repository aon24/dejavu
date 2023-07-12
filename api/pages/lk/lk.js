//
//
//
window.sovaActions = window.sovaActions || {};
window.sovaActions.lk = {
	init: doc => {},
	//*** *** ***

	recalc: {
		CAT_FD: doc => doc.changeDropList('SUBCAT_FD'),
		SUBCAT_FD: (doc, label, opt, i) => doc.setField( 'view1', doc.getField('cat_fd') + '|' + (i ? label : '') ),
	},
	// *** *** ***

	querySave: doc => { // заполнить нужные поля перед сохранением
//		let setPageDoc = doc.sovaPagesByName['setting'].doc;
//		['pageName', 'pageUrl', 'pageCat', 'notes'] // colorHist берем из гл. док.
//			.forEach( it => doc.setField( it, setPageDoc.getField(it) ) );
	},
	// *** *** ***
	
	cmd: {
//        undo: doc => doc.rootBox.cmdUndo(),
	},
	//*** *** ***

	hide: {
//		redo: doc => doc.rootBox && !doc.rootBox.hideRedo(),
	},
    
};













