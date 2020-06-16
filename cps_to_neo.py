from neo4j import GraphDatabase
import pandas as pd
import os
from os import listdir
from pathlib import Path
base_path = Path(__file__).parent
file_path = (base_path / ".../data").resolve()

months = ['July', 'August', 'September', 'October', 'November', 'December']

def find_csv_filenames(path_to_dir, suffix=".csv"):
    filenames = listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]


def feature_engineering(file):
    file = os.path.join(file_path, file)
    df = pd.read_csv(file, skiprows=[0], header=None)
    all_columns = list(df)
    df[all_columns] = df[all_columns].astype(str)
    df = df.applymap(lambda x: x.replace("%", "0"))
    df = df.replace("-", "")
    return df


def write_to_neo(driver, df, month):
    with driver.session() as session:
        with session.begin_transaction() as tr:
            for index, row in df.iterrows():
                tr.run("""        
                    MERGE (m1:Month{month:$month})
                    MERGE (a1:PoliceForce{area:$p0})
                    MERGE (b1:Homicide{area:$p0,convictions:$p1, percentConvictions:$p2, unsuccessful:$p3, percentUnsuccessful:$p4, month:$month})
                    MERGE (b2:AgainstThePerson{area:$p0,convictions:$p5, percentConvictions:$p6, unsuccessful:$p7, percentUnsuccessful:$p8, month:$month})
                    MERGE (b3:SexualOffences{area:$p0,convictions:$p9, percentConvictions:$p10, unsuccessful:$p11, percentUnsuccessful:$p12, month:$month})
                    MERGE (b4:Burglary{area:$p0,convictions:$p13, percentConvictions:$p14, unsuccessful:$p15, percentUnsuccessful:$p16, month:$month})
                    MERGE (b5:Robbery{area:$p0,convictions:$p17, percentConvictions:$p18, unsuccessful:$p19, percentUnsuccessful:$p20, month:$month})
                    MERGE (b6:TheftAndHandling{area:$p0,convictions:$p21, percentConvictions:$p22, unsuccessful:$p23, percentUnsuccessful:$p24, month:$month})
                    MERGE (b7:FraudAndForgery{area:$p0,convictions:$p25, percentConvictions:$p26, unsuccessful:$p27, percentUnsuccessful:$p28, month:$month})
                    MERGE (b8:CriminalDamage{area:$p0,convictions:$p29, percentConvictions:$p30, unsuccessful:$p31, percentUnsuccessful:$p32, month:$month})
                    MERGE (b9:Drugs{area:$p0,convictions:$p33, percentConvictions:$p34, unsuccessful:$p35, percentUnsuccessful:$p36, month:$month})
                    MERGE (b10:PublicOrder{area:$p0,convictions:$p37, percentConvictions:$p38, unsuccessful:$p39, percentUnsuccessful:$p40, month:$month})
                    MERGE (b11:OtherExcludingMotoring{area:$p0,convictions:$p43, percentConvictions:$p42, unsuccessful:$p43, percentUnsuccessful:$p44, month:$month})
                    MERGE (b12:Motoring{area:$p0,convictions:$p45, percentConvictions:$p46, unsuccessful:$p47, percentUnsuccessful:$p48, month:$month})
                    MERGE (b13:AdminFinalised{area:$p0,unsuccessful:$p49, month:$month})
                    MERGE (b14:LMotoringOffences{area:$p0,unsuccessful:$p50, month:$month})
                    MERGE (m1)<-[:IN_MONTH]-(b1)-[:IN_AREA]->(a1)
                    MERGE (m1)<-[:IN_MONTH]-(b2)-[:IN_AREA]->(a1)
                    MERGE (m1)<-[:IN_MONTH]-(b3)-[:IN_AREA]->(a1)
                    MERGE (m1)<-[:IN_MONTH]-(b4)-[:IN_AREA]->(a1)
                    MERGE (m1)<-[:IN_MONTH]-(b5)-[:IN_AREA]->(a1)
                    MERGE (m1)<-[:IN_MONTH]-(b6)-[:IN_AREA]->(a1)
                    MERGE (m1)<-[:IN_MONTH]-(b7)-[:IN_AREA]->(a1)
                    MERGE (m1)<-[:IN_MONTH]-(b8)-[:IN_AREA]->(a1)
                    MERGE (m1)<-[:IN_MONTH]-(b9)-[:IN_AREA]->(a1)
                    MERGE (m1)<-[:IN_MONTH]-(b10)-[:IN_AREA]->(a1)
                    MERGE (m1)<-[:IN_MONTH]-(b11)-[:IN_AREA]->(a1)
                    MERGE (m1)<-[:IN_MONTH]-(b12)-[:IN_AREA]->(a1)
                    MERGE (m1)<-[:IN_MONTH]-(b13)-[:IN_AREA]->(a1)
                    MERGE (m1)<-[:IN_MONTH]-(b14)-[:IN_AREA]->(a1)                  
                """, parameters={'p0': row[0], 'p1': row[1], 'p2': row[2], 'p3': row[3], 'p4': row[4], 'p5': row[5],
                                 'p6': row[6], 'p7': row[7], 'p8': row[8], 'p9': row[9], 'p10': row[10], 'p11': row[11],
                                 'p12': row[12], 'p13': row[13], 'p14': row[14], 'p15': row[15], 'p16': row[16],
                                 'p17': row[17],
                                 'p18': row[18], 'p19': row[19], 'p20': row[20], 'p21': row[21], 'p22': row[22],
                                 'p23': row[23],
                                 'p24': row[24], 'p25': row[25], 'p26': row[26], 'p27': row[27], 'p28': row[28],
                                 'p29': row[29],
                                 'p30': row[30], 'p31': row[31], 'p32': row[32], 'p33': row[33], 'p34': row[34],
                                 'p35': row[35],
                                 'p36': row[36], 'p37': row[37], 'p38': row[38], 'p39': row[39], 'p40': row[40],
                                 'p41': row[41],
                                 'p42': row[42], 'p43': row[43], 'p44': row[44], 'p45': row[45], 'p46': row[46],
                                 'p47': row[47],
                                 'p48': row[48], 'p49': row[49], 'p50': row[50], 'month': month})


if __name__ == '__main__':

    files = sorted(find_csv_filenames(file_path))
    months = sorted(months)

    x = 0
    while x < len(files):
        driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "password"))
        df = feature_engineering(files[x])
        month = months[x]
        write_to_neo(driver, df, month)
        driver.close()
        x += 1

