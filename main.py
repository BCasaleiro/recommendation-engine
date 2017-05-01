import numpy as np

class User:
    """Review Class"""

    def __init__(self, user):
        self.user = user
        self.reviews = []

class Review:
    """Review Class"""

    def __init__(self, product, user, helpfulness, score):
        self.product = product
        self.user = user
        self.helpfulness = helpfulness
        self.score = score

def read_file(fname):
    f = open(fname, 'r');
    reviews = []
    products = []

    count = 0
    flag = False
    for line in f:
        lcontents = line.split(': ')
        if lcontents[0] == 'product/productId':
            if ( flag ):
                reviews.append( Review(product, user, helpfulness, score) )
                products.append(product)
            product = line.split(': ')[1].strip('\n')
            flag = True

        elif lcontents[0] == 'review/userId':
            user = line.split(': ')[1].strip('\n')

        elif lcontents[0] == 'review/helpfulness':
            h = line.split(': ')[1].split('/')
            helpf = float(h[0])
            thelpf = float(h[1])
            if thelpf > 0:
                helpfulness =  helpf / thelpf
            else:
                helpfulness = 1.0

        elif lcontents[0] == 'review/score':
            score = float(line.split(': ')[1])

    return products, reviews

def remove_duplicates(p):
   no_duplicates = []
   [no_duplicates.append(i) for i in p if not no_duplicates.count(i)]
   return no_duplicates

def main():
    products, reviews = read_file('movies.txt')
    products = remove_duplicates( sorted(products) )
    


if __name__ == "__main__":
    main()
