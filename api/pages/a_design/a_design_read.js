//
// aon 2022
//
// *** *** ***

window.sovaActions = window.sovaActions || {};
window.sovaActions.a_design = {
	recalc: {},
	cmd: {
		addFurniture: (doc, boxIndex) => {
			const errExit = s => {
				alert(s);
				doc.page.closePage();
			};

			let btn = doc.rootBox.findBoxByIndex(boxIndex); // btn - button
			if (!btn)
				return errExit('Ошибка в кнопке');
			
			let mmm, named;
			for (let it of btn.parentBox.floatBoxes) { // btn.parentBox - бокс в котором и кнопка, и мебель
				if (it.parent3d === it)
					mmm = it;
			}

			if (!mmm)
				return errExit('Мебель не найдена');


			let wall = doc.mainDoc.rootBox.findWrap(doc.mainDoc.rootBox);
			if (wall && wall.parent3d) {
				if (!wall.tuning.wall) // м.б. выбрана мебель
					wall = wall.parentBox;
				if (wall && wall.tuning.wall) { // wall-выбранная стена с надписью фар,лефт итд
					let s = JSON.stringify(wall.clip.copyCell(mmm, 'ctrl-C'));
					let mmmNew = JSON.parse(s);
					wall.clip.pasteFurniture(wall, mmmNew);
					return;
				}
			}
			return errExit('стена не выбрана');
		},
		
		// *** *** ***
		
		addWall: (doc, boxIndex) => {
			// кнопка "Вставить"
			// команда "winBal(Окно-балкон)". Ее нет ни питоне ни js, она создана в документе с формой a_designer
			// boxIndex === boxIndex кнопки. задается при формировании кнопки в boxTools.getContent()

			const errExit = i => {
				alert(`Стена не выбрана. Code ${i}`);
				doc.page.closePage();
			};

			let btn = doc.rootBox.findBoxByIndex(boxIndex); // btn - button
			if (!btn)
				return errExit(boxIndex);
			
			let mmm;
			for (let it of btn.parentBox.floatBoxes) // btn.parentBox - блок в котором и кнопка, и 3д
				if (it.tuning.mmm)
					mmm = it;

			if (!mmm)
				return errExit(2);


			let wall = doc.mainDoc.rootBox.findWrap(doc.mainDoc.rootBox);
			if ( !(wall && wall.parent3d && wall.tuning.wall) ) // wall-выбранная стена с надписью фар
				return errExit(3);

			wall.clip.toHist(wall, 'old:addM3t_wall');
			
			let s = JSON.stringify(wall.clip.copyCell(mmm, 'ctrl-C'));
			let wallNew = JSON.parse(s); // wallNew таблица из кирпичей

			wall.clip.delArrCells(wall); // убрать грани или всю таблицу для сложной стены

			let m = wall.parent3d.tuning.cm === mmm.tuning.cm ? 1 : mmm.tuning.cm ==='mm' ? 10 : 0.1;
			wall.rect.width *= m;
			wall.rect.height *= m;
			
			let _x = wall.rect.width > wallNew.rect.width ? wall.rect.width : wallNew.rect.width;
			let _y = wall.rect.height > wallNew.rect.height ? wall.rect.height : wallNew.rect.height;

			_x /= m;
			_y /= m;

			wall.rect.width = wallNew.rect.width;
			wall.rect.height = wallNew.rect.height;
			
			wall.type = wallNew.type;
			wall.cells = wallNew.cells || [];
			wall.boxes = wallNew.boxes || [];
			wall.tuning.m3key = 'm3table'; // чтобы отличать в refreshRoom()
			wall.tuning.wed = 0;
			wall.tuning.changed = 1;
			
			wall.tuning.cm = mmm.tuning.cm;
			wall.setScale(wall, wall.parent3d.tuning.cm, true);
			delete wall.tuning.cm;
			
			if (!wall.pending)
				wall.pending = () => {
					console.log(wall.rect.width, _x);
					wall.setBoxSize(_x, _y);
					wall.rebuild = 'wall';
					wall.pending = () => wall.clip.toHist(wall, 'new:addM3t_wall');
					wall.setWrap();
				};
			
			doc.page.closePage();
		},
	}
};

//console.log('XXXXXXXXX', wall.boxIndex); 












