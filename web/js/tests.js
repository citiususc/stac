$(document).ready(function(){
    // Idle visual feedback when applying a test  
    function idleFeedBack() {
        label = $("#apply label");
        label.toggleClass("glyphicon-refresh");
        label.toggleClass("glyphicon-refresh-animate");
        label.toggleClass("glyphicon-play");
        $("#apply").prop("disabled", false);
    }
    
    // Event handler for applying a test
	$(document).on('click', '#apply', function() {
        if(!sessionStorage.getItem("data")) {
            $("#danger").html("<strong>¡Upload a file!</strong> In the top right of the navigation bar you can select and upload a file by clicking <it>Upload file</it>. Then, click <it>Show file</it> to watch its contents.");
            $("#danger").show();
        } else {
			var type = $(this).attr("test");

            var test = $('input[name=test]:checked').val();
            var alpha = $('#alpha').val();
            
            var url = APP_CONFIG.api_url+"/"+test+"/"+alpha;
            var post_hoc = $('input[name=post_hoc]:checked').val();
            if (post_hoc) {
                if ($("#control").length) {
                    control = $("#control").val();
                    url = APP_CONFIG.api_url+"/"+test+"/"+post_hoc+"/"+control+"/"+alpha;
                } else {
                    url = APP_CONFIG.api_url+"/"+test+"/"+post_hoc+"/"+alpha;
                }
            }
            
			$("#apply").prop("disabled", true);
            label = $("#apply label");
            label.toggleClass("glyphicon-play");
            label.toggleClass("glyphicon-refresh");
            label.toggleClass("glyphicon-refresh-animate");
			switch (type) {
                case "assistant":
					$.ajax({
						type: "POST", url: APP_CONFIG.api_url+"/assistant", dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify(JSON.parse(sessionStorage.data).values),
						success : function(data) {
							$("#danger").hide();
							$("#warning").hide();
							
							if (data.error) {
								$("#danger").html(data.error).show();
							} else {
                                $("#graph").html('\
                                <ul align="left">\
                                    <li>Number of groups k = ' +data.k+ '</li>\
                                    <li>Number of samples n = ' +data.n+ '</li>\
                                    <li>' + (data.paired ? 'Paired data' : 'Unpaired data') + '</li>\
                                    <li>' + (data.normality ? 'Normality satisfied' : 'Normality not satisfied') + '</li>\
                                    <li>' + (data.homocedasticity ? 'Homocedasticity satisfied' : 'Homocedasticity not satisfied') + '</li>\
                                    </ul>' + 
                                    Viz(data.graph, "svg"));
                                    $("svg").attr("width", "100%");
                                $("#decision_process").show();
							}
							
						},
						error : function(e) {
							console.log('error: ' + e);
						}
					}).always(idleFeedBack);
					break;
				case "normality":
					$.ajax({
						type: "POST", url: url, dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify(JSON.parse(sessionStorage.data).values),
						success : function(data) {
							$("#danger").hide();
							$("#warning").hide();
							
							if (data.error) {
								$("#danger").html(data.error).show();
							} else {
                                console.log(data);
								var salida = normality_table(data, JSON.parse(sessionStorage["data"]).names, test, alpha);
									
								$("#result").html(salida).show();
							}
							
						},
						error : function(e) {
							console.log('error: ' + e);
						}
					}).always(idleFeedBack);
					break;
				case "homocedasticity":
					$.ajax({
						type: "POST", url: url, dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify(JSON.parse(sessionStorage.data).values),
						success : function(data) {
							$("#danger").hide();
							$("#warning").hide();
							
							if (data.error) {
								$("#danger").html(data.error).show();
							} else {
								var salida = homocedasticity_table(data, test, alpha);
									
								$("#result").html(salida).show();
							}
						},
						error : function(e) {
							console.log('error: ' + e);
						}
					}).always(idleFeedBack);
					break;
				case "anova":
					$.ajax({
						type: "POST", url: url, dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify(JSON.parse(sessionStorage.data).values),
						success : function(data) {
							$("#danger").hide();
							$("#warning").hide();
							
							if (data.error) {
								$("#danger").html(data.error).show();
							} else {
								var salida = anova_table(data.anova, test, alpha);
								salida = salida + multi_posthoc_table(data.post_hoc, "bonferroni", alpha)
									
								$("#result").html(salida).show();
							}
							
						},
						error : function(e) {
							console.log('error: ' + e);
						}
					}).always(idleFeedBack);
					break;
				case "ttest":
                    var group1 = $("#group1").val()
                    var group2 = $("#group2").val()
					$.ajax({
						type: "POST", url: url, dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify({group1: JSON.parse(sessionStorage.data).values[group1], group2: JSON.parse(sessionStorage.data).values[group2]}),
						success : function(data) {
							$("#danger").hide();
							$("#warning").hide();
							
							if (data.error) {
								$("#danger").html(data.error).show();
							} else {
								var salida = ttest_table(data, test, alpha);
									
								$("#result").html(salida).show();
							}
							
						},
						error : function(e) {
							console.log('error: ' + e);
						}
					}).always(idleFeedBack);
					break;
				case "wilcoxon":
                    var group1 = $("#group1").val()
                    var group2 = $("#group2").val()
					$.ajax({
						type: "POST", url: url, dataType: "json",
                        contentType: "application/json",
                        data:  JSON.stringify({group1: JSON.parse(sessionStorage.data).values[group1], group2: JSON.parse(sessionStorage.data).values[group2]}),
						success : function(data) {
							$("#danger").hide();
							$("#warning").hide();
							
							if (data.error) {
								$("#danger").html(data.error).show();
							} else {
								$("#result").html(wilcoxon_table(data, test, alpha)).show();
							}
							
						},
						error : function(e) {
							console.log('error: ' + e);
						}
					}).always(idleFeedBack);
					break;
                case "binomialsign":
                        var group1 = $("#group1").val()
                        var group2 = $("#group2").val()
                                            $.ajax({
                                                    type: "POST", url: url, dataType: "json",
                            contentType: "application/json",
                            data: JSON.stringify({group1: JSON.parse(sessionStorage.data).values[group1], group2: JSON.parse(sessionStorage.data).values[group2]}),
                            success : function(data) {
                                    $("#danger").hide();
                                    $("#warning").hide();
                                    
                                    if (data.error) {
                                            $("#danger").html(data.error).show();
                                    } else {
                                            $("#result").html(wilcoxon_table(data, test, alpha)).show();
                                    }
                                    
                            },
                            error : function(e) {
                                    console.log('error: ' + e);
                            }
                    }).always(idleFeedBack);
                case "ranking":
					$.ajax({
						type: "POST", url: url, dataType: "json",
                        contentType: "application/json",
                        data: JSON.stringify(JSON.parse(sessionStorage.data).values),
						success : function(data) {
							$("#danger").hide();
							$("#warning").hide();
							
							if (data.error) {
								$("#danger").html(data.fallo).show();
							} else {
								var salida = ranking_table(data.ranking, test, alpha);
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
					}).always(idleFeedBack);
					break;
			}
        }
    });
});


// Transforms the output of a normality test into HTML tables
function normality_table(data, names, test, alpha) {
    var salida = 
    "<div class=\"table-responsive\"><h2>Results</h2>\
        <a href=\"#modal_export\" data-toggle=\"modal\"><button class=\"btn btn-default\"><span class=\"glyphicon glyphicon-export\"></span>Export</button></a>\
		<table class=\"table table-hover table-striped\">\
				<caption>"+ $("input[value="+test+"]").parent().text() + " test (significance level of " + alpha + ")</caption>\
				<thead>\
					<tr>\
						<th>Dataset</th>";
		
    salida = salida + "<th>Statistic</th><th>p-value</th><th>Result</th></thead><tbody>";
    $.each(data.p_value, function(index, value) {
        salida = salida + "<tr><td>" + names[index] + "</td><td>" + data.statistic[index].toFixed(5) + "</td><td>" + data.p_value[index].toFixed(5) + "</td>";
        if(data.result[index] == true)
            salida = salida + "<td>H0 is rejected</td></tr>";
        else
            salida = salida + "<td>H0 is accepted</td></tr>";
    });

	salida = salida + "</tbody></table></div>";

    return salida;
}

// Transforms the output of a homoscedasticity test into HTML tables
function homocedasticity_table(data, test, alpha) {
    var salida = 
    "<div class=\"table-responsive\"><h2>Results</h2>\
		<a href=\"#\" onclick=\"exportTableToCSV.apply(this, [$('table'), $('input[name=test]:checked').val()+'.csv'])\"><button class=\"btn btn-default\"><span class=\"glyphicon glyphicon-export\"></span> CSV</button></a>&nbsp;&nbsp;\
		<a href=\"#\" onclick=\"exportTableToLaTeX.apply(this, [$('table'), $('input[name=test]:checked').val()+'.tex'])\"><button class=\"btn btn-default\"><span class=\"glyphicon glyphicon-export\"></span> LaTeX</button></a> \
		<table class=\"table table-hover table-striped\">\
			<caption>"+ $("input[value="+test+"]").parent().text() + " test (significance level of " + alpha + ")</caption>\
			<thead><tr><th>Statistic</th><th>p-value</th><th>Result</th></tr></thead>\
			<tbody><tr><td>" +data.statistic.toFixed(5)+ "</td><td>" +data.p_value.toFixed(5)+ "</td>";
    if (data.resultado == true)
        salida = salida + "<td>H0 is rejected</td></tr>";
    else
        salida = salida + "<td>H0 is accepted</td></tr>";

	salida = salida + "</tbody></table></div>";

    return salida;
}

// Transforms the output of a t-test into HTML tables
function ttest_table(data, test, alpha) {
    var salida = 
    "<div class=\"table-responsive\"><h2>Results</h2>\
		<a href=\"#modal_export\" data-toggle=\"modal\"><button class=\"btn btn-default\"><span class=\"glyphicon glyphicon-export\"></span>Export</button></a>\
		<table class=\"table table-hover table-striped\">\
			<caption>T-test (significance level of " + alpha + ")</caption>\
			<thead><tr><th>T Statistic</th><th>p-value</th><th>Result</th></tr></thead>\
			<tbody><tr><td>" +data.statistic.toFixed(5)+ "</td><td>" +data.p_value.toFixed(5)+ "</td>";
    
    if(data.resultado == true)
        salida = salida + "<td>H0 is rejected</td></tr>";
    else
        salida = salida + "<td>H0 is accepted</td></tr>";

	salida = salida + "</tbody></table></div>";
	
    return salida;
}

// Transforms the output of an ANOVA test into HTML tables
function anova_table(data, test, alpha) {
    var salida = 
    "<div class=\"table-responsive\"><h2>Results</h2>\
        <a href=\"#modal_export\" data-toggle=\"modal\"><button class=\"btn btn-default\"><span class=\"glyphicon glyphicon-export\"></span>Export</button></a>\
		<table class=\"table table-hover table-striped\">\
			<caption>"+ $("input[value="+test+"]").parent().text() + " test (significance level of " + alpha + ")</caption>\
			<thead><tr><th>Statistic</th><th>p-value</th><th>Result</th></tr></thead>\
			<tbody><tr><td>" +data.statistic.toFixed(5)+ "</td><td>" +data.p_value.toFixed(5)+ "</td>";
    
    if(data.resultado == true)
        salida = salida + "<td>H0 is rejected</td></tr>";
    else
        salida = salida + "<td>H0 is accepted</td></tr>";

	salida = salida + "</tbody></table></div>";
	
    return salida;
}

// Transforms the output of a wilcoxon test into HTML tables
function wilcoxon_table(data, test, alpha) {
	var salida = 
    "<div class=\"table-responsive\"><h2>Results</h2>\
        <a href=\"#modal_export\" data-toggle=\"modal\"><button class=\"btn btn-default\"><span class=\"glyphicon glyphicon-export\"></span>Export</button></a>\
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

// Transforms the output of a ranking test into HTML tables
function ranking_table(data, test, alpha) {
    var salida = 
    "<div class=\"table-responsive\"><h2>Results</h2>\
		<a href=\"#modal_export\" data-toggle=\"modal\"><button class=\"btn btn-default\"><span class=\"glyphicon glyphicon-export\"></span>Export</button></a>\
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
    
    salida =  salida +
    "   <table class=\"table table-hover table-striped\">\
			<caption>Ranking</caption>\
			<thead><tr><th>Rank</th><th>Algorithm</th></thead>\
            <tbody>";
            
    $.each(data.rankings, function(index, value) {
        salida = salida + "<tr><td>" + value.toFixed(5) + "</td><td>" + data.names[index] + "</td></tr>";
	});
    salida = salida + "</tbody></table></div>";

    return salida;
}

// Transforms the output of a post-hoc test with control method into HTML tables
function control_method_table(data, test, alpha) {
    var salida = 
	"<table class=\"table table-hover table-striped\">\
            <caption>Post-hoc (Using "+data.control+" as control method)</caption>\
			<thead><tr><th>Comparison</th><th>Statistic</th><th>Adjusted p-value</th><th>Result</th></tr></thead>\
            <tbody>";

    $.each(data.comparisons, function(index, value) {
        salida = salida + "<td>" + value + "</td><td>" + data.statistic[index].toFixed(5) + "</td><td>" + data.p_value[index].toFixed(5) + "</td>";
        if (data.result[index])
            salida = salida + "<td>H0 is rejected</td></tr>";
        else
            salida = salida + "<td>H0 is accepted</td></tr>";
    });

    salida = salida + "</tbody></table></div>";

    return salida;
}

// Transforms the output of a post-hoc test without control method into HTML tables
function multi_posthoc_table(data, test, alpha) {
    var salida = 
	"<hr><div class=\"table-responsive\">\
		<table class=\"table table-hover table-striped\">\
			<caption>"+ $("input[value="+test+"]").parent().text() + " test (significance level of " + alpha + ")</caption>\
			<thead><tr><th>Comparison</th><th>Statistic</th><th>Adjusted p-value</th><th>Result</th></tr></thead>\
            <tbody>";	

    $.each(data.comparisons, function(index, value) {
        salida = salida + "<tr><td>" + value + "</td><td>" + data.statistic[index].toFixed(5) + "</td><td>" +data.p_value[index].toFixed(5)+ "</td>";
        if(data.result[index])
            salida = salida + "<td>H0 is rejected</td></tr>";
        else
            salida = salida + "<td>H0 is accepted</td></tr>";
    });
    
    salida = salida + "</tbody></table></div>";

    return salida;
}
