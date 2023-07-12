//
// AON 2020
//
// *** *** ***

window.sovaActions = window.sovaActions || {};
window.sovaActions.js_to_react = {
    init2: doc => {
        doc._oPol = JSON.parse(doc.getField('_polygon_fd'))[0];
        setInterval( window._prism, 50);
    },
    // ***
    
    cmd: {
        showPy: (doc, fil) => {
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
        
        showFile: (doc, param) => {
            let [newForm, fil] = doc.util.partition(param, '|');
            let main = window.sovaPages.main.doc;
            let url = '/api.post?apiShowFile&&' + fil.replace(/ /g, '');
            doc.util.doPost(doc, url, '')
                .then( plainTx => {
                    if (window.sovaPages[newForm]) {
                        window.sovaPages[newForm].minimized = false;
                        window.sovaPages[newForm].doc.setField('tx', plainTx);
                        doc.zIndex = newForm;
                        doc.forceUpdate();
                    }
                    else {
                        window.sovaPages[newForm] = { preloadData: {'TX': plainTx} };
                        doc.util.addSimlePage(doc, newForm, fil);
                    }
                })
                .catch( mess => console.log('File not loaded: ', fil, mess) );
        },
    },
};

// *** *** ***

window.sovaActions.z_react = { maxPage: _ => 'newdoc?M&z_react'};
window.sovaActions.z_showpy = { maxPage: _ => 'newdoc?M&z_showpy'};

// *** *** ***
