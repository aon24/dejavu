// *** *** ***

window.sovaActions = window.sovaActions || {};
window.sovaActions.a_react = {
    init2: doc => {
		let url = `ws://${doc.getField('webSocketServer_FD')}/html-viewer&${doc.unid}&${doc.props.userName}`;
		doc.webSocket = new WebSocket(url); // Hello Websocket, add me to the show list
		doc.webSocket.onmessage = mess => console.log(mess.data) || doc.setField('react_fd', mess.data, Math.random());
	},
};
// *** *** ***














