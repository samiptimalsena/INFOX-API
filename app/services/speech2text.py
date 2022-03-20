from app.utils.utils import load_S2T, device
from glob import glob
from loguru import logger

def speech2text(wav_file: str) -> str:
    """
    Converts audio to text

    Args:
        wav_file: filepath for the saved wav file

    Returns:
        Transcribed text
    """
    model, decoder, read_batch, split_into_batches, prepare_model_input = load_S2T()
    logger.info("Loaded S2T model")
    wav_files = glob(wav_file)
    batches = split_into_batches(wav_files, batch_size=10)
    processed_input = prepare_model_input(read_batch(batches[0]), device=device)
    output = model(processed_input)
    return decoder(output[0].cpu())