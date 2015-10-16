/**
 * Contains the functions to export the table info of the test results into LaTeX or CSV
 */

/**
 * Exports a list of tables into LaTeX
 * @param {list} table - List of tables to be exported
 * @returns {string} The list of tables converted into LaTeX
 */
function exportTableToLaTeX($table) {
    switch ($table.length) {
        case 0:
            return '';
            break;
        case 1:
            /*Función para repetir un string un determinado número de veces.*/
            String.prototype.repeat = function (n, d) {
                return --n ? this + (d || "") + this.repeat(n, d) : "" + this;
            };

            var $firstrow = $table.find('tr:has(th)'),

                // Temporary delimiter characters unlikely to be typed by keyboard
                // This is to avoid accidentally splitting the actual contents
                tmpColDelim = String.fromCharCode(11), // vertical tab character
                tmpRowDelim = String.fromCharCode(0), // null character

                // Actual delimiter characters for LaTeX format
                colDelim = "&",
                rowDelim = "\\\\\n",

                /*Primera línea de la tabla LaTeX.*/
                latex = "\\begin{tabular}{"+"c".repeat($firstrow.find('th').length,"|")+"}\n",

                latex = latex + $firstrow.map(function (i, row) {
                    var $row = $(row),
                        $cols = $row.find('th');
                    return $cols.map(function (j, col) {
                        var $col = $(col),
                            text = $col.text();
                        return text;
                    }).get().join(tmpColDelim);
                }).get().join(tmpRowDelim)
                        .split(tmpRowDelim).join(rowDelim)
                        .split(tmpColDelim).join(colDelim);

                latex = latex + "\\\\\n\\hline\n",

                /*Resto de líneas de la tabla LaTeX.*/
                $rows = $table.find('tr:has(td)'),

                latex = latex + $rows.map(function (i, row) {
                    var $row = $(row),
                        $cols = $row.find('td');
                    return $cols.map(function (j, col) {
                        var $col = $(col),
                            text = $col.text();
                        return text;
                    }).get().join(tmpColDelim);
                }).get().join(tmpRowDelim)
                        .split(tmpRowDelim).join(rowDelim)
                        .split(tmpColDelim).join(colDelim);

                /*Última línea de la tabla LaTeX.*/
                latex = latex + "\n\\end{tabular}";
                
            return latex;
            break;
        default:
            return $.map($table, function(v) {
                    return exportTableToLaTeX($(v));
                }).join('\n\n');
    }
}

/**
 * Exports a list of tables into CSV
 * @param {list} table - List of tables to be exported
 * @returns {string} The list of tables converted into CSV
 */
function exportTableToCSV($table) {
    switch ($table.length) {
        case 0:
            return '';
            break;
        case 1:
            var $rows = $table.find('tr:has(th,td)'),

                // Temporary delimiter characters unlikely to be typed by keyboard
                // This is to avoid accidentally splitting the actual contents
                tmpColDelim = String.fromCharCode(11), // vertical tab character
                tmpRowDelim = String.fromCharCode(0), // null character

                // actual delimiter characters for CSV format
                colDelim = '","',
                rowDelim = '"\r\n"',

                // Grab text from table into CSV formatted string
                csv = '"' + $rows.map(function (i, row) {
                    var $row = $(row),
                        $cols = $row.find('th,td');

                    return $cols.map(function (j, col) {
                        var $col = $(col),
                            text = $col.text();

                        return text.replace('"', '""'); // escape double quotes

                    }).get().join(tmpColDelim);

                }).get().join(tmpRowDelim)
                    .split(tmpRowDelim).join(rowDelim)
                    .split(tmpColDelim).join(colDelim) + '"';

            return csv;
            break;
        default:
            return $.map($table, function(v) {
                    return exportTableToCSV($(v));
                }).join('\n\n');
    }
}

