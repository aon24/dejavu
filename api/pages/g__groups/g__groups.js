//
//
//

let bodyResize = doc => {
	let page = doc.sovaPagesByName['group'];
	if (page) {
		let r = document.getElementById('forChild').getBoundingClientRect();
		page.frameStyle.top = r.top;
		page.frameStyle.left = r.left;
		page.frameStyle.width = r.width;
		page.frameStyle.height = r.height-100;
		page.forceUpdate();
	}
};

let openGroup = (doc, dbaUnid) => {
//	console.log('openGroup', dbaUnid);
	if (dbaUnid) {
		let [dbAlias, unid] = doc.util.partition(dbaUnid, '&');
		let page = doc.sovaPagesByName['group'];
		if (page) {
			page.docProps.dbAlias = dbAlias;
			page.docProps.unid = unid;
			page.docProps.focus = 'groupName';
			page.forceUpdate();
		}
		else {
			let r = document.getElementById('forChild').getBoundingClientRect();
			let group = {
				docProps: {
					dbAlias: dbAlias,
					unid: unid,
					focus: 'groupName',
				},
				pageName: 'group',
				withoutHat: true,
				rsMode: 'admin',
				frameStyle: {top: r.top, left: r.left, width: r.width, height: r.height-100}
			};
			doc.util.addChildPage(doc, group);
		}
	}
};

// *** *** ***

window.sovaActions = window.sovaActions || {};
window.sovaActions.g__groups = {
	init2: doc => {
		let r = document.getElementById('forChild').getBoundingClientRect();
		let group = {
			pageName: 'group',
			withoutHat: true,
			rsMode: 'admin',
			frameStyle: {top: r.top, left: r.left, width: r.width, height: r.height-100}
		};
		doc.util.addChildPage(doc, group);

		window.resizeObserver = new ResizeObserver( () => bodyResize(doc) );
		window.resizeObserver.observe(document.querySelector('body'));
	},
    //*** *** ***
  
    recalc: {
        CAT: doc => doc.changeDropList('SUBCAT'),
        SUBCAT: (doc, label, opt, i) => doc.setField('viewGroups', {cat: doc.getField('CAT'), subCat: label || ''}),
    },
    // *** *** ***
	
	querySave: doc => { // заполнить нужные поля перед сохранением
//		let setPageDoc = doc.sovaPagesByName['setting'].doc;
//		['pageName', 'pageUrl', 'pageCat', 'notes'] // colorHist берем из гл. док.
//			.forEach( it => doc.setField( it, setPageDoc.getField(it) ) );
	},
	// *** *** ***
	
    cmd: {
        openInDiv: (doc, dbaUnid) => openGroup(doc, dbaUnid),
		viewLoaded: (doc, par) => {
			let [xName, dbaUnid] = doc.util.partition(par, '|');
			openGroup(doc, dbaUnid);
		},
    },
    //*** *** ***

	hide: {
//		redo: doc => doc.rootBox && !doc.rootBox.hideRedo(),
	},
    
};













