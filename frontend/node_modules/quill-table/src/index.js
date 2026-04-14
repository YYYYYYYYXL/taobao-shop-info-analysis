import Quill from 'quill';
import Delta from 'quill-delta';
import TableCell from './js/TableCellBlot';
import TableRow from './js/TableRowBlot';
import Table from './js/TableBlot';
import Contain from './js/ContainBlot';
import './css/quill.table.css';
import TableTrick from "./js/TableTrick";

let Container = Quill.import('blots/container');

Container.order = [
    'list', 'contain',   // Must be lower
    'td', 'tr', 'table'  // Must be higher
];

class TableModule {
    constructor(quill, options) {
        let toolbar = quill.getModule('toolbar');
        toolbar.addHandler('table', function (value) {
            return TableTrick.table_handler(value, quill);
        });
        let clipboard = quill.getModule('clipboard');
        clipboard.addMatcher('TABLE', function (node, delta) {
            return delta;
        });
        clipboard.addMatcher('TR', function (node, delta) {
            return delta;
        });
        clipboard.addMatcher('TD', function (node, delta) {
            return delta.compose(new Delta().retain(delta.length(), {
                td: node.getAttribute('table_id') + '|' + node.getAttribute('row_id') + '|' + node.getAttribute('cell_id')
            }));
        });
    }
}

module.exports = {
    Table,
    TableRow,
    TableCell,
    Contain,
    TableModule
};