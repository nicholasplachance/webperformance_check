import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_data():
    try:
        # Analysis code here
        pass
    except Exception as e:
        logger.error(f'Error during analysis: {e}')
        raise

if __name__ == '__main__':
    try:
        analyze_data()
    except Exception as e:
        logger.error('Fatal error', exc_info=True)
