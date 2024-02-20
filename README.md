The goal of the experiment is to try to create some more personalised experience for a BOI customer who is choosing a savings account.

The technologies used: ChatGPT 4, Google Cloud with Vertex AI enabled (code was written and ran in Vertex AI workbench).

ChatGPT was instructed to create a fake bank statement for a person living in Ireland 6 months with a positive balance.

Savings accounts descriptions were downloaded from bankofireland.com website:

https://personalbanking.bankofireland.com/app/uploads/2570642-GoalSaver-Customer-Information-Sheet-V2-final.pdf

https://personalbanking.bankofireland.com/app/uploads/Customer-Infomation-Sheet-Advantage-Fixed-Term-Deposit.pdf

https://personalbanking.bankofireland.com/app/uploads/Customer-Info-Sheet-SuperSaver-Account-1.pdf

ChatGPT was instructed to create a recommendation based on the pdf documents and the fake bank statement.

Vertex AI was used to create functions to chat with the pdfs :) and compare them.

The ultimate goal of the experiment is to reproduce the answer that ChatGPT gave using the Vertex AI framework.


