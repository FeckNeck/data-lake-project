import pandas as pd

# Read the data
df = pd.read_csv('./data/data_processed.csv', delimiter=',')

TRANSFORMATIONS = [
    'language',
    'stopwords_removed',
    'word_count',
    'char_count',
    'sentence_count',
    'numerics',
    'sentiment',
    'subjectivity'
]

NAMES = [
    "Titouan",
    "Anne",
    "Anne",
    "Sheepy",
    "Michelle",
    "Jacko",
    "Walibi",
    "Cimboo",
    "Rudolphe",
    "Buzzbee",
]

# for each dataset text, create a neo4j node for each transformation and store it in txt file
with open('./db/init_db.txt', 'w') as f:
    for index, row in df.iterrows():
        f.write(f'CREATE (n:Blog: User {{\n')
        f.write(f'\ttext_id: {row["id"]},\n')
        f.write(f'\tname: "{NAMES[index]}",\n')
        f.write(f'\tgender: "{row["gender"]}",\n')
        f.write(f'\tage: {row["age"]},\n')
        f.write(f'\ttopic: "{row["topic"]}",\n')
        f.write(f'\tsign: "{row["sign"]}",\n')
        f.write(f'\tdate: "{row["date"]}",\n')
        f.write(f'\ttext: "{row["text"]}"\n')
        f.write(f'}});\n')
        for transformation in TRANSFORMATIONS:
            if transformation in ['language', 'stopwords_removed']:
                f.write(f'CREATE (n:Transformation: {transformation} {{text_id:{row["id"]}, value: "{row[transformation]}"}});\n')
                f.write(f'match (b:Blog:User), (n:Transformation: {transformation})\n')
                f.write(f'where b.text_id = {row["id"]} AND n.text_id={row["id"]}\n')
                f.write(f'create (b)-[r:{transformation}]->(n);\n\n')
            else:
                f.write(f'CREATE (n:Transformation: {transformation} {{text_id:{row["id"]}, value: {row[transformation]}}});\n')
                f.write(f'match (sr:Transformation: stopwords_removed), (n:Transformation: {transformation})\n')
                f.write(f'where sr.text_id = {row["id"]} AND n.text_id={row["id"]}\n')
                f.write(f'create (sr)-[r:{transformation}]->(n);\n\n')
        f.write('\n\n\n')
    f.close()