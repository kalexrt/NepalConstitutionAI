from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from loguru import logger

class TextChunker:
    def __init__(self, max_words: int, similarity_threshold: float):
        self.max_words = max_words
        self.similarity_threshold = similarity_threshold
        logger.info("Initialized TextChunker with max_words=%d and similarity_threshold=%.2f", max_words, similarity_threshold)

    def fixed_size_chunking(self, sentences):
        text = " ".join(sentences)
        text_splitter = CharacterTextSplitter(
            separator="",
            chunk_size=self.max_words, 
            chunk_overlap=int(0.2 * self.max_words)
        )
        chunks = text_splitter.split_text(text)
        logger.info("Created %d fixed-size chunks", len(chunks))
        return chunks

    def recursive_chunking(self, sentences):
        text = " ".join(sentences)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.max_words,  
            chunk_overlap=int(0.2 * self.max_words)
        )
        chunks = text_splitter.split_text(text)
        logger.info("Created %d recursive chunks", len(chunks))
        return chunks
