let tegStyle = document.createElement('style');
let dc = {};
let _el;

document.head.appendChild(tegStyle);

let setStyle = () => {
	let M = Math.min( document.documentElement.clientWidth / dc.targetW, 1 );
	_el.style.transform = `scale(${M}, ${M})`;
	_el.style.marginLeft = `${-dc.targetW*(1-M)/2}px`;
	_el.style.marginTop = `${-dc.targetH*(1-M)/2}px`;
	_el.style.width = `${dc.targetW}px`;
	_el.style.height = `${dc.targetH}px`;
};
// *** *** ***

screen.orientation.addEventListener('change', () => setTimeout( () => setStyle(), 100));

window.sovaActions = window.sovaActions || {};
window.sovaActions.a_viewer = {
    init2: doc => {
		_el = document.getElementById('a_viewer');
		let url = `ws://${doc.getField('webSocketServer_FD')}/html-viewer&${doc.unid}&${doc.props.userName}`;

		doc.webSocket = new WebSocket(url); // Hello Websocket, add me to the show list
		doc.webSocket.onmessage = mess => {
			let [head, sty, body] = mess.data.split('¤');
			head.split('&').forEach( it => {
				let [l, r] = doc.util.partition(it, '=');
				if (l)
					dc[l.trim()] = r.trim();
			});
			setStyle();
			_el.innerHTML = body;
			tegStyle.innerHTML = `div{overflow: hidden;}\n${sty}`;
		};
	},
};
// *** *** ***














