**Retrieval-augmented generation (RAG) system with RAGBench dataset and evaluate with TRACe metrics**
1.1.	Problem Description
  	
Retrieval-augmented generation (RAG) systems are vital for solving complex question-answering tasks but face challenges like inefficient retrieval, inaccuracies in grounding, and lack of coherence, often leading to outdated or fabricated information. Additionally, there is no unified evaluation framework across domains, and large language models (LLMs) struggle with RAG tasks due to difficulties in estimating context relevance. Benchmarks like RagBench reveal LLM judges underperform compared to fine-tuned RAG evaluation models, and concerns arise about noise and bias in GPT-4 turbo annotations affecting system reliability.
To address these issues, this project proposes an advanced RAG pipeline optimized across all workflow stages. The pipeline integrates multimodal retrieval to enhance performance on visual inputs and leverages RAGBench by testing on diverse datasets spanning healthcare, finance, legal, and technology domains, this pipeline aims to establish a robust, reliable, and domain-adaptable solution for knowledge-intensive tasks.

1.2.	Dataset

To ensure a comprehensive evaluation, the system will be taking the RAGBench data set which consists of 12 datasets across 5 domains
1.	Bio-medical research
a.	PubMedQA: Biomedical question answering for health-related queries.
b.	CovidQA-RAG: COVID-19-specific queries requiring up-to-date, factual information.
2.	General knowledge
a.	HotpotQA: Multi-hop reasoning across multiple documents.
b.	MS Marco: Web-based large-scale QA dataset for open-domain tasks.
c.	HAGRID: Dataset focusing on health-related grounding.
d.	ExpertQA: Requires expert knowledge for high-accuracy QA tasks.
3.	Legal contracts
a.	CUAD: Legal contract analysis for QA.
4.	Customer service
a.	DelusionQA: Handles ambiguous and delusional queries to test response robustness.
b.	EManual: QA tasks focusing on technical manuals.
c.	TechQA: Complex technical content QA dataset.
5.	Finance 
a.	FinQA: Financial question-answering dataset.
b.	TAT-QA: Tabular data QA requiring advanced reasoning.

2.2	Data processing , Storage and Retrieval

In this section, we detail the data processing and storage techniques employed to optimize the retrieval-augmented generation (RAG) pipeline. The tasks included Sentence-Level Chunking, Sliding Window Overlap with Token Limit, Embedding Generation, and Evaluation of Vector Databases for efficient storage and retrieval. Below is a breakdown of the steps taken:

2.2.1	Sentence-Level Chunking 

To ensure the contextual integrity of the content, especially for multi-hop datasets like Emanual,  CUAD , FinQA and TAT-QA, we implemented Sentence-Level Chunking. This technique breaks down documents into smaller, coherent chunks while preserving the semantic meaning of the text. We utilized the BAAI/LLM-Embedder to generate embeddings for each chunk, ensuring that the retrieval process captures the most relevant information.
•	Chunking Technique: Sentence-level chunking was applied with a customised sliding window logic of 25 to 30 sentences as a chunk and with an overlap of 5 to 8 sentences maintain the logical flow of information.
•	Embedding Approach: The BAAI/LLM-Embedder was used to generate embeddings for each chunk, ensuring high-quality vector representations.
•	Metadata Addition: Metadata such as keywords from the chunk were added to each chunk for efficient retrieval.

2.2.2	Embedding for Each Document

To facilitate efficient retrieval, embeddings were generated for each document for the PubMedQA, CovidQA, HotpotQA, MS Marco, HAGRID, ExpertQA, TechQA and DelusionQA datasets. This step involved:
•	Document-Level Embedding: Each document was processed to generate a single embedding vector using the BAAI/LLM-Embedder.
•	Embedding Approach: The BAAI/LLM-Embedder was used to generate embeddings for each chunk, ensuring high-quality vector representations.
•	Metadata Addition: Metadata such as keywords from the chunk were added to each chunk for efficient retrieval.
•	Storage: Document-level embeddings were stored in the vector database for quick access during retrieval.
Additionally, we attempted Sliding Window Overlap with a token limit of 512, but it did not yield accurate results when retrieving data from the vector database.

2.2.3	Evaluation of Chroma DB vs Milvus DB and Database Selection

To determine the most suitable vector database for our RAG system, we conducted a comprehensive evaluation of Chroma DB and Milvus DB. The evaluation focused on the following criteria:
•	Performance: Retrieval speed and latency were measured for both databases.
•	Scalability: The ability to handle large-scale datasets with billions of vectors.
•	Hybrid Search Support: Support for both sparse (BM25) and dense (embedding-based) retrieval methods.
•	Cloud-Native Capabilities: Compatibility with cloud platforms for easy deployment and scalability.

Evaluation Results:

•	Milvus DB outperformed Chroma DB in terms of retrieval speed, scalability, and hybrid search capabilities.
•	Milvus DB's support for multiple index types and cloud-native features made it the preferred choice for our RAG system.
Final Selection:
•	Milvus DB was selected as the primary vector database for storing embeddings and facilitating fast retrieval.

2.2.4	Storage and Retrieval Workflow

The final data processing and storage workflow is as follows:
1.	Embedding Generation: Each chunk and document is processed using the BAAI/LLM-Embedder to generate embeddings.
2.	Storage: Embeddings are stored in Milvus DB for efficient retrieval.
3.	Retrieval: During query processing, the system retrieves the most relevant chunks and documents based on the embeddings stored in Milvus DB.
This optimized workflow ensures that the RAG system can handle large-scale, domain-diverse datasets while maintaining high retrieval accuracy and low latency.

