// *** *** ***
//
// aon 2022
//
// *** *** ***

window.sovaActions = window.sovaActions || {};
window.sovaActions.img = {
	cmd: {
		oneImg: (doc, img) => {
			let setPage = doc.mainDoc.sovaPagesByName['settingColors'];
			let docSP = setPage.doc;
			let box = doc.mainDoc.settingBox;
			if (box) {
				docSP.setField('backgroundImage', img);
				box.clip.toHist(box, 'tuning', 'backgroundImage');
			}
			else {
				docSP.setField('backgroundImageWP', img);
				docSP.rootBox.clip.toHist(docSP.rootBox, 'tuning', 'backgroundImageWP');
			}
			doc.page.closePage();
		},
		chDir: (doc, path) => {
			let tabHeader = doc.getField('_TABHEADER') || 0;
			let pageName = 'Pictures';
			let page = doc.mainDoc.sovaPagesByName[pageName];
			page && page.closePage();
			let rect =doc.util.getRect(doc.mainDoc, 80, 80);
			rect.width = Math.min(rect.width, 1200);
			let img = {
				dbAlias: 'dba',
				unid: 'unid',
				pageName,
				title: `${pageName}: ${path}`,
				rsMode: 'preview',
				min: true,
				newForm: `img&key=${path}&tabHeader=${tabHeader}`,
				frameStyle: rect,
				modal: 1,
			}
			doc.util.addChildPage(doc.mainDoc, img);
		},
	}
};