GraphRAG:(For Global and Local Search)

Environment:		.venv / Python 3.11.9

Model: 			Qwen/Qwen3-8B

TPM: 			50000

RPM: 			1000

Embedding Model: 	Qwen/Qwen3-Embedding-0.6B

TPM:			50000

RPM:			1000

Chunk size: 		2000

Chunk overlap: 		50











The Query Engine for the garphRAG can complete following tasks:

 	Global search

 	Local search

 	DRIFT search

 	Entity-based Question Generation



Following statements are inputs and outputs of these three tasks using the example provided by the GitHub (*A Christmas Carol* by Charles Dickens)











High-level, summarization question of the book.

For Global search:

 	codes:

 		$ graphrag query \\

 		--root ./ragtest \\

 		--method global \\

 		--query "What are the top themes in this story?"

 		--response-type 'Single Sentence'

 

 	Response:

 		The top theme of the story is the moral and spiritual transformation of Ebenezer Scrooge, driven by compassion, community, and supernatural intervention, as evidenced by his interactions with the Cratchit family, Fred, 		and the three spirits, with the COUNTING-HOUSE symbolizing his materialistic nature \[Data: Reports (29, 18, 21, 9, 103, +more)].



 	Time:

 		Around 4 min



 	Process:

 		-Map Phase/Data Analysis: global\_search\_map\_system\_prompt.txt

 		-Reduce Phase/Synthesis: global\_search\_reduce\_system\_prompt.txt

 		-Knowledge Enhancement: global\_search\_knowledge\_system\_prompt.txt



 	Configuration (in settings.yaml):

 		global\_search:

  		max\_context\_tokens: 3000      	*# Total context for each analyst*

  		data\_max\_tokens: 3000         	*# Data size per analyst*

  		map\_max\_length: 150           	*# Individual analyst report length*

  		reduce\_max\_length: 200        	*# Final synthesized answer length*

  		dynamic\_search\_threshold: 1   	*# Relevance threshold*

  		dynamic\_search\_num\_repeats: 1 	*# Single analysis pass*









Question related to a certain entity of the book.

For Local search:

 	codes:

 		$ graphrag query \\

 		--root ./ragtest \\

 		--method local \\

 		--query "Who is Scrooge and what are his main relationships? Answer in one paragraph of no more than five sentences."

 		--response-type 'Paragraph'

 

 	Response:

 		Ebenezer Scrooge is a miserly businessman who undergoes a transformative journey after interacting with three ghosts: the Ghost of Christmas Past, Present, and Future \[Data: Relationships (15, 34, 170)]. His primary 		relationships include his nephew Fred, who challenges his coldness with warmth and humour during Christmas gatherings \[Data: Entities (156, 14), Relationships (14, 181)], his niece Fan, who shares familial bonds and 		playful moments with Fred \[Data: Entities (119), Relationships (130, 135)], and Jacob Marley, his deceased business partner whose ghost confronts him about his past actions \[Data: Entities (33), Relationships (33, 12)]. 		Scrooge also interacts with Bob Cratchit, his clerk, during the Christmas dinner and a meeting where Cratchit expresses gratitude for Scrooge’s nominal kindness \[Data: Entities (158, 158), Relationships (183, 185, 186)]. 		Additionally, he has connections to characters like the schoolmaster and the undertaker’s man, who represent pivotal moments in his past \[Data: Relationships (56, 155)].

 

 	Time:

 		Around 1 min

 

 	Process:

 		-Single Process: local\_search\_system\_prompt.txt

 

 	Configuration (in settings.yaml):

 		local\_search:

 		max\_context\_tokens: 4000     	*# Total context size for single call*

  		text\_unit\_prop: 0.5         	*# Proportion of text units vs communities*

  		community\_prop: 0.1         	*# Proportion of community data*











Investigative question related to a character of the book.

For DRIFT search:



\*\* Original model (Qwen/Qwen3-8B) does not support JSON, therefore for DRIFT search, the model has been changed into (THUDM/GLM-4-9B-0414), the embedding model also changed into (BAAI/bge-m3)

\*\* TPM: 20000

\*\* RPM: 500

\*\* max output token: 512



 	codes:

 		$ graphrag query \\

 		--root ./ragtest \\

 		--method drift \\

 		--query "How might Scrooge's childhood events have indirectly led to his loneliness in adulthood? Answer in one paragraph."

 		--response-type 'Paragraph'



 	Response:

 		\*\*Exposure to Social Contrasts:\*\* Growing up as the son of a wealthy merchant in London exposed Scrooge to the stark differences between wealth and poverty. This early exposure may have fostered a sense of entitlement 		and detachment from the struggles of others, contributing to a lack of empathy and social connection later in life \[Data: Scrooge's Childhood and Loneliness (1, 2)].

 		\*\*Orphanhood and Neglect:\*\* The death of Scrooge's father left him orphaned, placing him under the care of his cold and authoritarian sister, Fan. This early experience of familial neglect and emotional distance may have 		been a significant factor in his emotional isolation \[Data: Scrooge's Childhood and Loneliness (2)].

 		\*\*Lack of Stable Family Structure:\*\* Fan's subsequent marriage and move to another country further removed Scrooge from any stable family support system. Navigating adulthood with limited emotional support from family 		likely contributed to his sense of being alone \[Data: Scrooge's Childhood and Loneliness (2)].

 		\*\*Rejection of Kindness and Love:\*\* Scrooge's decision to break off his engagement to Belle due to financial concerns rather than emotional connection highlights his obsession with money and rejection of meaningful 			personal relationships. This rejection likely deepened his sense of loneliness  \[Data: Scrooge's Childhood and Loneliness (2)].

 

 	Time:

 		Around 1 min

 

 	Process:

 		-Initial Query Processing: drift\_search\_system\_prompt.txt

 		-Local Context Building: local\_search\_system\_prompt.txt

 		-Data Synthesis: drift\_reduce\_prompt.txt

 		-Follow-up Processing: basic\_search\_system\_prompt.txt

 

 	Configuration (in settings.yaml):

 		drift\_search:

  		concurrency: 1                    	*# Sequential processing*

  		primer\_folds: 1                   	*# Number of primer analyses*

  		data\_max\_tokens: 800              	*# Context size per search*

  		reduce\_max\_tokens: 300            	*# Final synthesis token limit*

  		primer\_llm\_max\_tokens: 800        	*# Primer analysis token limit*

  		n\_depth: 1                        	*# Iteration depth*

  		local\_search\_max\_data\_tokens: 800 	*# Local search context size*

  		local\_search\_text\_unit\_prop: 0.6  	*# Text unit proportion*

  		local\_search\_community\_prop: 0.1  	*# Community data proportion*

  		drift\_k\_followups: 2              	*# Number of follow-up questions*





 





To summarize:

 	- Global Search is more useful for broad, comprehensive analysis across the entire knowledge graph and high-level questions about content.

 	- Local Search is more ideal for direct factual questions where specific information from the most relevant parts of knowledge graph is needed.

 	- DRIFT Search is normally used for investigative and complex analytical questions that require broader context or iterative exploration.

 	- Global Search has no token limits whereas Local and DRIFT Search can encounter token limits while using complex query.

 	- Global Search outputs list of themes \& central players; Local Search outputs list of relevant text chunks/quotes; DRIFT Search outputs synthesized narrative and explaining connections.

 	- Usually, Local Search takes minimum time to process, Global Search takes longer, meanwhile, query time of DRIFT Search depends on query questions and complexity of input articles.



 

