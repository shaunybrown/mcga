import pandas as pd
import geopandas as gpd
import os
from pathlib import Path
from neo4j import GraphDatabase

base_path = Path(__file__).parent
file_path = (base_path / ".../data").resolve()
file = os.path.join(file_path, "Police_Force_Areas__December_2016__Boundaries.shp")
driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "password"))


def write_to_neo(driver, df):
    with driver.session() as session:
        with session.begin_transaction() as tr:
            for index, row in df.iterrows():
                tr.run("""
                    MATCH (a:PoliceForce{area:$p0})
                    SET a.wkt = $p2 
                    """, parameters={'p0': row["pfa16nm"], 'p2': str(row["geometry"])})


df = gpd.read_file(file)
print(df)
write_to_neo(driver, df)
driver.close()




