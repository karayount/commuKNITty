import json

# the search below has ~2 million results
# http://www.ravelry.com/projects/search#weight=lace%7Cfingering%7Csport%7Cdk%7Cworsted%7Caran%7Cbulky&pc=cardigan%7Cpullover%7Cvest%7Csocks%7Cfingerless%7Cgloves%7Cmittens%7Cbeanie-toque%7Cearflap%7Cscarf%7Cshawl-wrap%7Ccowl&sort=best&yardage=0%7C2000&status=finished&view=cards&craft=knitting&ravelry-download=yes



with open('projects_data.txt', 'w') as outfile:
    json.dump(data, outfile)