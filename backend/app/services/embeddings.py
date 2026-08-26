from sentence_transformers import sentence_transformer

MODEL_NAME = "BAAI/bge-small-en-v1.5"

model = sentence_transformer(model = MODEL_NAME)

def embed_test(text: str):
    return model.encode(text,normalize_embeddings = True).tolist()

