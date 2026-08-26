def build_context(results):

    context_parts = []

    for index, result in enumerate(results, start=1):

        context_parts.append(
            f"""
SOURCE {index}
Document ID: {result["document_id"]}
Source File: {result["source_file"]}

Content:
{result["chunk_text"]}
"""
        )

    return "\n".join(context_parts)