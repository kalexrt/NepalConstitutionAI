from nepal_constitution_ai.data_pipeline.chunking import chunk_pdf_content
from nepal_constitution_ai.data_pipeline.embedding import embed_chunks
from nepal_constitution_ai.data_pipeline.pinecone_utils import initialize_pinecone, create_index, wait_for_index, upsert_vectors
from nepal_constitution_ai.config.config import settings

def main():
    chunked_data_dict_list, chunked_data = chunk_pdf_content(settings.FILE_PATH)
    embedded_chunks = embed_chunks(chunked_data)

    pc = initialize_pinecone()
    create_index(pc)
    wait_for_index(pc)
    
    vectors = [{"id": f"chunk_{i+1}", "values": emb, "metadata": [{"text": chunk[key], "source": key} for key in chunk][-1]}
               for i, (chunk, emb) in enumerate(zip(chunked_data_dict_list, embedded_chunks))]

    upsert_vectors(pc, vectors)

if __name__ == "__main__":
    main()
