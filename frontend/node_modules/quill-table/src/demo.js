window.Quill = require('quill');
const quillTable = require('./index.js');

Quill.register(quillTable.TableCell);
Quill.register(quillTable.TableRow);
Quill.register(quillTable.Table);
Quill.register(quillTable.Contain);
Quill.register('modules/table', quillTable.TableModule);

import 'quill/dist/quill.core.css';
import 'quill/dist/quill.snow.css';
import './css/quill.table.css';

const maxRows = 10;
const maxCols = 5;
const tableOptions = [];
for (let r = 1; r <= maxRows; r++) {
    for (let c = 1; c <= maxCols; c++) {
        tableOptions.push('newtable_' + r + '_' + c);
    }
}

const defaultToolbar = [
    [{table: tableOptions}, {table: 'append-row'}, {table: 'append-col'}],
    ['bold', 'italic', 'underline', 'strike'],
    ['blockquote', 'code-block', 'image'],

    [{'list': 'ordered'}, {'list': 'bullet'}],

    [{'indent': '-1'}, {'indent': '+1'}],
    [{'header': [1, 2, 3, 4, 5, 6, false]}],

    [{'color': []}, {'background': []}],
    [{'font': []}],
    [{'align': []}],

    ['clean']
];
const Editor = new Quill(document.getElementById('quillContainer'), {
        modules: {
            toolbar: defaultToolbar,
            table: true
        },
        placeholder: '',
        theme: 'snow',
        readOnly: false,
    }
);