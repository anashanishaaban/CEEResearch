from markitdown import MarkItDown
import sys

md = MarkItDown()
result = md.convert("/Users/anasshaaban/ResearchProject/dashboard/dashboardapp/saved/070575.pdf")
print(result.text_content)

with open("/Users/anasshaaban/ResearchProject/dashboard/dashboardapp/saved/070575.txt", "a") as myfile:
    myfile.write(result.text_content)
    print("Done")

myfile.close()