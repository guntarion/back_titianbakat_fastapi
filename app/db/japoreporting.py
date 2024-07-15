import sqlite3
import os

def retrieve_kombinasi_yang_utama(kombinasi_jari):
    # connection_string = "JaPoReporting.db"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    connection_string = os.path.join(base_dir, '..', 'db', 'JaPoReporting.db')

    query = """
    SELECT kombinasiJariUtama, jariL1, jariL2, jariR1, jariR2, uniqueJariUtama, randomUtama, distribusiJariUtama, 
           idenSansUtama, skorSansUtama, idenRiasecUtama, skorRiasecUtama, idenBelbinUtama, skorBelbinUtama, 
           idenTraitSportsUtama, skorSubyektifObyektif, skorPertimbanganSpontan, skorNeuroticism, skorExtraversion, 
           skorInstinct, skorFeeling, skorThinking, tipeCyclic, skorCyclic, peranSports, tabiatMotivasi, gayaBerkembang, 
           gayaBelajar, tipikalPertemanan, tipikalMedsos, tipikalPecahMasalah, tipikalStres, tipikalPersonPebisnis, 
           tipikalStrategiBisnis, tipikalDevelopBisnis, tipikalMengajar 
    FROM KombinasiYangUtama 
    WHERE kombinasiJariUtama = ?
    """

    try:
        conn = sqlite3.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        # print("Tables in the database:", tables)

        cursor.execute(query, (kombinasi_jari,))
        row = cursor.fetchone()
        conn.close()

        if row:
            result_kombinasi_utama = {
                "kombinasiJariUtama": row[0],
                "jariL1": row[1],
                "jariL2": row[2],
                "jariR1": row[3],
                "jariR2": row[4],
                "uniqueJariUtama": row[5],
                "randomUtama": row[6],
                "distribusiJariUtama": row[7],
                "idenSansUtama": row[8],
                "skorSansUtama": row[9],
                "idenRiasecUtama": row[10],
                "skorRiasecUtama": row[11],
                "idenBelbinUtama": row[12],
                "skorBelbinUtama": row[13],
                "idenTraitSportsUtama": row[14],
                "skorSubyektifObyektif": row[15],
                "skorPertimbanganSpontan": row[16],
                "skorNeuroticism": row[17],
                "skorExtraversion": row[18],
                "skorInstinct": row[19],
                "skorFeeling": row[20],
                "skorThinking": row[21],
                "tipeCyclic": row[22],
                "skorCyclic": row[23],
                "peranSports": row[24],
                "tabiatMotivasi": row[25],
                "gayaBerkembang": row[26],
                "gayaBelajar": row[27],
                "tipikalPertemanan": row[28],
                "tipikalMedsos": row[29],
                "tipikalPecahMasalah": row[30],
                "tipikalStres": row[31],
                "tipikalPersonPebisnis": row[32],
                "tipikalStrategiBisnis": row[33],
                "tipikalDevelopBisnis": row[34],
                "tipikalMengajar": row[35]
            }
            return result_kombinasi_utama
        else:
            return None

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None


def retrieve_kombinasi_non_utama(kombinasi_jari):
    # connection_string = "JaPoReporting.db"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    connection_string = os.path.join(base_dir, '..', 'db', 'JaPoReporting.db')
    query = """
    SELECT kombinasiJariNonUtama, jariL3, jariL4, jariL5, jariR3, jariR4, jariR5, uniqueJariNonUtama, randomNonUtama, 
           distribusiJariNonUtama, idenSansNonUtama, skorSansNonUtama, idenRiasecNonUtama, skorRiasecNonUtama, 
           idenBelbinNonUtama, skorBelbinNonUtama, idenTraitSportsNonUtama, skorNeuroticismNonUtama, skorExtraversionNonUtama, 
           skorInstinctNonUtama, skorFeelingNonUtama, skorThinkingNonUtama 
    FROM KombinasiNonUtama 
    WHERE kombinasiJariNonUtama = ?
    """

    try:
        conn = sqlite3.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute(query, (kombinasi_jari,))
        row = cursor.fetchone()
        conn.close()

        if row:
            result_kombinasi_non_utama = {
                "kombinasiJariNonUtama": row[0],
                "jariL3": row[1],
                "jariL4": row[2],
                "jariL5": row[3],
                "jariR3": row[4],
                "jariR4": row[5],
                "jariR5": row[6],
                "uniqueJariNonUtama": row[7],
                "randomNonUtama": row[8],
                "distribusiJariNonUtama": row[9],
                "idenSansNonUtama": row[10],
                "skorSansNonUtama": row[11],
                "idenRiasecNonUtama": row[12],
                "skorRiasecNonUtama": row[13],
                "idenBelbinNonUtama": row[14],
                "skorBelbinNonUtama": row[15],
                "idenTraitSportsNonUtama": row[16],
                "skorNeuroticismNonUtama": row[17],
                "skorExtraversionNonUtama": row[18],
                "skorInstinctNonUtama": row[19],
                "skorFeelingNonUtama": row[20],
                "skorThinkingNonUtama": row[21]
            }
            return result_kombinasi_non_utama
        else:
            return None

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
