import csv
import random
import string

# Source for articles: https://www.kaggle.com/snapcrack/all-the-news

print('''INSERT INTO documents (title, min_security_level, content)
VALUES ''')

count = 0
with open('articles1.csv') as f:
    articlereader = csv.reader(f, delimiter=',', quotechar='"')
    for row in articlereader:
        if count > 0:
            title = row[2]
            content = row[9]
            print("('%s', %d, '%s')," % (title.replace('\\', '').replace("'", "\\'"), random.randint(0, 4), content.replace('\\', '').replace("'", "\\'")))
        count += 1
        if count > 1000:
            break

print("('SUPER SECRET', 5, 'BLACKHAT_PASSWORD=T1mel3ssT1mingAtt4cks');")

print('''
INSERT INTO users (name, security_level)
VALUES
('anonymous', 0),''')
for x in range(500):
    print("('%s', %d)," % (''.join(random.choice(string.ascii_letters + string.digits) for i in range(random.randint(4, 10))), random.randint(0, 4)))
print("('admin', 5);")
