import logging

def setup_logger(name, level=logging.INFO):
    logger = logging.getLogger(name)
    
    # Verifica se o logger já possui handlers para evitar múltiplos logs
    if not logger.hasHandlers():
        # Adiciona um handler de stream (console)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)

    return logger