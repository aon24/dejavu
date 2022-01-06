
// *** *** ***
//
// aon 2021
//
// *** *** ***

window._pyramid = main => {
	let _oPol = JSON.parse(main.getField('_polygon_fd'))[0];
	let pi_3 = [0, -1*Math.PI/3, -2*Math.PI/3, -Math.PI, -4*Math.PI/3, -5*Math.PI/3, 0];
	let _grad = Math.PI/180;
	let [_h, r, _u, _cx, _cy] = [0, 0, 0.0, 40, 50];

	let _pyraLoop = () => {
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
	
	setInterval( () => _pyraLoop(), 50);
};
