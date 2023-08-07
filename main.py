# @Author: chesterblue
# @File Name: main.py
from query.fofa import fofaScan
from query.hunter import hunterScan
import click

def writeRestoFile(filename, res):
    with open(filename, "a+") as fp:
        for url in res:
            fp.write(url+"\r\n")

def printRes(res):
    for url in res:
        print(url)

def getResFromfofa(query, num):
    fofa = fofaScan(query, num)
    results = fofa.getResult()
    return results

def getResFromhunter(query, num):
    hunter = hunterScan(query, num)
    results = hunter.getResult()
    return results
    

@click.command()
@click.option("-q", required="true", help="what you want to query")
@click.option("-s", required="true", help="search engines[fofa,hunter]")
@click.option("-n", default=10, help="numbers of result.default=10")
@click.option("-o", help="file to write output results")
def main(q, s, n, o):
    query = q
    num = n
    engines = {
        "fofa": getResFromfofa,
        "hunter": getResFromhunter
    }
    search_engine = engines.get(s.lower())
    if search_engine:
        results = search_engine(query, num)
        printRes(results)
        if o:
            writeRestoFile(o, results)
    else:
        print("Not found search engine: %s"%s)

if __name__== "__main__":
    main()
        
