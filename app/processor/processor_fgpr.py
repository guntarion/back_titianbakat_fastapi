import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.japoreporting import retrieve_kombinasi_yang_utama, retrieve_kombinasi_non_utama
from datetime import datetime
from pprint import pprint

def debug_print(message, debug_flag=False):
    if debug_flag:
        print(message)

def convert_fingertype(fingertype):
    conversion_map = {
        "archessimple": "arch",
        "archestented": "tented",
        "loopplain": "loop",
        "loopreverse": "radial",
        "loopdouble": "double",
        "whorlsplain": "whorl",
        "whorlspeacock": "peacock"
    }
    return conversion_map.get(fingertype, fingertype)

def process_fingerprint_data(data):
    # print("Received data:", data)
    ridge_values = {k: float(v) for k, v in data.items() if '_ridgevalue' in k}
    # print("Ridge values:", ridge_values)
    processed_ridge_values = ridgevalue_processing(ridge_values)
    
    # Capture and convert `_fingertype`
    fingertype_values = {k: convert_fingertype(
        v) for k, v in data.items() if '_fingertype' in k}
    print("Finger type values:", fingertype_values)

    fingertypename_values = [v for k, v in fingertype_values.items()]
    print("Finger type name values:", fingertypename_values)

    kombinasi_jari_yang_utama = f"{fingertype_values['L1_fingertype']}_{fingertype_values['L2_fingertype']}_{fingertype_values['R1_fingertype']}_{fingertype_values['R2_fingertype']}"
    kombinasi_jari_non_utama = f"{fingertype_values['L3_fingertype']}_{fingertype_values['L4_fingertype']}_{fingertype_values['L5_fingertype']}_{fingertype_values['R3_fingertype']}_{fingertype_values['R4_fingertype']}_{fingertype_values['R5_fingertype']}"

    print("kombinasi jari utama", kombinasi_jari_yang_utama)
    print("kombinasi jari NON utama", kombinasi_jari_non_utama)

    # Process fingertype
    processed_finger_type = fingertype_processing(kombinasi_jari_yang_utama, kombinasi_jari_non_utama, fingertypename_values)

    processed_sports_talent = identifikasi_sports_talent(fingertypename_values)

    return {
        'ridge_values': processed_ridge_values,
        'fingertype_values': processed_finger_type,
        'sports_talent': processed_sports_talent,
    }

def ridgevalue_processing(ridge_values):
    # Step #1 - Adjust values and calculate totals
    adjusted_values = {k: (v * 100 if v < 20 else v) for k, v in ridge_values.items()}
    # print("Adjusted values:", adjusted_values)
    
    total_ridges = sum(adjusted_values.values())
    total_right_hand = sum([adjusted_values[k] for k in adjusted_values if 'R' in k])
    total_left_hand = sum([adjusted_values[k] for k in adjusted_values if 'L' in k])
    
    # Step #2 - Count the number of arches (ridgevalue is 0)
    arch_count = sum([1 for v in adjusted_values.values() if v == 0])
    
    # Step #3 - Allocate values for arches
    if arch_count > 0:
        difference = abs(total_right_hand - total_left_hand)
        allocation_value = difference / arch_count
        
        adjusted_values = {k: (allocation_value if v == 0 else v) for k, v in adjusted_values.items()}
    
    # Calculate reverse values
    reverse_values = {k: (1 / v) for k, v in adjusted_values.items()}
    total_reverse = sum(reverse_values.values())
    
    # Calculate percentages
    percentages = {k: (v / total_reverse) for k, v in reverse_values.items()}
    print("Percentages:", percentages)
    
    # Hemisphere calculation
    hemisphere_left = round(sum([percentages[k] for k in percentages if 'L' in k]) * 100, 2)
    hemisphere_right = round(sum([percentages[k] for k in percentages if 'R' in k]) * 100, 2)
    
    # Learning styles
    learning_keys = ['L3_ridgevalue', 'L4_ridgevalue', 'L5_ridgevalue', 'R3_ridgevalue', 'R4_ridgevalue', 'R5_ridgevalue']
    total_learning_styles = sum([percentages.get(k, 0) for k in learning_keys])
    learning_styles = {
        'kinesthetic_tactile': round((percentages.get('L3_ridgevalue', 0) / total_learning_styles) * 100, 2),
        'auditory_musical': round((percentages.get('L4_ridgevalue', 0) / total_learning_styles) * 100, 2),
        'visual_picture': round((percentages.get('L5_ridgevalue', 0) / total_learning_styles) * 100, 2),
        'kinesthetic_body': round((percentages.get('R3_ridgevalue', 0) / total_learning_styles) * 100, 2),
        'auditory_linguistic': round((percentages.get('R4_ridgevalue', 0) / total_learning_styles) * 100, 2),
        'visual_text': round((percentages.get('R5_ridgevalue', 0) / total_learning_styles) * 100, 2),
    }
    learning_styles['visual'] = round((learning_styles['visual_picture'] + learning_styles['visual_text']) / 2, 2)
    learning_styles['auditory'] = round((learning_styles['auditory_linguistic'] + learning_styles['auditory_musical']) / 2, 2)
    learning_styles['kinesthetic'] = round((learning_styles['kinesthetic_body'] + learning_styles['kinesthetic_tactile']) / 2, 2)
    
    # Work styles
    work_styles = {
        'manager': round((percentages.get('L1_ridgevalue', 0) + percentages.get('R1_ridgevalue', 0)) * 100, 2),
        'initiator': round((percentages.get('L2_ridgevalue', 0) + percentages.get('R2_ridgevalue', 0)) * 100, 2),
        'executor': round((percentages.get('L3_ridgevalue', 0) + percentages.get('R3_ridgevalue', 0)) * 100, 2),
        'communicator': round((percentages.get('L4_ridgevalue', 0) + percentages.get('R4_ridgevalue', 0)) * 100, 2),
        'trend': round((percentages.get('L5_ridgevalue', 0) + percentages.get('R5_ridgevalue', 0)) * 100, 2),
    }
    
    # Latent intelligence
    latent_intelligence = {
        'technical_visual': round(percentages.get('R5_ridgevalue', 0) * 100, 2),
        'artistic_visual': round(percentages.get('L5_ridgevalue', 0) * 100, 2),
        'visual_spatial': round((percentages.get('L5_ridgevalue', 0) + percentages.get('R5_ridgevalue', 0)) / 2 * 100, 2),
        'technical_audio_communication': round(percentages.get('R4_ridgevalue', 0) * 100, 2),
        'artistic_audio_communication': round(percentages.get('L4_ridgevalue', 0) * 100, 2),
        'technical_movement': round(percentages.get('R3_ridgevalue', 0) * 100, 2),
        'artistic_movement': round(percentages.get('L3_ridgevalue', 0) * 100, 2),
        'kinesthetic': round((percentages.get('R3_ridgevalue', 0) + percentages.get('L3_ridgevalue', 0)) / 2 * 100, 2),
        'rational_logic': round(percentages.get('R2_ridgevalue', 0) * 100, 2),
        'imagination_conceptual': round(percentages.get('L2_ridgevalue', 0) * 100, 2),
        'intrapersonal': round(percentages.get('R1_ridgevalue', 0) * 100, 2),
        'interpersonal': round(percentages.get('L1_ridgevalue', 0) * 100, 2),
    }
    
    # Debug output
    '''
    print("Hemisphere left: {:.2f}".format(hemisphere_left))
    print("Hemisphere right: {:.2f}".format(hemisphere_right))
    for k, v in learning_styles.items():
        print("Learning style - {}: {:.2f}".format(k, v * 100))
    for k, v in work_styles.items():
        print("Work style - {}: {:.2f}".format(k, v * 100))
    for k, v in latent_intelligence.items():
        print("Latent intelligence - {}: {:.2f}".format(k, v * 100))
    '''
    
    # Final results
    return {
        'hemisphere_left': hemisphere_left,
        'hemisphere_right': hemisphere_right,
        'learning_styles': learning_styles,
        'work_styles': work_styles,
        'latent_intelligence': latent_intelligence,
    }

from collections import defaultdict
def count_spesific_fingerprint_type_occurrence(fingers):
    fingerprint_spesific_counts = defaultdict(int)
    fingerprintTypes = ["arch", "tented", "loop", "radial", "double", "whorl", "peacock"]
    for fingerprintType in fingerprintTypes:
        fingerprint_spesific_counts[fingerprintType] = 0
    for fingerprintType in fingers:
        if fingerprintType in fingerprint_spesific_counts:
            fingerprint_spesific_counts[fingerprintType] += 1
    debug_print("fingerprint_spesific_counts : " + str(fingerprint_spesific_counts), debug_flag=True)
    return fingerprint_spesific_counts

def count_generic_fingerprint_type_occurrence(fingerprint_spesific_counts):
    fingerprint_generic_counts = defaultdict(int)

    archtype = fingerprint_spesific_counts["arch"] + fingerprint_spesific_counts["tented"]
    whorltype = fingerprint_spesific_counts["double"] + fingerprint_spesific_counts["whorl"] + fingerprint_spesific_counts["peacock"]
    looptype = fingerprint_spesific_counts["loop"]
    radialtype = fingerprint_spesific_counts["radial"]

    fingerprint_generic_counts["archtype"] = archtype
    fingerprint_generic_counts["whorltype"] = whorltype
    fingerprint_generic_counts["looptype"] = looptype
    fingerprint_generic_counts["radialtype"] = radialtype

    debug_print("fingerprint_generic_counts: " + str(fingerprint_generic_counts), debug_flag=True)

    return fingerprint_generic_counts

def generate_rank_and_skoring_sanskerta(kombinasiYangUtamaInfo, kombinasiNonUtamaInfo, fingertypename_values):
    listYangUtama = kombinasiYangUtamaInfo["idenSansUtama"]
    skorYangUtama = kombinasiYangUtamaInfo["skorSansUtama"]
    listNonUtamaOri = kombinasiNonUtamaInfo["idenSansNonUtama"]
    skorNonUtamaOri = kombinasiNonUtamaInfo["skorSansNonUtama"]

    debug_print("⚠️", debug_flag=True)
    debug_print("listYangUtama : " + str(listYangUtama), debug_flag=True)
    debug_print("listNonUtamaOri : " + str(listNonUtamaOri), debug_flag=True)

    randomValueNonUtama = float(kombinasiNonUtamaInfo["randomNonUtama"])
    if randomValueNonUtama < 0.5:
        randomValueNonUtama += 0.5

    listYangUtamaArray = listYangUtama.split('_')
    skorYangUtamaArray = skorYangUtama.split('_')

    listNonUtamaOriArray = listNonUtamaOri.split('_')
    skorNonUtamaOriArray = skorNonUtamaOri.split('_')

    dictYangUtama = {listYangUtamaArray[i]: float(skorYangUtamaArray[i]) for i in range(len(listYangUtamaArray))}

    dictSanskritYangUtama = {}
    
    skor_mahitala_yang_utama = dictYangUtama.get("mahitala", 0.0)
    skor_widigda_yang_utama = dictYangUtama.get("widigda", 0.0)
    skor_katresnan_yang_utama = dictYangUtama.get("katresnan", 0.0)
    skor_wingwang_yang_utama = dictYangUtama.get("wingwang", 0.0)
    
    dictSanskritYangUtama["skor_mahitala_yang_utama"] = skor_mahitala_yang_utama
    dictSanskritYangUtama["skor_widigda_yang_utama"] = skor_widigda_yang_utama
    dictSanskritYangUtama["skor_katresnan_yang_utama"] = skor_katresnan_yang_utama
    dictSanskritYangUtama["skor_wingwang_yang_utama"] = skor_wingwang_yang_utama
    
    print(dictSanskritYangUtama)


    dictNonUtamaOri = {listNonUtamaOriArray[i]: float(skorNonUtamaOriArray[i]) for i in range(len(listNonUtamaOriArray))}
    

    
    debug_print("dictYangUtama : " + str(dictYangUtama), debug_flag=True)
    debug_print("dictNonUtamaOri : " + str(dictNonUtamaOri), debug_flag=True)
    

    dictNonUtama = {k: v for k, v in dictNonUtamaOri.items(
    ) if k not in dictYangUtama and k != "none"}

    debug_print("dictNonUtama : " + str(dictNonUtama), debug_flag=True)
    debug_print("skorYangUtamaArray : " + str(skorYangUtamaArray), debug_flag=True)
    debug_print("skorNonUtamaOriArray : " + str(skorNonUtamaOriArray), debug_flag=True)

    fingerprint_spesific_counts = count_spesific_fingerprint_type_occurrence(fingertypename_values)
    fingerprint_generic_counts = count_generic_fingerprint_type_occurrence(fingerprint_spesific_counts)

    lowestFromYangUtama = min([v for v in dictYangUtama.values() if v > 0])

    if lowestFromYangUtama < 5:
        substractorForNonUtama = 1
    elif lowestFromYangUtama < 10:
        substractorForNonUtama = 2
    elif lowestFromYangUtama < 20:
        substractorForNonUtama = 3
    elif lowestFromYangUtama < 30:
        substractorForNonUtama = 5
    elif lowestFromYangUtama < 40:
        substractorForNonUtama = 8
    elif lowestFromYangUtama < 50:
        substractorForNonUtama = 12
    elif lowestFromYangUtama < 60:
        substractorForNonUtama = 17
    elif lowestFromYangUtama < 70:
        substractorForNonUtama = 23
    elif lowestFromYangUtama < 80:
        substractorForNonUtama = 30
    elif lowestFromYangUtama < 90:
        substractorForNonUtama = 38
    elif lowestFromYangUtama < 100:
        substractorForNonUtama = 47
    else:
        substractorForNonUtama = 50

    highestAllowedFromNonUtama = lowestFromYangUtama - substractorForNonUtama

    if dictNonUtama:
        highestFromNonUtama = max(dictNonUtama.values())
        divisorForNonUtama = highestAllowedFromNonUtama / highestFromNonUtama
        dictNonUtama = {k: v * divisorForNonUtama for k,
                        v in dictNonUtama.items()}

    dictMerge = {k: v for k, v in dictYangUtama.items() if k != "none"}
    dictMerge.update(dictNonUtama)

    while len(dictMerge) < 4:
        for keyToCheck in ["katresnan", "widigda", "wingwang", "mahitala"]:
            if keyToCheck not in dictMerge:
                dictMerge[keyToCheck] = randomValueNonUtama * \
                    min(dictMerge.values())
            if len(dictMerge) >= 4:
                break

    dictMergeList = list(dictMerge.items())

    dictMergeList.sort(key=lambda x: x[1], reverse=True)

    nameSanskertaRank_1, skorSanskertaRank_1 = dictMergeList[0]
    nameSanskertaRank_2, skorSanskertaRank_2 = dictMergeList[1]
    nameSanskertaRank_3, skorSanskertaRank_3 = dictMergeList[2]
    nameSanskertaRank_4, skorSanskertaRank_4 = dictMergeList[3]

    SkorMahitala = int(round(dictMerge.get("mahitala", 0)))
    SkorWidigda = int(round(dictMerge.get("widigda", 0)))
    SkorKatresnan = int(round(dictMerge.get("katresnan", 0)))
    SkorWingwang = int(round(dictMerge.get("wingwang", 0)))

    dictRankScoreSanskerta = {
        nameSanskertaRank_1: int(round(skorSanskertaRank_1)),
        nameSanskertaRank_2: int(round(skorSanskertaRank_2)),
        nameSanskertaRank_3: int(round(skorSanskertaRank_3)),
        nameSanskertaRank_4: int(round(skorSanskertaRank_4)),
    }

    print("dictRankScoreSanskerta: ", dictRankScoreSanskerta)
    return dictRankScoreSanskerta

def generate_rank_and_skoring_hollandcodes(kombinasiYangUtamaInfo, kombinasiNonUtamaInfo):
    listYangUtama = kombinasiYangUtamaInfo["idenRiasecUtama"]
    skorYangUtama = kombinasiYangUtamaInfo["skorRiasecUtama"]
    listNonUtamaOri = kombinasiNonUtamaInfo["idenRiasecNonUtama"]
    skorNonUtamaOri = kombinasiNonUtamaInfo["skorRiasecNonUtama"]
    randomValueNonUtama = float(kombinasiNonUtamaInfo["randomNonUtama"])

    if randomValueNonUtama < 0.5:
        randomValueNonUtama += 0.5

    listYangUtamaArray = listYangUtama.split('_')
    skorYangUtamaArray = list(map(float, skorYangUtama.split('_')))
    listNonUtamaOriArray = listNonUtamaOri.split('_')
    skorNonUtamaOriArray = list(map(float, skorNonUtamaOri.split('_')))

    dictYangUtama = {listYangUtamaArray[i]: skorYangUtamaArray[i] for i in range(len(listYangUtamaArray))}
    dictNonUtamaOri = {listNonUtamaOriArray[i]: skorNonUtamaOriArray[i] for i in range(len(listNonUtamaOriArray))}

    dictNonUtama = {k: v for k, v in dictNonUtamaOri.items() if k not in dictYangUtama and k != "none"}

    lowestFromYangUtama = min(v for v in dictYangUtama.values() if v > 0)

    if lowestFromYangUtama < 5:
        substractorForNonUtama = 1
    elif lowestFromYangUtama < 10:
        substractorForNonUtama = 2
    elif lowestFromYangUtama < 20:
        substractorForNonUtama = 3
    elif lowestFromYangUtama < 30:
        substractorForNonUtama = 5
    elif lowestFromYangUtama < 40:
        substractorForNonUtama = 8
    elif lowestFromYangUtama < 50:
        substractorForNonUtama = 12
    elif lowestFromYangUtama < 60:
        substractorForNonUtama = 17
    elif lowestFromYangUtama < 70:
        substractorForNonUtama = 23
    elif lowestFromYangUtama < 80:
        substractorForNonUtama = 30
    elif lowestFromYangUtama < 90:
        substractorForNonUtama = 38
    elif lowestFromYangUtama < 100:
        substractorForNonUtama = 47
    else:
        substractorForNonUtama = 50

    highestAllowedFromNonUtama = lowestFromYangUtama - substractorForNonUtama

    if dictNonUtama:
        highestFromNonUtama = max(dictNonUtama.values())
        divisorForNonUtama = highestAllowedFromNonUtama / highestFromNonUtama
        dictNonUtama = {k: v * divisorForNonUtama for k, v in dictNonUtama.items()}

    dictMerge = {**dictYangUtama, **dictNonUtama}

    while len(dictMerge) < 6:
        keysToCheck = ["social", "enterprising", "investigative", "artistic", "conventional", "realistic"]
        for keyToCheck in keysToCheck:
            if keyToCheck not in dictMerge:
                dictMerge[keyToCheck] = randomValueNonUtama * min(dictMerge.values())
            if len(dictMerge) >= 6:
                break

    dictMergeList = sorted(dictMerge.items(), key=lambda item: item[1], reverse=True)

    rankAndScoreRiasec = {
        dictMergeList[i][0]: int(round(dictMergeList[i][1])) for i in range(6)
    }

    return rankAndScoreRiasec

def generate_rank_and_skoring_belbinteam(kombinasiYangUtamaInfo, kombinasiNonUtamaInfo):
    listYangUtama = kombinasiYangUtamaInfo["idenBelbinUtama"]
    skorYangUtama = kombinasiYangUtamaInfo["skorBelbinUtama"]

    listNonUtamaOri = kombinasiNonUtamaInfo["idenBelbinNonUtama"]
    skorNonUtamaOri = kombinasiNonUtamaInfo["skorBelbinNonUtama"]
    randomValueNonUtama = float(kombinasiNonUtamaInfo["randomNonUtama"])
    if randomValueNonUtama < 0.5:
        randomValueNonUtama += 0.5

    listYangUtamaArray = listYangUtama.split('_')
    skorYangUtamaArray = skorYangUtama.split('_')

    listNonUtamaOriArray = listNonUtamaOri.split('_')
    skorNonUtamaOriArray = skorNonUtamaOri.split('_')

    dictYangUtama = {listYangUtamaArray[i]: float(skorYangUtamaArray[i]) for i in range(len(listYangUtamaArray))}
    dictNonUtamaOri = {listNonUtamaOriArray[i]: float(skorNonUtamaOriArray[i]) for i in range(len(listNonUtamaOriArray))}

    dictNonUtama = {k: v for k, v in dictNonUtamaOri.items() if k not in dictYangUtama and k != "none"}

    lowestFromYangUtama = min(v for v in dictYangUtama.values() if v > 0)

    if lowestFromYangUtama < 5:
        substractorForNonUtama = 1
    elif lowestFromYangUtama < 10:
        substractorForNonUtama = 2
    elif lowestFromYangUtama < 20:
        substractorForNonUtama = 3
    elif lowestFromYangUtama < 30:
        substractorForNonUtama = 5
    elif lowestFromYangUtama < 40:
        substractorForNonUtama = 8
    elif lowestFromYangUtama < 50:
        substractorForNonUtama = 12
    elif lowestFromYangUtama < 60:
        substractorForNonUtama = 17
    elif lowestFromYangUtama < 70:
        substractorForNonUtama = 23
    elif lowestFromYangUtama < 80:
        substractorForNonUtama = 30
    elif lowestFromYangUtama < 90:
        substractorForNonUtama = 38
    elif lowestFromYangUtama < 100:
        substractorForNonUtama = 47
    else:
        substractorForNonUtama = 50

    highestAllowedFromNonUtama = lowestFromYangUtama - substractorForNonUtama

    if dictNonUtama:
        highestFromNonUtama = max(dictNonUtama.values())
        divisorForNonUtama = highestAllowedFromNonUtama / highestFromNonUtama
        dictNonUtama = {k: v * divisorForNonUtama for k, v in dictNonUtama.items()}

    dictMerge = {**dictYangUtama, **dictNonUtama}

    while len(dictMerge) < 9:
        keysToCheck = ["teamworker", "implementer", "completerfinisher", "resourceinvestigator", "monitorevaluator", "specialist", "plant", "shaper", "coordinator"]
        for keyToCheck in keysToCheck:
            if keyToCheck not in dictMerge:
                randomValue = randomValueNonUtama * min(dictMerge.values())
                dictMerge[keyToCheck] = randomValue
            if len(dictMerge) >= 9:
                break

    dictMergeList = list(dictMerge.items())

    dictRankScoreBelbinTeam = {dictMergeList[i][0]: int(round(dictMergeList[i][1])) for i in range(9)}

    return dictRankScoreBelbinTeam



def identifikasi_sports_talent(fingertypename_values):
    bN_values = {
        "ARC": [12.5, 7.5, 15, 7.5, 7.5], "TEA": [12.5, 7.5, 15, 7.5, 7.5], "ARL": [12.1875, 7.3125, 14.625, 7.3125, 7.3125],
        "ARW": [11.875, 7.125, 14.25, 7.125, 7.125], "LOO": [9.375, 5.625, 11.25, 5.625, 5.625], "RAD": [9.375, 5.625, 11.25, 5.625, 5.625],
        "DOB": [8.125, 4.875, 9.75, 4.875, 4.875], "WHO": [6.875, 4.125, 8.25, 4.125, 4.125], "TAR": [6.875, 4.125, 8.25, 4.125, 4.125],
        "PEA": [7.5, 4.125, 8.25, 4.125, 4.125], "SHE": [6.875, 4.125, 8.25, 4.125, 4.125]
    }

    bE_values = {key: [value * 0.8 for value in values] for key, values in bN_values.items()}
    b_Sport_values = {key: [value * 1.2 for value in values] for key, values in bN_values.items()}

    skorStren = skorSpeed = skorEndu = skorCoord = 0.0
    cyclicPreference = 0.0

    fingerprintCounts = count_spesific_fingerprint_type_occurrence(fingertypename_values)

    jumlahTotal_LOOP = fingerprintCounts["loop"] + fingerprintCounts["radial"]
    jumlahTotal_WHORLS = fingerprintCounts["whorl"] + fingerprintCounts["double"]

    for i, jari in enumerate(fingertypename_values):
        for k in bN_values.keys():
            if jari == k.lower():
                skorStren += bN_values[k][i % 5]
                skorSpeed += bE_values[k][i % 5]
                skorCoord += b_Sport_values[k][i % 5]

    if jumlahTotal_WHORLS == jumlahTotal_LOOP:
        skorEndu = 80.0
    elif jumlahTotal_WHORLS > jumlahTotal_LOOP:
        skorEndu = 80.0 - (min((jumlahTotal_WHORLS - jumlahTotal_LOOP) * 7 + 2, 67.0))
    else:
        skorEndu = 80.0 - (min((jumlahTotal_LOOP - jumlahTotal_WHORLS) * 7 + 2, 67.0))

    if fingertypename_values[0] == "whorl" or fingertypename_values[0] == "peacock":
        skorEndu += 10.0
    if fingertypename_values[2] == "whorl" or fingertypename_values[2] == "peacock":
        skorEndu += 5.0
    if fingertypename_values[7] == "whorl" or fingertypename_values[7] == "peacock":
        skorEndu += 5.0


    # skorArraySportsTraits = IdentifikasiSportsTalent(dataKlien)
    # skorStrength = int(skorArraySportsTraits[0])
    # skorSpeed = int(skorArraySportsTraits[1])
    # skorEndurance = int(skorArraySportsTraits[2])
    # skorCoordination = int(skorArraySportsTraits[3])

    return [skorStren, skorSpeed, skorEndu, skorCoord]

def fingertype_processing(kombinasi_jari_yang_utama, kombinasi_jari_non_utama, fingertypename_values):
    kombinasi_yang_utama = retrieve_kombinasi_yang_utama(kombinasi_jari_yang_utama)
    kombinasi_non_utama = retrieve_kombinasi_non_utama(kombinasi_jari_non_utama)

    if not kombinasi_yang_utama or not kombinasi_non_utama:
        return None

    # SANSKRIT PERSONALITY
    rank_and_score_sanskerta = generate_rank_and_skoring_sanskerta(kombinasi_yang_utama, kombinasi_non_utama, fingertypename_values)

    nameSanskertaRank1 = list(rank_and_score_sanskerta.keys())[0]
    nameSanskertaRank2 = list(rank_and_score_sanskerta.keys())[1]
    nameSanskertaRank3 = list(rank_and_score_sanskerta.keys())[2]
    nameSanskertaRank4 = list(rank_and_score_sanskerta.keys())[3]

    skorSanskertaRank1 = list(rank_and_score_sanskerta.values())[0]
    skorSanskertaRank2 = list(rank_and_score_sanskerta.values())[1]
    skorSanskertaRank3 = list(rank_and_score_sanskerta.values())[2]
    skorSanskertaRank4 = list(rank_and_score_sanskerta.values())[3]

    skorMahitala = rank_and_score_sanskerta.get("mahitala", 0)
    skorWidigda = rank_and_score_sanskerta.get("widigda", 0)
    skorKatresnan = rank_and_score_sanskerta.get("katresnan", 0)
    skorWingwang = rank_and_score_sanskerta.get("wingwang", 0)

    dobSkorNeuroticismUtama = float(kombinasi_yang_utama["skorNeuroticism"])
    dobSkorNeuroticismNonUtama = float(kombinasi_non_utama["skorNeuroticismNonUtama"])
    dobSkorExtraversionUtama = float(kombinasi_yang_utama["skorExtraversion"])
    dobSkorExtraversionNonUtama = float(kombinasi_non_utama["skorExtraversionNonUtama"])
    totalNeuroticism = int(dobSkorNeuroticismUtama + dobSkorNeuroticismNonUtama)
    totalExtraversion = int(dobSkorExtraversionUtama + dobSkorExtraversionNonUtama)

    dobSkorInstinctUtama = float(kombinasi_yang_utama["skorInstinct"])
    dobSkorFeelingUtama = float(kombinasi_yang_utama["skorFeeling"])
    dobSkorThinkingUtama = float(kombinasi_yang_utama["skorThinking"])
    dobSkorInstinctNonUtama = float(kombinasi_non_utama["skorInstinctNonUtama"])
    dobSkorFeelingNonUtama = float(kombinasi_non_utama["skorFeelingNonUtama"])
    dobSkorThinkingNonUtama = float(kombinasi_non_utama["skorThinkingNonUtama"])
    bobotUtama = 0.7
    bobotNonUtama = 0.3
    totalInstinct = int((dobSkorInstinctUtama * bobotUtama) + (dobSkorInstinctNonUtama * bobotNonUtama))
    totalFeeling = int((dobSkorFeelingUtama * bobotUtama) + (dobSkorFeelingNonUtama * bobotNonUtama))
    totalThinking = int((dobSkorThinkingUtama * bobotUtama) + (dobSkorThinkingNonUtama * bobotNonUtama))

    skorSubyektifObyektif = int(float(kombinasi_yang_utama["skorSubyektifObyektif"]))
    skorPertimbanganSpontan = int(float(kombinasi_yang_utama["skorPertimbanganSpontan"]))

    rank_and_score_riasec = generate_rank_and_skoring_hollandcodes(kombinasi_yang_utama, kombinasi_non_utama)

    nameRiasecRank1 = list(rank_and_score_riasec.keys())[0]
    nameRiasecRank2 = list(rank_and_score_riasec.keys())[1]
    nameRiasecRank3 = list(rank_and_score_riasec.keys())[2]
    nameRiasecRank4 = list(rank_and_score_riasec.keys())[3]
    nameRiasecRank5 = list(rank_and_score_riasec.keys())[4]
    nameRiasecRank6 = list(rank_and_score_riasec.keys())[5]

    skorRiasecRank1 = list(rank_and_score_riasec.values())[0]
    skorRiasecRank2 = list(rank_and_score_riasec.values())[1]
    skorRiasecRank3 = list(rank_and_score_riasec.values())[2]
    skorRiasecRank4 = list(rank_and_score_riasec.values())[3]
    skorRiasecRank5 = list(rank_and_score_riasec.values())[4]
    skorRiasecRank6 = list(rank_and_score_riasec.values())[5]

    kombinasi3Riasec = f"{nameRiasecRank1}-{nameRiasecRank2}-{nameRiasecRank3}"

    skorRealistic = rank_and_score_riasec.get("realistic", 0)
    skorInvestigative = rank_and_score_riasec.get("investigative", 0)
    skorArtistic = rank_and_score_riasec.get("artistic", 0)
    skorSocial = rank_and_score_riasec.get("social", 0)
    skorEnterprising = rank_and_score_riasec.get("enterprising", 0)
    skorConventional = rank_and_score_riasec.get("conventional", 0)

    rank_and_score_belbin = generate_rank_and_skoring_belbinteam(kombinasi_yang_utama, kombinasi_non_utama)

    nameBelbinRank1 = list(rank_and_score_belbin.keys())[0]
    nameBelbinRank2 = list(rank_and_score_belbin.keys())[1]
    nameBelbinRank3 = list(rank_and_score_belbin.keys())[2]
    nameBelbinRank4 = list(rank_and_score_belbin.keys())[3]
    nameBelbinRank5 = list(rank_and_score_belbin.keys())[4]
    nameBelbinRank6 = list(rank_and_score_belbin.keys())[5]
    nameBelbinRank7 = list(rank_and_score_belbin.keys())[6]
    nameBelbinRank8 = list(rank_and_score_belbin.keys())[7]
    nameBelbinRank9 = list(rank_and_score_belbin.keys())[8]

    skorBelbinRank1 = list(rank_and_score_belbin.values())[0]
    skorBelbinRank2 = list(rank_and_score_belbin.values())[1]
    skorBelbinRank3 = list(rank_and_score_belbin.values())[2]
    skorBelbinRank4 = list(rank_and_score_belbin.values())[3]
    skorBelbinRank5 = list(rank_and_score_belbin.values())[4]
    skorBelbinRank6 = list(rank_and_score_belbin.values())[5]
    skorBelbinRank7 = list(rank_and_score_belbin.values())[6]
    skorBelbinRank8 = list(rank_and_score_belbin.values())[7]
    skorBelbinRank9 = list(rank_and_score_belbin.values())[8]

    skorShaper = rank_and_score_belbin.get("shaper", 0)
    skorImplementer = rank_and_score_belbin.get("implementer", 0)
    skorCompleterfinisher = rank_and_score_belbin.get("completerfinisher", 0)
    skorCoordinator = rank_and_score_belbin.get("coordinator", 0)
    skorTeamworker = rank_and_score_belbin.get("teamworker", 0)
    skorResourceinvestigator = rank_and_score_belbin.get("resourceinvestigator", 0)
    skorMonitorevaluator = rank_and_score_belbin.get("monitorevaluator", 0)
    skorPlant = rank_and_score_belbin.get("plant", 0)
    skorSpecialist = rank_and_score_belbin.get("specialist", 0)

    listYangUtama = kombinasi_yang_utama["idenTraitSportsUtama"]
    listNonUtamaOri = kombinasi_non_utama["idenTraitSportsNonUtama"]
    listYangUtamaArray = listYangUtama.split('_')
    listNonUtamaOriArray = listNonUtamaOri.split('_')
    duplicates = set()

    for item in listNonUtamaOriArray:
        if item in listYangUtamaArray:
            duplicates.add(item)

    combinedList = listYangUtamaArray + [item for item in listNonUtamaOriArray if item != "none" and item not in duplicates]
    listSportsPersonality = combinedList

    sportsPersonalityRank1 = listSportsPersonality[0] if len(listSportsPersonality) > 0 else ""
    sportsPersonalityRank2 = listSportsPersonality[1] if len(listSportsPersonality) > 1 else ""
    sportsPersonalityRank3 = listSportsPersonality[2] if len(listSportsPersonality) > 2 else ""
    sportsPersonalityRank4 = listSportsPersonality[3] if len(listSportsPersonality) > 3 else ""
    sportsPersonalityRank5 = listSportsPersonality[4] if len(listSportsPersonality) > 4 else ""
    sportsPersonalityRank6 = listSportsPersonality[5] if len(listSportsPersonality) > 5 else ""
    sportsPersonalityRank7 = listSportsPersonality[6] if len(listSportsPersonality) > 6 else ""
    sportsPersonalityRank8 = listSportsPersonality[7] if len(listSportsPersonality) > 7 else ""

    peranSports = kombinasi_yang_utama["peranSports"]
    tipeCyclic = kombinasi_yang_utama["tipeCyclic"]
    skorCyclic = int(float(kombinasi_yang_utama["skorCyclic"]))

    

    kalkulasi_pola = {
        "KombinasiJariUtama": kombinasi_jari_yang_utama,
        "KombinasiJariNonUtama": kombinasi_jari_non_utama,
        "TabiatMotivasi": kombinasi_yang_utama["tabiatMotivasi"],
        "GayaBerkembang": kombinasi_yang_utama["gayaBerkembang"],
        "GayaBelajar": kombinasi_yang_utama["gayaBelajar"],
        "TipikalPertemanan": kombinasi_yang_utama["tipikalPertemanan"],
        "TipikalMedsos": kombinasi_yang_utama["tipikalMedsos"],
        "TipikalPecahMasalah": kombinasi_yang_utama["tipikalPecahMasalah"],
        "TipikalStres": kombinasi_yang_utama["tipikalStres"],
        "TipikalPersonPebisnis": kombinasi_yang_utama["tipikalPersonPebisnis"],
        "TipikalStrategiBisnis": kombinasi_yang_utama["tipikalStrategiBisnis"],
        "TipikalDevelopBisnis": kombinasi_yang_utama["tipikalDevelopBisnis"],
        "TipikalMengajar": kombinasi_yang_utama["tipikalMengajar"],
        "TotalNeuroticism": totalNeuroticism,
        "TotalExtraversion": totalExtraversion,
        "TotalInstinct": totalInstinct,
        "TotalFeeling": totalFeeling,
        "TotalThinking": totalThinking,
        "SkorSubyektifObyektif": skorSubyektifObyektif,
        "SkorPertimbanganSpontan": skorPertimbanganSpontan,
        "nameSanskertaRank1": nameSanskertaRank1,
        "skorSanskertaRank1": skorSanskertaRank1,
        "nameSanskertaRank2": nameSanskertaRank2,
        "skorSanskertaRank2": skorSanskertaRank2,
        "nameSanskertaRank3": nameSanskertaRank3,
        "skorSanskertaRank3": skorSanskertaRank3,
        "nameSanskertaRank4": nameSanskertaRank4,
        "skorSanskertaRank4": skorSanskertaRank4,
        "SkorMahitala": skorMahitala,
        "SkorWidigda": skorWidigda,
        "SkorKatresnan": skorKatresnan,
        "SkorWingwang": skorWingwang,
        "nameRiasecRank1": nameRiasecRank1,
        "skorRiasecRank1": skorRiasecRank1,
        "nameRiasecRank2": nameRiasecRank2,
        "skorRiasecRank2": skorRiasecRank2,
        "nameRiasecRank3": nameRiasecRank3,
        "skorRiasecRank3": skorRiasecRank3,
        "nameRiasecRank4": nameRiasecRank4,
        "skorRiasecRank4": skorRiasecRank4,
        "nameRiasecRank5": nameRiasecRank5,
        "skorRiasecRank5": skorRiasecRank5,
        "nameRiasecRank6": nameRiasecRank6,
        "skorRiasecRank6": skorRiasecRank6,
        "kombinasi3Riasec": kombinasi3Riasec,
        "skorRealistic": skorRealistic,
        "skorInvestigative": skorInvestigative,
        "skorArtistic": skorArtistic,
        "skorSocial": skorSocial,
        "skorEnterprising": skorEnterprising,
        "skorConventional": skorConventional,
        "sportsPersonalityRank1": sportsPersonalityRank1,
        "sportsPersonalityRank2": sportsPersonalityRank2,
        "sportsPersonalityRank3": sportsPersonalityRank3,
        "sportsPersonalityRank4": sportsPersonalityRank4,
        "sportsPersonalityRank5": sportsPersonalityRank5,
        "sportsPersonalityRank6": sportsPersonalityRank6,
        "sportsPersonalityRank7": sportsPersonalityRank7,
        "sportsPersonalityRank8": sportsPersonalityRank8,
        "peranSports": peranSports,
        "tipeCyclic": tipeCyclic,
        "skorCyclic": skorCyclic,
    }

    return kalkulasi_pola
