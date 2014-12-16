//Función para exportar archivos .tex
function exportTableToLaTeX($table, filename) {

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
        latex = latex + "\n\\end{tabular}",

        // Data URI
        latexData = 'data:application/octet-stream;charset=utf-8,' + encodeURIComponent(latex);

    if(navigator.appName == 'Microsoft Internet Explorer'){
        var generator = window.open(filename, 'latex', 'height=400,width=600');
        generator.document.write('<html><head><title>LaTeX</title>');
        generator.document.write('</head><body >');
        generator.document.write('<textArea cols=70 rows=15 wrap="off" >');
        generator.document.write(latex);
        generator.document.write('</textArea>');
        generator.document.write('</body></html>');
        generator.document.close();
    }
    else{
        $(this).attr({
            'download': filename,
            'href': latexData,
            'target': '_blank'
        });
    }
}

//Función para exportar archivos .csv
function exportTableToCSV($table, filename) {

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
            .split(tmpColDelim).join(colDelim) + '"',

        // Data URI
        csvData = 'data:application/csv;charset=utf-8,' + encodeURIComponent(csv);

    if(navigator.appName == 'Microsoft Internet Explorer'){
        var generator = window.open(filename, 'csv', 'height=400,width=600');
        generator.document.write('<html><head><title>CSV</title>');
        generator.document.write('</head><body >');
        generator.document.write('<textArea cols=70 rows=15 wrap="off" >');
        generator.document.write(csv);
        generator.document.write('</textArea>');
        generator.document.write('</body></html>');
        generator.document.close();
    }
    else{
        $(this).attr({
            'download': filename,
            'href': csvData,
            'target': '_blank'
        });
    }
}

