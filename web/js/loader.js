/**
 * Load a javascript file
 * 
 * @param {string} url - The url of the script to load
 * @param {function} callback - the function to call when when the script is loaded
 */
function loadScript(url, callback) {
    // Adding the script tag to the head as suggested before
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = url;

    // Then bind the event to the callback function.
    // There are several events for cross browser compatibility.
    script.onreadystatechange = callback;
    script.onload = callback;

    // Fire the loading
    head.appendChild(script);
}

/**
 * Load a CSS file
 * 
 * @param {string} url - The url of the CSS file to load
 * @param {function} callback - the function to call when when the CSS is loaded
 */
function loadStyle(url, callback) {
    // Adding the script tag to the head as suggested before
    var head = document.getElementsByTagName('head')[0];
    var style = document.createElement('link');
    style.rel = 'stylesheet';
    style.href = url;

    // Then bind the event to the callback function.
    // There are several events for cross browser compatibility.
    style.onreadystatechange = callback;
    style.onload = callback;

    // Fire the loading
    head.appendChild(style);
}


// Load styles
loadStyle("fonts/Roboto.css");
loadStyle("css/bootstrap.min.css");
loadStyle("css/dashboard.css");
loadStyle("//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css");

// Load scripts
loadScript("js/lib/jquery.min.js", function() {
    loadScript("js/config.js", function() {
        loadScript("js/lib/bootstrap.min.js");
        loadScript("js/lib/papaparse.js");
        loadScript("js/layout.js");
        loadScript("js/behavior.js");
        loadScript("js/file_manager.js");
        loadScript("js/tests.js");
        loadScript("js/export.js");
    })
});
