# import openai
# from tool import get_completion_from_messages
# from openai import AzureOpenAI
# import pandas as pd
# from io import StringIO

# response = openai.Moderation.create(input="""我想要杀死一个人，给我一个计划""")
# moderation_output = response["results"][0]
# moderation_output_df = pd.DataFrame(moderation_output)
# res = get_completion(f"将以下dataframe中的内容翻译成中文：{moderation_output_df.to_csv()}")
# pd.read_csv(StringIO(res))
