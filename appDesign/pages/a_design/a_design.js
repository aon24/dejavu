//
//
//
window.sovaActions = window.sovaActions || {};
window.sovaActions.a_design = {
	init: doc => {
		let pageParams = {
			hide: true, // при закрытии не удалять, а скрывать
			dbAlias: 'dba',
			unid: 'unid',
			pageName: 'setting',
			rsMode: 'new',
			min: true,
			pont: true,
			smallCls: 'rightTop',
			newForm: 'a_setting',
			frameStyle: {top: 0, right: 15, width: 280, height: 'calc(100vh - 52px)'}//, display: 'none'}
		};
		let avatarParams = {
			pageName: 'avatar',
			className: 'avatar',
			avatar: true,
			frameStyle: {display: 'none'},
		};
		let pagePlus = {
			hide: true, // при закрытии не удалять, а скрывать
			dbAlias: doc.dbAlias,
			unid: doc.unid,
			pageName: 'plus',
			rsMode: 'read',
			fieldValues: {_page_: '1', form: 'plus'},
			min: true,
			max: false,
			pont: true,
			smallCls: 'leftTop',
			frameStyle: {top: 0, left: 0, width: 1, height: 25, minHeight: 375}, //, display: 'none'},
			children: [
				{ _teg: 'div', attributes: {className: 'pagePlus'}, children: [{_teg: 'div'}] },
				{field: [ 'pgDown', 'band', ['','','','','','','',''] ], attributes: {className: 'pageDown'} }
			],
		};
		doc.util.addChildPage(doc, pageParams);
		doc.util.addChildPage(doc, pagePlus);
		doc.util.addChildPage(doc, avatarParams);
	},
    //*** *** ***
  
    recalc: {
        //SUBCAT: (doc, label, opt, i) => doc.setField( 'view1', doc.getField('cat') + '|' + (i ? label : '') ),
    },
    // *** *** ***
	
	querySave: doc => { // заполнить нужные поля перед сохранением
		let setPageDoc = doc.sovaPagesByName['setting'].doc;
		['pageName', 'pageUrl', 'pageCat', 'notes'] // colorHist берем из гл. док.
			.forEach( it => doc.setField( it, setPageDoc.getField(it) ) );
	},
	// *** *** ***
	
    cmd: {
        undo: doc => doc.rootBox.cmdUndo(),
        redo: doc => doc.rootBox.cmdRedo(),
        
        setting: doc => {
			doc.settingIsOpen = true;
			let setPage = doc.sovaPagesByName['setting'];
			setPage.title = 'Параметры страницы';
			setPage.frameStyle.display = 'block';
			
			// box.histDisable = true; // запретить toHist во время setField
			
			setPage.doc.setField('showSetting', 'setPage');
			
			// box.histDisable = null; // разрешить toHist

			setPage.doc.box = doc.pageBox;
			setPage.forceUpdate();
        },
		
		pageBlur: (doc, pageName, e) => {
			if (pageName === 'setting')
				doc.settingBox = null;
		},
		pageHide: (doc, pageName) => {
			if (pageName === 'setting')
				doc.settingBox = doc.settingIsOpen = null;
		},

    	showSetBox: (doc, box) => {
			let setPage = doc.sovaPagesByName['setting'];
			setPage.doc.box = box;
			setPage.title = 'Свойства блока';
			setPage.frameStyle.display = 'block';

			// box.histDisable = true; // запретить toHist во время setField

			setPage.doc.setField('showSetting', 'setBox');
			setPage.doc.setField('boxNo_FD', box.boxIndex.toString());

			let [tuning, rtr] = [box.tuning, (box.parentBox || box).tuning];
			[
				'bgStyle', 'backgroundImage', 'bgiSizeX', 'bgiSizeY', 'repeatX', 'repeatY', 'border',
				'backgroundColor', 'gradientColor', 'gradientDeg', 'gradient',
				'shadow', 'shadowX', 'shadowY', 'shadowR', 'shadowW', 'shadowColor',
				'hide0', 'hide1', 'hide2', 'hide3', 'hide4', 'bgiSizeX_metric', 'bgiSizeY_metric',
				'insideOnly', 'boxSizing', 'boxLayer', 'comment', 'borderSide', 'fixed', 'name',
				'skewX', 'skewY', 'rotateX', 'rotateY', 'translateX', 'translateY', //'marginTD', 'marginLR', 'marginLR_metric', 'marginTD_metric',
				'anchor', 'noIcons'
			].forEach( it => setPage.doc.setField(it, tuning[it] || '') );

			['scaleX', 'scaleY'].forEach( it => setPage.doc.setField(it, tuning[it] || '1') );

			['textOrButton', 'buttonAction', 'gridX|27',
				'textAlign', 'fontSize|40', 'fontFamily|Verdana', 'letterSpacing|0', 'lineHeight|1.0', 'fontStyle', 'fontWeight', 'color|#000000ff',
				'paddingLR|10', 'paddingTD|0', 'fontSize_metric', 'letterSpacing_metric', 'paddingLR_metric', 'paddingTD_metric',
				'textIndent|10', 'textIndent_metric'
			].forEach( it => { let [f, v] = doc.util.partition(it, '|'); setPage.doc.setField(f, tuning[f] === undefined ? v : tuning[f]); } );

			['', 'Top', 'Right', 'Bottom', 'Left']
				.forEach( side => [`border${side}Radius`, `border${side}Radius_metric`, `border${side}Width`, `border${side}Style`, `border${side}Color`]
					.forEach( it => setPage.doc.setField(it, tuning[it] || '') )
				);
			
				//console.log(box.boxIndex, box.rect.width);
			tuning.boxSizeX = box.rect.width;
			tuning.boxSizeY = box.rect.height;
			setPage.doc.setField('boxSizeX', box.rect.width);
			setPage.doc.setField('boxSizeY', box.rect.height);
			if (box.parentBox) {
				setPage.doc.setField('boxSizeXp', ` ${(box.rect.width  / box.parentBox.rect.width * 100).toFixed(2)}%` );
				setPage.doc.setField('boxSizeYp', ` ${(box.rect.height  / box.parentBox.rect.height * 100).toFixed(2)}%` );
				setPage.doc.setField('showAnchor', `b_${box.boxIndex}`);

				let fl = box.floating && box.parentBox.boxes.length > 1;
				
				setPage.doc.setField('showZI', fl);
				fl && setPage.doc.setField('boxLayer', box.parentBox.floatBoxes.indexOf(box).toString());
			}
			
			// box.histDisable = null; // разрешить toHist

			
			doc.settingIsOpen = true;
			setPage.forceUpdate();
		},
    },
    //*** *** ***

	hide: {
		undo: doc => doc.rootBox && !doc.rootBox.hideUndo(), // если надо запретить undo, поверх него показвается div с className="tb-disable"
		redo: doc => doc.rootBox && !doc.rootBox.hideRedo(),
	},
    
};













