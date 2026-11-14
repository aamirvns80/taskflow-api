import logging

from app.logging_config import configure_logging

def test_configure_logging_does_not_add_duplicate_handlers():
    root_logger = logging.getLogger()
    configure_logging()
    handlers_after_first_call = len(root_logger.handlers)
    
    configure_logging()
    handlers_after_second_call = len(root_logger.handlers)
    
    assert handlers_after_second_call== handlers_after_first_call
    
    
    
    