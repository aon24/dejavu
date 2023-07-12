window.sovaActions = window.sovaActions || {};
window.sovaActions.irm = {
    init2: doc => window._pyramid(doc),
    cmd: {
		showHostAdr: doc => doc.msg.box(`\n${doc.getField('hostAddress_FD')}\n\nПерейдите по ссылке и откройте нужную страницу.`,
			'Адрес сервера|Вы можете подключиться к серверу с другого устройства по указанному ниже адресу.')
			.then(() => {}, () => {}),
	},
};