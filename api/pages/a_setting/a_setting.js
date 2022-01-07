// *** *** ***

window.sovaActions = window.sovaActions || {};
window.sovaActions.a_setting = {
	init2: doc => {
		doc.page.title = 'Параметры страницы';
		doc.page.frameStyle.display = 'block';

		let mainDoc = doc.page.props.owner;
		mainDoc.settingIsOpen = true;
		doc.setField('_page_', '1'); // _page_ === 1, означает, что это страница, а не документ и сохранять ее не надо
		doc.setField('showSetting', 'setPage');
		['docNo', 'pageName', 'pageUrl', 'pageCat', 'notes', 'created_FD', 'modified_FD', 'creator_FD', 'modifier_FD', 'published_FD', 'rainbow'] // colorHist берем из гл. док.
			.forEach( it => doc.setField( it, mainDoc.getField(it) ) );

		doc.box = mainDoc.pageBox; // pageBox - нулевой блок (служебный)
		['contur', 'screen', 'gridX', 'gridY'].forEach( it => doc.setField(it, doc.box.tuning[it] || '') );
		let screen = (doc.box.tuning['screen']/100) - 1; // номер экрана по умолчанию
		doc.setField('screen', screen);
		doc.setField('pagePlusDim', doc.box.boxes[screen].tuning.pagePlusDim || 2); // масштаб pagePlus
		doc.setField('_page_', 1); // blocking Esc
		mainDoc.forceUpdate();
	},
    //*** *** ***

    hide: {
		setBox: doc => doc.getField('showSetting')  !== 'setBox',
		setPage: doc => doc.getField('showSetting') !== 'setPage',
		gradient: doc => !doc.getField('gradient'),
		bgColor: doc => doc.getField('bgStyle') !== 'color' || doc.getField('hide1'),
		bgImage: doc => doc.getField('bgStyle') !== 'image' || doc.getField('hide1'),
		borEQ: doc => doc.getField('border') !== 'borEQ' || doc.getField('hide2'),
		borNE: doc => doc.getField('border') !== 'borNE' || doc.getField('hide2'),
		shadow: doc => !doc.getField('shadow') || doc.getField('hide3'),
		textStyle: doc => !doc.getField('textOrButton') || doc.getField('hide4'),
		borLeft: doc => doc.getField('borderSide'),
		borTop: doc => doc.getField('borderSide') !== 1,
		borRight: doc => doc.getField('borderSide') !== 2,
		borBottom: doc => doc.getField('borderSide') !== 3,
		boxStyle: doc => doc.getField('hide0'),
		hide1: doc => doc.getField('hide1'),
		hide2: doc => doc.getField('hide2'),
		hide3: doc => doc.getField('hide3'),
		hide4: doc => doc.getField('hide4'),
		zIndex: doc => !doc.getField('showZI'),
		//layer: doc => doc.box && !doc.box.box,
		insideOnly: doc => doc.box && !doc.box.box,
		
		rotate: doc => doc.getField('trans'),
		skew: doc => doc.getField('trans') !== 1,
		scale: doc => doc.getField('trans') !== 2,
		translate: doc => doc.getField('trans') !== 3,
		
		isButton: doc => doc.getField('textOrButton') !== 'showButton' || doc.getField('hide4'),
		actionText: doc => {
			let [b, ba] = [doc.getField('buttonAction'), doc.getField('buttonAction_alias')];
			return !b || ba === 'submit' || doc.getField('hide4');
		},
		showAnchor: doc => !doc.getField('anchor'),
    },
	//*** *** ***
	
	recalc: {
		'SCREEN': (doc, param) => {
			let screen = (doc.box.tuning.screen/100) - 1;
			let newBox = doc.box.changeScreen(param);
			if (newBox)
				doc.setField('pagePlusDim', newBox.tuning.pagePlusDim || 2);
		},
		'PAGEPLUSDIM': (doc, val, noHist) => {
			let screen = (doc.box.tuning.screen/100) - 1;
			let root = doc.box.floatBoxes[0] || doc.box.boxes[screen];
			root.tuning.pagePlusDim = val;
			doc.box.forceUpdate();
		},
	},
	cmd: {
		blPlus: doc => { // увеличить z-index
			let box = doc.box;
			let i = Number(doc.getField('boxLayer'));
			if ( i < box.parentBox.boxes.length - 1 ) {
				let t = box.parentBox.boxes[i+1];
				box.parentBox.boxes[i+1] = box.parentBox.boxes[i];
				box.parentBox.boxes[i] = t;
				t = box.parentBox.floatBoxes[i+1];
				box.parentBox.floatBoxes[i+1] = box.parentBox.floatBoxes[i];
				box.parentBox.floatBoxes[i] = t;
				doc.setField('boxLayer', (i+1).toString());
				box.pending = [box.toHist, 'tuning'];
				box.parentBox.forceUpdate();
			}
		},
		blMinus: doc => { // уменьшить z-index
			let box = doc.box;
			let i = Number(doc.getField('boxLayer'));
			if ( i ) {
				let t = box.parentBox.boxes[i-1];
				box.parentBox.boxes[i-1] = box.parentBox.boxes[i];
				box.parentBox.boxes[i] = t;
				t = box.parentBox.floatBoxes[i-1];
				box.parentBox.floatBoxes[i-1] = box.parentBox.floatBoxes[i];
				box.parentBox.floatBoxes[i] = t;
				doc.setField('boxLayer', (i-1).toString() );
				box.pending = [box.toHist, 'tuning'];
				box.parentBox.forceUpdate();
			}
		}
	},

};

// *** *** ***

let setBoxFeatureCheck = (doc, feature, val, noHist, toHist) => {
	let box = doc.box;
	
//	if (box.histDisable) // запретить toHist во время setField
//		return;
	
	if ( box && (box.tuning[feature] !== val || toHist === true) ) {
//console.log('setBoxFeatureCheck', feature, val );
		let v = box.testTuning(feature, val);
		if ( v ) {
//console.log('toHist:', toHist,feature, 'val:', val, 'box.tuning[feature]', box.tuning[feature], v, 'noHist', noHist, 'noHist === false', noHist === false);
			if ( v === true || v === val ) {
				box.tuning[feature] = val;
				if (noHist !== true) {
					//console.log('**************toHist:', typeof toHist, toHist,feature, val, box.tuning[feature]);
					//box.toHist('borderWidth');
					box.pending = [box.toHist, 'borderWidth'];
				}
				box.forceUpdate();
			}
			else
				doc.setField(feature, v); // setFied вызовет recalc еще раз, но toHist 
		}
	}
};

let setBoxFeature = (doc, feature, val, noHist, toHist) => {
	let box = doc.box;
//console.log(box.boxIndex, feature, val);
//	if (box.histDisable) // запретить toHist во время setField
//		return;

	if ( ['boxSizeX', 'boxSizeY'].includes(feature) )
		box.boxSizeTemp = true;
		//console.log('********* boxSizeX', val, box.boxIndex);

	if ( box && (box.tuning[feature] !== val || toHist === true) ) {
		let v = box.tuning[feature];
		box.tuning[feature] = val;
		if (noHist !== true) {
			//console.log('v === lf', val.slice(0,-1) === '\n');
//console.log('**************toHist:', feature, val, v, 'toHist', box.tuning[feature] !== val, toHist === true);
			box.pending = [box.toHist, 'tuning'];
		}
		box.forceUpdate();
		//setTimeout( () => box.forceUpdate(), 10);
	}
};

let recalc = window.sovaActions.a_setting.recalc;

// recalc  с перериcовкой settingPage (для chb/chb3), setBoxFeature возвращает undefined
['borderText', 'bgStyle', 'border', 'shadow', 'gradient', 'borderSide', 'trans', 'textStyle', 'textOrButton', 'buttonAction', 'anchor',
 'boxSizeX', 'boxSizeY',
 'hide0', 'hide1', 'hide2', 'hide3', 'hide4']
	.forEach(it => {recalc[it.toUpperCase()] = (doc, param, noHist, toHist) => setBoxFeature(doc, it, param, noHist, toHist) || doc.forceUpdate()} );

// recalc  без перериcовки settingPage
['backgroundImage', 'repeatX', 'repeatY', 'bgiSizeX', 'bgiSizeY',
 'shadowX', 'shadowY', 'shadowR', 'shadowW', 'shadowColor',
 'backgroundColor', 'gradientColor', 'gradientDeg', 'bgiSizeX_metric', 'bgiSizeY_metric',
 'insideOnly', 'boxSizing', 'boxLayer', 'comment', 'fixed', 'notes', 'noIcons',
 'skewX', 'skewY', 'rotateX', 'rotateY', 'scaleX', 'scaleY', 'translateX', 'translateY', //'marginTD', 'marginLR', 'marginLR_metric', 'marginTD_metric',
 ]
	.forEach( it => {recalc[it.toUpperCase()] = (doc, param, noHist, toHist) => setBoxFeature(doc, it, param, noHist, toHist)} );

// text features
[
 'color', 'textAlign', 'fontFamily', 'fontWeight', 'fontStyle', 'letterSpacing', 'lineHeight', 'fontSize',
 'paddingLR', 'paddingTD', 'fontSize_metric', 'letterSpacing_metric', 'paddingLR_metric', 'paddingTD_metric',
 'textIndent', 'textIndent_metric'
]
	.forEach( it => {recalc[it.toUpperCase()] = (doc, param, noHist, toHist) => setBoxFeature(doc, it, param, noHist, toHist)} );

// recalc для бордюра
['', 'Top', 'Right', 'Bottom', 'Left']
	.forEach( side => [`border${side}Radius`, `border${side}Radius_metric`, `border${side}Color`, `border${side}Style`]
		.forEach( it => {
				recalc[it.toUpperCase()] = (doc, param, noHist, toHist) => setBoxFeature(doc, it, param, noHist, toHist)
			}
		)
	);

// recalc для бордюра с проверкой ширины
['', 'Top', 'Right', 'Bottom', 'Left']
	.forEach( side => {	recalc[`border${side}Width`.toUpperCase()] = (doc, param, noHist, toHist) => setBoxFeatureCheck(doc, `border${side}Width`, param, noHist, toHist) });

// параметры страницы
['contur', 'gridX', 'gridY'].forEach( it => {recalc[it.toUpperCase()] = (doc, param, noHist, toHist) => setBoxFeature(doc, it, param, noHist, toHist)} );

// *** *** ***















