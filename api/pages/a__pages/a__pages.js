let [_pageX, _pageY] = [50, 0];

window.sovaActions = window.sovaActions || {};
window.sovaActions.a__pages = {
    init: doc => doc.changeDropList('SUBCAT'),
	
    init2: doc => window._pyramid(doc),
	
    //*** *** ***

    recalc: {
        CAT: doc => doc.changeDropList('SUBCAT'),
        SUBCAT: (doc, label, opt, i) => doc.setField('viewPages', {cat: doc.getField('CAT'), subCat: label || ''}),
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

// *** *** ***
		
//		openHtml: (doc, dba) => {},
		
// *** *** ***
		
		showPy: (doc, fil) => {
			let pageParams = {
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
            let main = window.sovaPages.main.doc;
            let url = '/api.post?apiShowPy&&' + fil.replace(/ /g, '');
            doc.util.doPost(doc, url, '')
                .then( jsTx => {
                    if (window.sovaPages[fil]) {
                        window.sovaPages[fil].minimized = false;
                        window.sovaPages[fil].doc.setField('tx', jsTx);
                        doc.zIndex = fil;
                        doc.forceUpdate();
                    }
                    else {
                        window.sovaPages[fil] = { preloadData: {'TX': jsTx} };
                        doc.util.addSimlePage(doc, fil, fil, 'z_showpy');
                    }
                })
                .catch( mess => console.log('File not loaded: ', fil, mess) );
        },

// *** *** ***

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














