import sys
import json
import os.path
import numpy as np

class User:
    """User Class"""

    def __init__(self, user):
        self.user = user
        self.reviews = []

class Review:
    """Review Class"""

    def classification(self):
        return float(self.score) * float(self.helpfulness)

    def __init__(self, product, user, helpfulness, score):
        self.product = product
        self.user = user
        self.helpfulness = helpfulness
        self.score = score

class Recommendation:
    """Recommendation Class"""

    def __init__(self, product, score):
        self.product = product
        self.score = score
        self.reviews = []

def obj_dict(obj):
    return obj.__dict__

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

def process_users(reviews):
    user_id = []
    users = []

    for r in reviews:
        if r.user in user_id:
            users[ user_id.index(r.user) ].reviews.append(r)
        else:
            user_id.append(r.user)
            users.append( User(r.user) )
            users[len(users) - 1].reviews.append(r)

    return users

def collaborative_filtering(users, products, n):
    matrix = np.zeros((n, n))

    for u in users:
        n_r = len(u.reviews)
        for r_index in range(n_r - 1):
            for r2_index in range(r_index + 1, n_r):
                matrix[ products.index( u.reviews[r_index].product ) ][ products.index( u.reviews[r2_index].product ) ] += u.reviews[r2_index].classification()

    return matrix

def find_user(user, users):
    for i, u in enumerate(users):
        if u.user == user:
            return u
    return -1

def already_reviewed(product, reviews):
    for r in reviews:
        if r.product == product:
            return True
    return False

def recommend(u, products, matrix, n):
    recommended = []
    for i, r in enumerate(u.reviews):
        possible = matrix[:,products.index(r.product)]
        for k, p in enumerate(possible):
            if (p > 0 and not already_reviewed(products[k], u.reviews)):
                flag = True
                for rec in recommended:
                    if rec.product == products[k]:
                        flag = False
                        if rec.score < p:
                            rec.score = p
                if flag:
                    recommended.append( Recommendation(products[k], p) )

    recommended.sort(key=lambda x: x.score, reverse=True)

    if int(n) > len(recommended):
        n = len(recommended)

    for i in range(int(n)):
        print '{}\t{}'.format(recommended[i].product, recommended[i].score)

def main(user, n):
    if os.path.isfile('matrix.txt') and os.path.isfile('users.json') and os.path.isfile('products.txt'):
        matrix = np.loadtxt('matrix.txt')
        products_file = open('products.json', 'r')
        products = json.load(products_file)
        users_file = open('users.json', 'r')
        users = json.load(users_file)
    else:
        print 'Reading File...'
        products, reviews = read_file('movies-small.txt')
        print 'Processing Products...'
        products = remove_duplicates( sorted(products) )
        products_file = open('products.json', 'w')
        json.dump(products, products_file, default=obj_dict)

        print 'Processing Users...'
        users = process_users(reviews)
        users.sort(key=lambda x: x.user, reverse=True)
        users_file = open('users.json', 'w')
        json.dump(users, users_file, default=obj_dict)

        print 'Collaborative Filtering Item-Item...'
        matrix = collaborative_filtering(users, products, len(products))
        print 'Printing Matrix to file...'
        np.savetxt('matrix.txt', matrix)

    u = find_user(user, users)
    if u != -1:
        recommend(u, products, matrix, n)
    else:
        print 'User not found.'

if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print 'Invalid number of arguments. Expected 2, {} given.'.format(len(sys.argv) - 1)
        print 'Try python main.py [userId] [NumberOfRecommendations]'
