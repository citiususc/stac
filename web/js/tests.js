$(document).ready(function(){
	$(document).on('click', '#apply', function() {
        if(!sessionStorage.getItem("data")) {
            $("#danger").html("<strong>¡Upload a file!</strong> In the top right of the navigation bar you can select and upload a file by clicking <it>Upload file</it>. Then, click <it>Show file</it> to watch its contents.");
            $("#danger").show();
        } else {
			var type = $(this).attr("test");
			var test = $('input[name=test]:checked').val();
			var alpha = $('#alpha').val();
            
            var url = window.location.origin+"/stac/api/"+test+"/"+sessionStorage.getItem("data")+"/"+alpha;
            var post_hoc = $('input[name=post_hoc]:checked').val();
            if (post_hoc) var url = window.location.origin+"/stac/api/"+test+"/"+sessionStorage.getItem("data")+"/"+alpha+"/"+post_hoc;
			console.log(url);
			
			switch (type) {
				case "normality":
					$.ajax({
						type: "GET", url: url, dataType: "json",
						success : function(data) {
							$("#danger").hide();
							$("#warning").hide();
							
							if (data.fallo) {
								$("#danger").html(data.fallo).show();
							} else {
								var salida = normality_table(data, test, alpha);
									
								$("#result").html(salida).show();
							}
							
						},
						error : function(e) {
							console.log('error: ' + e);
						}
					});
					break;
				case "homocedasticity":
					$.ajax({
						type: "GET", url: url, dataType: "json",
						success : function(data) {
							$("#danger").hide();
							$("#warning").hide();
							
							if (data.fallo) {
								$("#danger").html(data.fallo).show();
							} else {
								var salida = homocedasticity_table(data, test, alpha);
									
								$("#result").html(salida).show();
							}
						},
						error : function(e) {
							console.log('error: ' + e);
						}
					});
					break;
				case "anova":
					$.ajax({
						type: "GET", url: url, dataType: "json",
						success : function(data) {
							$("#danger").hide();
							$("#warning").hide();
							
							if (data.fallo) {
								$("#danger").html(data.fallo).show();
							} else {
								var salida = anova_table(data.test_anova, test, alpha);
								salida = salida + multi_posthoc_table(data.test_comparacion, "bonferroni", alpha)
									
								$("#result").html(salida).show();
							}
							
						},
						error : function(e) {
							console.log('error: ' + e);
						}
					});
					break;
				case "ttest":
					$.ajax({
						type: "GET", url: url, dataType: "json",
						success : function(data) {
							$("#danger").hide();
							$("#warning").hide();
							
							if (data.fallo) {
								$("#danger").html(data.fallo).show();
							} else {
								var salida = ttest_table(data, test, alpha);
									
								$("#result").html(salida).show();
							}
							
						},
						error : function(e) {
							console.log('error: ' + e);
						}
					});
					break;
				case "wilcoxon":
					$.ajax({
						type: "GET", url: url, dataType: "json",
						success : function(data) {
							$("#danger").hide();
							$("#warning").hide();
							
							if (data.error) {
								$("#danger").html(data.fallo).show();
							} else {
								var salida = wilcoxon_table(data, test, alpha);
									
								$("#result").html(salida).show();
							}
							
						},
						error : function(e) {
							console.log('error: ' + e);
						}
					});
					break;
				case "mannwhitneyu":
					$.ajax({
						type: "GET", url: url, dataType: "json",
						success : function(data) {
							$("#danger").hide();
							$("#warning").hide();
							
							if (data.error) {
								$("#danger").html(data.fallo).show();
							} else {
								var salida = wilcoxon_table(data, test, alpha);
									
								$("#result").html(salida).show();
							}
						},
						error : function(e) {
							console.log('error: ' + e);
						}
					});
					break;
                case "ranking":
					$.ajax({
						type: "GET", url: url, dataType: "json",
						success : function(data) {
							$("#danger").hide();
							$("#warning").hide();
							
							if (data.error) {
								$("#danger").html(data.fallo).show();
							} else {
								var salida = ranking_table(data.test_ranking, test, alpha);
                                if ($("input[name=post_hoc]:checked").attr("comparison") == "control")
                                    salida = salida + control_method_table(data.post_hoc, test, alpha);
                                else
                                    salida = salida + multi_posthoc_table(data.post_hoc, test, alpha);
								$("#result").html(salida).show();
							}
						},
						error : function(e) {
							console.log('error: ' + e);
						}
					});
					break;
			}
        }
    });
});


function normality_table(data, test, alpha) {
    var salida = 
    "<div class=\"table-responsive\"><h2>Results</h2>\
		<a href=\"#\" onclick=\"exportTableToCSV.apply(this, [$('table'), $('input[name=test]:checked').val()+'.csv'])\"><button class=\"btn btn-default\"><span class=\"glyphicon glyphicon-export\"></span> CSV</button></a>&nbsp;&nbsp;\
		<a href=\"#\" onclick=\"exportTableToLaTeX.apply(this, [$('table'), $('input[name=test]:checked').val()+'.tex'])\"><button class=\"btn btn-default\"><span class=\"glyphicon glyphicon-export\"></span> LaTeX</button></a> \
			<table class=\"table table-hover table-striped\">\
				<caption>"+ $("input[value="+test+"]").parent().text() + " test (significance level of " + alpha + ")</caption>\
				<thead>\
					<tr>\
						<th>Dataset</th>";
		
		if(test == "shapiro") {
			salida = salida + "<th>W Statistic</th><th>p-value</th><th>Result</th></thead><tbody>";
			$.each(data.p_value, function(index, value) {
				salida = salida + "<tr><td>" + data.dataset[index] + "</td><td>" + data.w[index].toFixed(5) + "</td><td>" + data.p_value[index].toFixed(5) + "</td>";
				if(data.result[index] == true)
					salida = salida + "<td>H0 is rejected</td></tr>";
				else
					salida = salida + "<td>H0 is accepted</td></tr>";
			});
    } else if(test == "kolmogorov"){
        salida = salida + "<th>D Statistic</th><th>p-value</th><th>Result</th></tr></thead><tbody>";
        $.each(data.p_valores, function(index, value) {
		    salida = salida + "<tr><td>" + (index+1) + "</td><td>" + data.estadisticos_d[index].toFixed(5) + "</td><td>" + data.p_valores[index].toFixed(5) + "</td>";
            if(data.resultado[index] == true)
                salida = salida + "<td>H0 is rejected</td></tr>";
            else
                salida = salida + "<td>H0 is accepted</td></tr>";
	        });
    } else{
        salida = salida + "<th>K2 Statistic</th><th>p-value</th><th>Result</th></tr></thead><tbody>";
        $.each(data.p_valores, function(index, value) {
		    salida = salida + "<tr><td>" + (index+1) + "</td><td>" + data.estadisticos_k2[index].toFixed(5) + "</td><td>" + data.p_valores[index].toFixed(5) + "</td>";
            if(data.resultado[index] == true)
                salida = salida + "<td>H0 is rejected</td></tr>";
            else
                salida = salida + "<td>H0 is accepted</td></tr>";
	        });
    }

	salida = salida + "</tbody></table></div>";

    return salida;
}

function homocedasticity_table(data, test, alpha) {
    var salida = 
    "<div class=\"table-responsive\"><h2>Results</h2>\
		<a href=\"#\" onclick=\"exportTableToCSV.apply(this, [$('table'), $('input[name=test]:checked').val()+'.csv'])\"><button class=\"btn btn-default\"><span class=\"glyphicon glyphicon-export\"></span> CSV</button></a>&nbsp;&nbsp;\
		<a href=\"#\" onclick=\"exportTableToLaTeX.apply(this, [$('table'), $('input[name=test]:checked').val()+'.tex'])\"><button class=\"btn btn-default\"><span class=\"glyphicon glyphicon-export\"></span> LaTeX</button></a> \
		<table class=\"table table-hover table-striped\">\
			<caption>"+ $("input[value="+test+"]").parent().text() + " test (significance level of " + alpha + ")</caption>\
			<thead><tr><th>W Statistic</th><th>p-value</th><th>Result</th></tr></thead>\
			<tbody><tr><td>" +data.estadistico_w.toFixed(5)+ "</td><td>" +data.p_valor.toFixed(5)+ "</td>";
    if (data.resultado == true)
        salida = salida + "<td>H0 is rejected</td></tr>";
    else
        salida = salida + "<td>H0 is accepted</td></tr>";

	salida = salida + "</tbody></table></div>";

    return salida;
}

function anova_table(data, test, alpha) {
    var salida = 
    "<div class=\"table-responsive\"><h2>Results</h2>\
		<a href=\"#\" onclick=\"exportTableToCSV.apply(this, [$('table'), $('input[name=test]:checked').val()+'.csv'])\"><button class=\"btn btn-default\"><span class=\"glyphicon glyphicon-export\"></span> CSV</button></a>&nbsp;&nbsp;\
		<a href=\"#\" onclick=\"exportTableToLaTeX.apply(this, [$('table'), $('input[name=test]:checked').val()+'.tex'])\"><button class=\"btn btn-default\"><span class=\"glyphicon glyphicon-export\"></span> LaTeX</button></a> \
		<table class=\"table table-hover table-striped\">\
			<caption>"+ $("input[value="+test+"]").parent().text() + " test (significance level of " + alpha + ")</caption>\
			<thead><tr><th>Statistic</th><th>p-value</th><th>Result</th></tr></thead>\
			<tbody><tr><td>" +data.estadistico.toFixed(5)+ "</td><td>" +data.p_valor.toFixed(5)+ "</td>";
    
    if(data.resultado == true)
        salida = salida + "<td>H0 is rejected</td></tr>";
    else
        salida = salida + "<td>H0 is accepted</td></tr>";

	salida = salida + "</tbody></table></div>";
	
    return salida;
}

function ttest_table(data, test, alpha) {
    var salida = 
    "<div class=\"table-responsive\"><h2>Results</h2>\
		<a href=\"#\" onclick=\"exportTableToCSV.apply(this, [$('table'), $('input[name=test]:checked').val()+'.csv'])\"><button class=\"btn btn-default\"><span class=\"glyphicon glyphicon-export\"></span> CSV</button></a>&nbsp;&nbsp;\
		<a href=\"#\" onclick=\"exportTableToLaTeX.apply(this, [$('table'), $('input[name=test]:checked').val()+'.tex'])\"><button class=\"btn btn-default\"><span class=\"glyphicon glyphicon-export\"></span> LaTeX</button></a> \
		<table class=\"table table-hover table-striped\">\
			<caption>T-test (significance level of " + alpha + ")</caption>\
			<thead><tr><th>T Statistic</th><th>p-value</th><th>Result</th></tr></thead>\
			<tbody><tr><td>" +data.estadistico_t.toFixed(5)+ "</td><td>" +data.p_valor.toFixed(5)+ "</td>";
    
    if(data.resultado == true)
        salida = salida + "<td>H0 is rejected</td></tr>";
    else
        salida = salida + "<td>H0 is accepted</td></tr>";

	salida = salida + "</tbody></table></div>";
	
    return salida;
}

function wilcoxon_table(data, test, alpha) {
	var salida = 
    "<div class=\"table-responsive\"><h2>Results</h2>\
		<a href=\"#\" onclick=\"exportTableToCSV.apply(this, [$('table'), $('input[name=test]:checked').val()+'.csv'])\"><button class=\"btn btn-default\"><span class=\"glyphicon glyphicon-export\"></span> CSV</button></a>&nbsp;&nbsp;\
		<a href=\"#\" onclick=\"exportTableToLaTeX.apply(this, [$('table'), $('input[name=test]:checked').val()+'.tex'])\"><button class=\"btn btn-default\"><span class=\"glyphicon glyphicon-export\"></span> LaTeX</button></a> \
		<table class=\"table table-hover table-striped\">\
			<caption>"+ $("input[value="+test+"]").parent().text() + " test (significance level of " + alpha + ")</caption>\
			<thead><tr><th>Statistic</th><th>p-value</th><th>Result</th></tr></thead>\
			<tbody><tr><td>" +data.statistic+ "</td><td>" +data.p_value+ "</td>";

    if (data.result)
        salida = salida + "<td>H0 is rejected</td></tr></tbody></table>";
    else
        salida = salida + "<td>H0 is accepted</td></tr></tbody></table>";
        
	salida = salida + "</tbody></table></div>";
	
    return salida;
}

function ranking_table(data, test, alpha) {
    var salida = 
    "<div class=\"table-responsive\"><h2>Results</h2>\
		<a href=\"#\" onclick=\"exportTableToCSV.apply(this, [$('table'), $('input[name=test]:checked').val()+'.csv'])\"><button class=\"btn btn-default\"><span class=\"glyphicon glyphicon-export\"></span> CSV</button></a>&nbsp;&nbsp;\
		<a href=\"#\" onclick=\"exportTableToLaTeX.apply(this, [$('table'), $('input[name=test]:checked').val()+'.tex'])\"><button class=\"btn btn-default\"><span class=\"glyphicon glyphicon-export\"></span> LaTeX</button></a> \
		<table class=\"table table-hover table-striped\">\
            <caption>"+ $("input[value="+test+"]").parent().text() + " test (significance level of " + alpha + ")</caption>\
			<thead><tr><th>Statistic</th><th>p-value</th><th>Result</th></thead>\
            <tbody>\
                <td>"+data.statistic.toFixed(5) + "</td><td>" + data.p_value.toFixed(5) + "</td>";
            if (data.result)
                salida = salida + "<td>H0 is rejected</td></tr>";
            else
                salida = salida + "<td>H0 is accepted</td></tr>";
    salida = salida + "</tbody></table>";
    
    var salida =  salida +
    "   <table class=\"table table-hover table-striped\">\
			<caption>Ranking</caption>\
			<thead><tr><th>Rank</th><th>Algorithm</th></thead>\
            <tbody>";
            
    $.each(data.ranking, function(index, value) {
        salida = salida + "<tr><td>" + value.toFixed(5) + "</td><td>" + data.names[index] + "</td></tr>";
	});
    salida = salida + "</tbody></table></div>";

    return salida;
}

function control_method_table(data, test, alpha) {
    var salida = 
	"<table class=\"table table-hover table-striped\">\
            <caption>Post-hoc (Using "+data.control_method+" as control method)</caption>\
			<thead><tr><th>Comparison</th><th>Statistic</th><th>p-value</th><th>Adjusted p-value</th><th>Result</th></tr></thead>\
            <tbody>";

    $.each(data.names, function(index, value) {
        salida = salida + "<td>" + data.control_method + " vs " + value + "</td><td>" + data.statistics[index].toFixed(5) + "</td><td>" + data.p_values[index].toFixed(5) + "</td><td>" + data.adjusted_p_values[index].toFixed(5) + "</td>";
        if (data.result[index])
            salida = salida + "<td>H0 is rejected</td></tr>";
        else
            salida = salida + "<td>H0 is accepted</td></tr>";
    });

    salida = salida + "</tbody></table></div>";

    return salida;
}

function multi_posthoc_table(data, test, alpha) {
    var salida = 
	"<hr><div class=\"table-responsive\">\
		<table class=\"table table-hover table-striped\">\
			<caption>"+ $("input[value="+test+"]").parent().text() + " test (significance level of " + alpha + ")</caption>\
			<thead><tr><th>Comparison</th><th>Statistic</th><th>p-value</th><th>Adjusted p-value</th><th>Result</th></tr></thead>\
            <tbody>";
			
    if(test == "bonferroni"){
        $.each(data.comparaciones, function(index, value) {
                salida = salida + "<tr><td>" + value + "</td><td>" +data.valores_t[index].toFixed(5)+ "</td><td>" +data.p_valores[index].toFixed(5)+ "</td><td>" +data.p_valores_ajustados[index].toFixed(5)+ "</td>";
            if(data.resultado[index] == true)
                salida = salida + "<td>H0 is rejected</td></tr>";
            else
                salida = salida + "<td>H0 is accepted</td></tr>";
        });
    } else {
        $.each(data.comparisons, function(index, value) {
	        salida = salida + "<tr><td>" + value + "</td><td>" + data.statistics[index].toFixed(5) + "</td><td>" +data.p_values[index].toFixed(5)+ "</td><td>" +data.adjusted_p_values[index].toFixed(5) + "</td>";
            if(data.result[index])
                salida = salida + "<td>H0 is rejected</td></tr>";
            else
                salida = salida + "<td>H0 is accepted</td></tr>";
        });
    }
    
    salida = salida + "</tbody></table></div>";

    return salida;
}
