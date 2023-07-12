// *** *** ***

window.sovaActions = window.sovaActions || {};
window.sovaActions.a_settingLite = {
	init2: doc => {
		doc.page.title = 'Параметры страницы';
		doc.page.frameStyle.display = 'block';

		let mainDoc = doc.page.props.owner;
		mainDoc.settingLiteIsOpen = true;
		doc.setField('_page_', '1'); // // blocking Esc
		doc.setField('showSettingLite', 'arrow');
	},
    //*** *** ***

    hide: {
		setBox: doc => doc.getField('showSetting')  !== 'setBox',
    },
	//*** *** ***
	
	recalc: {
		'SCREEN': (doc, param) => {
			let newBox = doc.box.changeScreen(param);
			if (newBox)
				doc.setField('pagePlusDim', newBox.tuning.pagePlusDim || 2);
		},
	},
	//*** *** ***
	
	cmd: {
		copy3d: doc => doc.box.copyItem(),
	},

};
// *** *** ***

let recalcL = window.sovaActions.a_settingLite.recalc;

// *** *** ***

let testSBFL = (doc, feature, val, toHist) => {
	let box = doc.box;
	let p = box && box.tuning && (box.tuning[feature] !== val || toHist === true);
	if (p)
		return box;
};

// *** *** ***

let setBoxFeatureL = (doc, feature, val, noHist, toHist) => {
	let box = testSBF(doc, feature, val, toHist);
	if (box) {
		if (noHist !== true)
			box.toHistAfterRender = 'tuning';
		!box.noForceUpdate && box.forceUpdate();
	}
};

// *** *** ***
// recalc  с перериcовкой settingLite
['boxType', 'show3d',]
	.forEach(it => recalcL[it.toUpperCase()] = (doc, param, noHist, toHist) => setBoxFeatureL(doc, it, param, noHist, toHist) || doc.forceUpdate() );

// recalc  без перериcовки settingLite
[ 'coverOn','angleHide', ]
	.forEach( it => {recalcL[it.toUpperCase()] = (doc, param, noHist, toHist) => setBoxFeatureL(doc, it, param, noHist, toHist)} );

// *** *** ***















