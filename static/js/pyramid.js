window.onload = _ => {
    let pi_3 = [0, -1*Math.PI/3, -2*Math.PI/3, -Math.PI, -4*Math.PI/3, -5*Math.PI/3, 0];
    let _grad = Math.PI/180;
    let [_h, _r, _u, _cx, _cy] = [0, 0, 0.0, 65, 65];

    svg = document.getElementById('pyramid');
    let pyramid = Array.from(svg.children);

    setInterval( _ => { // start вращения
        let [x1, y1, ug] = [ [], [], _u*_grad];

        pi_3.forEach( (u, i) => {
            let [x,y] = [Math.cos(u+ug), Math.sin(u+ug)];
            [x1[i], y1[i]] = [0.87*(x-y), 0.25*(-x-y)];
        });

        let ls = [];
        let ir = 4 + Math.floor((_u+25.)/60.);
        let ib = 4 + Math.floor(_u/60.);
        if ( ir >= 6 )
            ir -= 6;

        if ( ib >= 6 )
            ib -= 6;

        for (let i = 0; i < 6; i++) {
            ls[i+6] = [_cx+_r*x1[i], _cy+_r*y1[i], _cx, _cy-_h, _cx+_r*x1[i+1], _cy+_r*y1[i+1], 'rgba(176, 0, 0, 0.7)', '#faa'];
            ls[i]   = [_cx+_r*x1[i], _cy+_r*y1[i], _cx, _cy+_h, _cx+_r*x1[i+1], _cy+_r*y1[i+1], 'rgba(176, 229, 229, 0.7)', '#fff'];
        }
        pyramid.forEach( (it,j) => {
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
            it.setAttribute("points", `${ls[i][0]},${ls[i][1]} ${ls[i][2]},${ls[i][3]} ${ls[i][4]},${ls[i][5]}`);
            it.setAttribute("fill", ls[i][6]);
            it.setAttribute("stroke", ls[i][7]);
        });

        _h < 60 && _h++;
        _r < 40 && _r++;
        
        _u += 0.5;
        if (_u >= 360)
            _u = 0.0;
    }, 50);
}