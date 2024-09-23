ns = """mjxghg_peak_frames: /media/vedant/New Volume/DPythonProjects/yt_summarizer/data/mjxghg/Stream Cipher vs Block Cipher.mp4
hzwvxl_peak_frames: /media/vedant/New Volume/DPythonProjects/yt_summarizer/data/hzwvxl/Feistel Cipher Structure.mp4
wcilcz_peak_frames: /media/vedant/New Volume/DPythonProjects/yt_summarizer/data/wcilcz/Introduction to Data Encryption Standard (DES).mp4
kyyanr_peak_frames: /media/vedant/New Volume/DPythonProjects/yt_summarizer/data/kyyanr/Single Round of DES Algorithm.mp4
ofyopr_peak_frames: /media/vedant/New Volume/DPythonProjects/yt_summarizer/data/ofyopr/The F Function of DES (Mangler Function).mp4
onefti_peak_frames: /media/vedant/New Volume/DPythonProjects/yt_summarizer/data/onefti/Key Scheduling and Decryption in DES.mp4
gmbjvd_peak_frames: /media/vedant/New Volume/DPythonProjects/yt_summarizer/data/gmbjvd/Avalanche Effect and the Strength of DES.mp4
eqeugq_peak_frames: /media/vedant/New Volume/DPythonProjects/yt_summarizer/data/eqeugq/Data Encryption Standard (DES) - Solved Questions.mp4
ulfpch_peak_frames: /media/vedant/New Volume/DPythonProjects/yt_summarizer/data/ulfpch/Introduction to Advanced Encryption Standard (AES).mp4
aknbma_peak_frames: /media/vedant/New Volume/DPythonProjects/yt_summarizer/data/aknbma/AES Encryption and Decryption.mp4
xieyvy_peak_frames: /media/vedant/New Volume/DPythonProjects/yt_summarizer/data/xieyvy/AES Round Transformation.mp4
okjesq_peak_frames: /media/vedant/New Volume/DPythonProjects/yt_summarizer/data/okjesq/AES Key Expansion.mp4
zovaan_peak_frames: /media/vedant/New Volume/DPythonProjects/yt_summarizer/data/zovaan/AES Security and Implementation Aspects.mp4
qoydqu_peak_frames: /media/vedant/New Volume/DPythonProjects/yt_summarizer/data/qoydqu/Multiple Encryption and Triple DES.mp4
fkqadb_peak_frames: /media/vedant/New Volume/DPythonProjects/yt_summarizer/data/fkqadb/Block Cipher Modes of Operation.mp4
csxxxo_peak_frames: /media/vedant/New Volume/DPythonProjects/yt_summarizer/data/csxxxo/Electronic Codebook (ECB).mp4
ylzhyx_peak_frames: /media/vedant/New Volume/DPythonProjects/yt_summarizer/data/ylzhyx/Cipher Block Chaining (CBC).mp4
yevuhu_peak_frames: /media/vedant/New Volume/DPythonProjects/yt_summarizer/data/yevuhu/Cipher Feedback (CFB).mp4
mhkajg_peak_frames: /media/vedant/New Volume/DPythonProjects/yt_summarizer/data/mhkajg/Output Feedback (OFB).mp4
yqnstp_peak_frames: /media/vedant/New Volume/DPythonProjects/yt_summarizer/data/yqnstp/Counter Mode (CTR).mp4
txmkgy_peak_frames: /media/vedant/New Volume/DPythonProjects/yt_summarizer/data/txmkgy/Block Cipher Modes of Operation (Solved Question).mp4"""

ns = """evxhrb_peak_frames: /media/vedant/New Volume/DPythonProjects/yt_summarizer/data/evxhrb/RSA Algorithm - How does it work - Ill PROVE it with an Example! -- Cryptography - Practical TLS.mp4
hoegot_peak_frames: /media/vedant/New Volume/DPythonProjects/yt_summarizer/data/hoegot/7 - Cryptography Basics - Diffie-Hellman Key Exchange.mp4"""

if __name__ == "__main__":
    ns = ns.split("\n")
    ns = [i.split(": ") for i in ns]
    ns = [x[1] for x in ns]

    import shutil
    import os
    for i in ns:
        print(i) 
        dir = i.split("/")
        name = dir[-1]
        dir = dir[:-1]
        dir = "/".join(dir) + "_profits" 
        destination = "/media/vedant/New Volume/DPythonProjects/yt_summarizer/new2/" + name
        
        shutil.copytree(dir, destination)
        # break

