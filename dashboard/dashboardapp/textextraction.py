from markitdown import MarkItDown
import sys

md = MarkItDown()
result = md.convert("/Users/anasshaaban/ResearchProject/dashboard/dashboardapp/080630.pdf")
print(result.text_content)

with open("results.txt", "a") as myfile:
    myfile.write(result.text_content)
    print("Done")

myfile.close()