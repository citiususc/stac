/**
 * Contains the configuration of the web application
 */
APP_CONFIG={
    app_url : window.location.href.substring(0, window.location.href.lastIndexOf('/')),
    api_url : window.location.href.substring(0, window.location.href.lastIndexOf('/')) + '/api'
}
