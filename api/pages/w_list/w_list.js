//
//
//
window.sovaActions = window.sovaActions || {};
window.sovaActions.u_hunam = {
	init: doc => {},
    //*** *** ***
  
    recalc: {
        //SUBCAT: (doc, label, opt, i) => doc.setField( 'view1', doc.getField('cat') + '|' + (i ? label : '') ),
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













