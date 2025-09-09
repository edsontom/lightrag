# from openbb import obb
# output = obb.equity.price.historical("AAPL")
# df = output.to_dataframe()
# print(df)


# from markitdown import MarkItDown
#
# md = MarkItDown(enable_plugins=False) # Set to True to enable plugins
# result = md.convert(r"D:\tmp\壁仞移动AI工作站样机使用说明.pdf")
# print(result.text_content)
# print('----------------------------')
from markitdown import MarkItDown

md = MarkItDown(docintel_endpoint="<document_intelligence_endpoint>")
result = md.convert("https://cn.bing.com/search?q=top+k+top+p&qs=HS&sc=16-0&cvid=11106F250E74485FB2659FB833211C34&FORM=QBLH&sp=1&lq=0")
print(result.text_content)