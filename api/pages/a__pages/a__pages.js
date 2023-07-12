let [_pageX, _pageY] = [50, 0];

window.sovaActions = window.sovaActions || {};
window.sovaActions.a__pages = {
    init: doc => doc.changeDropList('SUBCAT'),
	
    init2: doc => window._pyramid(doc),
	
    //*** *** ***

    recalc: {
        CAT: doc => doc.changeDropList('SUBCAT', null, -2), // -2, чтобы работало поле list
        SUBCAT: (doc, label, opt, i) => doc.setField('viewPages', {cat: doc.getField('CAT'), subCat: label || ''}),
    },
	// *** *** ***
	
    cmd: {
		xopen_: (doc, dba) => {
			let kv = doc.util.urlKeys(dba);
            let view = doc.register['ViewPages'.toUpperCase()];
            view.rowClick(kv.unid);
			
			doc.util.xopen(`opendoc?${dba}`);
		},
		viewLoaded: (doc, par) => {
			let [xName, dba] = doc.util.partition(par, '|');
			let [dbAlias, unid] = doc.util.partition(dba, '&');
			doc.changeDropList('subCat');
//			doc.changeDropList('subCat', ['new','List'], 1);
			
		},
		realTime: (doc, dba) => {
			let kv = doc.util.urlKeys(dba);
            let view = doc.register['ViewPages'.toUpperCase()];
            view.rowClick(kv.unid);

			let p = doc.sovaPagesByName[kv.unid];
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
		
		showHostAdr: doc => doc.msg.box(`\n${doc.getField('hostAddress_FD')}\n\nПерейдите по ссылке и откройте нужную страницу кнопкой "Real time".`,
'Адрес сервера|Для ослеживания изменений в режиме реального времени вы можете подключиться к серверу с другого устройства по указанному ниже адресу.')
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

		toArchive: (doc, dba) => {
            let kv = doc.util.urlKeys(dba);
            let view = doc.register['ViewPages'.toUpperCase()];
            view.rowClick(kv.unid);
            let row = view.selectedDoc;
            doc.msg.box('Удалить выбранный документ?', 'Удаление', ['Да+|Y', 'Нет'])
				.then( () => {
				    doc.util.serverAction(doc, `toArchive?${dba}`)
						.then( () => view.loadView(true) ) // refresh true
						.catch({}); // serverAction call doc.msg.error(e)
				})
				.catch( () => {});
        },

// *** *** ***
// console.log(row);

    	logoff: doc => { window.location.href = '/logoff' },
		// ***
        previewNew: (doc, param) => {
            let kv = doc.util.urlKeys(param);
            let view = doc.register['ViewPages'.toUpperCase()];
            view.rowClick(kv.unid);
            doc.previewNew(param);
		},
		// ***
		xcopy: (doc, dba) => {
            let kv = doc.util.urlKeys(dba);
            let view = doc.register['ViewPages'.toUpperCase()];
            view.rowClick(kv.unid);
            doc.msg.box('Сделать копию выбранного документа?', 'Дублирование', ['Да+|Y', 'Нет'])
				.then( () => {
				    doc.util.serverAction(doc, `duplicate?${dba}`)
						.then( () => view.loadView(true) ) // refresh true
						.catch({}); // serverAction call doc.msg.error(e)
				})
				.catch( () => {});
		},
		// ***
        copy: (doc, unid) => {
            let act = ['copy?' + doc.dbAlias, unid].join('&');
            
            doc.util.serverAction(doc, act)
                .then( _ => doc.msg.box('Агент успешно запущен', 'Запуск сбора отчета') )
                .catch( e => doc.msg.error(e) );
        },
    },
};
// *** *** ***














