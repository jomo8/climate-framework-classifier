import pandas as pd
from openai import OpenAI
client = OpenAI(api_key="API-KEY")


# FIRST PROMPT

# Read the CSV file
df = pd.read_csv('1.4/nasdaq_screener_1.4.8.csv')
csv_content = df["Name"].to_string()

first_prompt="I am giving you a CSV from the NASDAQ website that contains the names of public trades. Fix each name to contain commonly used name for each company that I can search online. For example, an entry like 'AGNC Investment Corp. Depositary Shares rep 6.875% Series D Fixed-to-Floating Cumulative Redeemable Preferred Stock' should be 'AGNC Investment Corp.'. Ignore duplicate company names, leaving only 1 company name per company. Give me your answer in the format of a CSV file, where each name is a newline. Here are the companies: " + csv_content
frameworks="CSRD, CBAM"

first_completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": first_prompt},
    ]
)

# Write the CSV data to a file
with open("1.4/company_names_1.4.8.txt", "w") as file:
    file.write(first_completion.choices[0].message.content.strip())
print("CSV file created successfully!")



# SECOND PROMPT

with open('1.4/company_names_1.4.8.txt', 'r') as file:
    cur_companies = file.read()

second_prompt="Using your knowledge on publicly traded companies, tell me which companies comply with these climate frameworks: " + frameworks + ". Your response must contain a column for the company name and a column for each framework with `YES` or `NO`. Your response should say `YES` if the company meets the requirements to be obligated to disclose for the framework, and `NO` if the company does not meet the requirements to be obligated for the framework. For example, a company with more than $150 million in annual EU revenues must comply with CSRD and would be marked as`YES`. Give me your answer in the format of a CSV file, where each name is a newline. Ignore duplicate companies. Here are the companies: \n" + cur_companies
# print(second_prompt)

second_completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": second_prompt},
    ]
)

# print(first_completion.choices[0].message.content)
print(second_completion.choices[0].message.content)

# Write the CSV data to a file
with open("1.4/final_companies_1.4.8.csv", "w") as file:
    file.write(second_completion.choices[0].message.content.strip())

print("CSV file created successfully!")