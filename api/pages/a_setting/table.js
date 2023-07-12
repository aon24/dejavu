// *** *** ***

window.sovaActions.a_setting.hide.table = doc => doc.getField('table');

window.sovaActions.a_setting.cmd.crtTable = doc => {
	let rootBox = doc.box.doc.rootBox; // boxIndex = 100
	let ourBox = rootBox.floatBoxes[0]; // boxIndex = 1000
	if (ourBox.type === 'cols')
		return;
		
	// ***
	
	rootBox._tabSelItem_ = '0';
	let tableSize = doc.getField('tableSize');
	if (!tableSize)
		return;
	
	let [w_140, h_root] = [ourBox.rect.width, ourBox.rect.height];
	w_140 = Math.min(w_140/tableSize, 140);
	let h_header = 60;
	let lsh = [];
	let lsb = [];
	let t = rootBox.tuning.tableTuning;

	// ***

	let _border = {};
	['Top', 'Right', 'Bottom', 'Left'].forEach( side => {
		if ( !['Bottom', 'Left'].includes(side) )
			_border[`border${side}Radius`] = 10;
		_border[`border${side}Width`] = 2;
		_border[`border${side}Color`] = '#aaa';
		_border[`border${side}Radius_metric`] = 'px';
		_border[`border${side}Style`] = 0;
	});

	let tabTuning = {
		font: 'normal 16px Arial',
		padding: '4px 0px',
		textAlign: 'center',
		verticalAlign: 'middle',

		bgStyle: 'color',
		backgroundColor: '#f4f4f4',

		border: 'borNE',
		..._border,
	};
	
	let tabBody = {
		...tabTuning,
		backgroundColor: '#fff',
		borderTopWidth: 0,
		borderTopRadius: 0,
		borderRightRadius: 0,
	};
	let tabLast = {
		...tabTuning,
		bgStyle: null,
		borderTopWidth: 0, borderRightWidth: 0, borderLeftWidth: 0,
		borderBottomWidth: 2,
		borderBottomColor: '#aaa',
	};
	// ***

	let tabs = () => {
		let i = 0;
		for (; i < tableSize; i++) {
			lsh[i] = {
				key: Math.random(),
				rect: {width: w_140},
				className: 'tabItem',
				name: `TABLEHEADER_${i}`,
				tuning: tabTuning,
			};
			lsb[i] = {
				key: Math.random(),
				rect: {height: h_root - h_header, width: ourBox.rect.width, left: 0, top: 0},
				floating: true,
				className: 'tabBody',
				name: `TABLEBODY_${i}`,
				tuning: tabBody,
			};
		}

		if (ourBox.rect.width > i*w_140)
			lsh.push({
				tuning: tabLast,
				key: Math.random(),
				rect: {width: ourBox.rect.width - i*w_140}
			});
	};
	// ***

	ourBox.toHist(ourBox, 'oldRect_split', ourBox.boxIndex)
	tabs();
	
	let header = {key: Math.random(),
		rect: {height: h_header},
		type: 'cols',
		cells: lsh,
	};
	let body = {
		key: Math.random(),
		rect: {height: h_root - h_header},
		boxes: lsb,
	};
	
	let table = {name: '_table_', key: Math.random(),
		rect: {height: h_root},
		type: 'rows',
		cells: [header, body]
	};

	if (ourBox.cells.length) {
		ourBox.cells.unshift(table); // добавить в блок строку сверху
		ourBox.recalcHeight = h_root;
	}
	else { // разбить блок на 2 строки
		ourBox.recalcHeight = h_root + h_header;
		ourBox.type = 'rows';
		ourBox.cells[0] = table;
		ourBox.cells[1] = {rect: {height: h_header}, key: Math.random()};

		ourBox.cells[1].content = ourBox.content;
		ourBox.content = null;
	}

	ourBox.forceUpdate();
};

// *** *** ***
