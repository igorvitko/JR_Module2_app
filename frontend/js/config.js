(() => {
    const onNginx = location.port === '' || location.port === '80';
    window.APP_CONFIG = {
        baseUrl: onNginx ? '' : 'http://localhost:8000',
    };
    console.log('[CONFIG] baseUrl =', JSON.stringify(window.APP_CONFIG.baseUrl));
})();