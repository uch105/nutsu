import logging

logger = logging.getLogger('request_logger')

def log_request(request):
    ip = request.META.get('REMOTE_ADDR')
    user = request.user.username if request.user.is_authenticated else 'Guest'
    method = request.method
    path = request.path
    agent = request.META.get('HTTP_USER_AGENT', 'Unknown')

    logger.info(f"IP: {ip}, User: {user}, Method: {method}, Path: {path}, Agent: {agent}")