let _oPol;
let [_pageX, _pageY] = [50, 0];
window.sovaActions = window.sovaActions || {};
window.sovaActions.a_main = {
    init: doc => doc.changeDropList('SUBCAT'),
	
    init2: doc => {
        _oPol = JSON.parse(doc.getField('_polygon_fd'))[0];
		main = doc;
        setInterval( () => _pyramid(doc), 50);
	},
    //*** *** ***

    recalc: {
        CAT: (doc, label, opt, i) => {
            doc.changeDropList('SUBCAT');
            doc.setField( 'view1', i && label );
        },
        SUBCAT: (doc, label, opt, i) => doc.setField( 'view1', doc.getField('cat') + '|' + (i ? label : '') ),
    },
	// *** *** ***
	
    cmd: {
		realTime: (doc, dba) => {
			let [dbAlias, unid] = doc.util.partition(dba, '&');
			let p = doc.sovaPagesByName[unid];
			if (p) {
				if (p.minimized) {
					p.frameStyle.transition = 'all 0.5s ease';
					p.minimized = false;
					setTimeout(_ => p.frameStyle.transition = 'none', 1000);
					p.forceUpdate();
				}
				else
					p.doc.onClick();
			}
			else {
				let pageParams = {
					dbAlias,
					unid,
					userName: doc.props.userName,
					pageName: unid,
					rsMode: 'read',
					min: true,
					max: true,
					pont: true,
					form: 'a_viewer', // чтобы открыть превью с другой формой
					smallCls: true,
					frameStyle: {top: _pageY, left: _pageX, width: 1000, height: 600}
				};
				_pageX += 30;
				_pageY += 30;
				doc.util.addChildPage(doc, pageParams);
			}
		},
		// ***
		
		showHostAdr: doc => doc.msg.box(`\n${doc.getField('hostAddress_FD')}\nПерейдите по ссылке и откройте нужную страницу кнопкой "Real time".`, 'Адреса сервера|Для ослеживания изменений в режиме реального времени'+
		' вы можете подключиться к серверу с другого устройства по любому из указанных ниже адресов.')
			.then(() => {}, () => {}),
		// ***
		
		publish: (doc, dba) => {
			doc.inputBox('Введите адрес страницы', text='', title='Публикация на сайте')
				.then( tx => {
					doc.util.serverAction(doc, `setFieldFromView?${dba}&field=${'published'}&value=${tx}`, '', true) // body='', silent=true
						.then( () => doc.msg.box('Агент успешно запущен', 'Запуск сбора отчета') )
						.catch( e => doc.msg.ok('Документ удален', 'Запись в базу') );
				})
				.catch( e => {});
		},


    	logoff: doc => { window.location.href = '/logoff' },
        copy: (doc, unid) => {
            let act = ['copy?' + doc.dbAlias, unid].join('&');
            
            doc.util.serverAction(doc, act)
                .then( _ => doc.msg.box('Агент успешно запущен', 'Запуск сбора отчета') )
                .catch( e => doc.msg.error(e) );
        },
    },
};
// *** *** ***

let pi_3 = [0, -1*Math.PI/3, -2*Math.PI/3, -Math.PI, -4*Math.PI/3, -5*Math.PI/3, 0];
let _grad = Math.PI/180;
let [_h, r, _u, _cx, _cy] = [0, 0, 0.0, 40, 50];

// *** *** ***

let _pyramid = main => {

	let ir = 4 + Math.floor((_u+25.)/60.);
	let ib = 4 + Math.floor(_u/60.);
	if ( ir >= 6 )
		ir -= 6;

	if ( ib >= 6 )
		ib -= 6;

    let [ls, x1, y1, ug] = [ [], [], [], _u*_grad ];

	pi_3.forEach( (u, i) => {
        let [x,y] = [Math.cos(u+ug), Math.sin(u+ug)];
        [x1[i], y1[i]] = [0.87*(x-y), 0.25*(-x-y)];
	});

    for (let i = 0; i < 6; i++) {
        ls[i+6] = [_cx+r*x1[i], _cy+r*y1[i], _cx, _cy-_h, _cx+r*x1[i+1], _cy+r*y1[i+1], 'rgba(176, 0, 0, 0.7)', '#faa'];
		ls[i]   = [_cx+r*x1[i], _cy+r*y1[i], _cx, _cy+_h, _cx+r*x1[i+1], _cy+r*y1[i+1], 'rgba(176, 229, 229, 0.7)', '#fff'];
	}
    
	_oPol.children.forEach( (it,j) => {
		let i = j;
		if ( j < 6 ) {
			i += ib;
			if ( i >= 6 )
				i -= 6;
		}
		else {
			i += ir;
			if ( i >= 12 )
				i -= 6;
		}
		it.attributes.points = `${ls[i][0]},${ls[i][1]} ${ls[i][2]},${ls[i][3]} ${ls[i][4]},${ls[i][5]}`;
		it.attributes.fill = ls[i][6];
		it.attributes.stroke = ls[i][7];
	});
	_h < 50 && _h++;
	r < 30 && r++;
	main.setField('polygon_fd', _oPol, 0);
	_u += 0.5;
    if (_u >= 360)
        _u = 0.0;
};















