question.json is used in rag for extractiong the questions it should in the same directory as rag

then we will run the rag 

choose option 1 then it will generate all QA pairs in generated_qa_pairs.json 
then it will give a option of review (y/n)  click y to review then all the options will be seen selected accordingly after all then this will be saved in reviewed_qa_pairs.json

then this reviewed_qa_pairs.json/generated_qa_pairs.json should be in the same directory as the agent.py as it take all the question answers form it

in agent.py we have used reviewed_qa_pairs.json this has to change in agent.py if you don't want to review but as you said manual correction we have explictly used reviewed_qa_pairs.json

at last run the agent.py 

it will fill the form
