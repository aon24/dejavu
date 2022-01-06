//
//
//
window.sovaActions = window.sovaActions || {};
window.sovaActions.v_track = {
	init: doc => {
		let avatarParams = {
			pageName: 'avatar',
			className: 'avatar',
			avatar: true,
			frameStyle: {display: 'none'},
		};
		doc.util.addChildPage(doc, avatarParams);
	},
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
		createTrack: doc => {
			doc.setField('createTrack', 1);
			doc.cmdSave();
		},
    },
    //*** *** ***

	hide: {
		btnOpen: doc => !doc.getField('trackCreated'),
		btnCrt: doc => doc.getField('trackCreated'),
		buttons: doc => ['read', 'preview'].includes(doc.rsMode),
	},
    
};













