//
//
//

window.sovaActions = window.sovaActions || {};
window.sovaActions.a_form = {
	init2: doc => {
	},
    //*** *** ***
  
    recalc: {
        SUBCAT: (doc, label, opt, i) => doc.setField( 'view1', doc.getField('cat') + '|' + (i ? label : '') ),
    },
    // *** *** ***
	
	querySave: doc => { // заполнить нужные поля перед сохранением
	},
	// *** *** ***
	
    cmd: {
		publish: doc => {},
	},
	// *** *** ***

	hide: {
		undo: doc => doc.rootBox && !doc.rootBox.hideUndo(), // если надо запретить undo, поверх него показвается div с className="tb-disable"
		redo: doc => doc.rootBox && !doc.rootBox.hideRedo(),
	},

};
