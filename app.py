from nptdms import TdmsFile, TdmsWriter, RootObject, ChannelObject
import nptdms
import numpy as np
import pandas as pd
import sys
import os

if __name__ == "__main__":
    input_folder = os.path.abspath(sys.argv[1])
    output_file = sys.argv[2]
    print("== Welcome to this Amazing TDMS Merge Tool ==")
    print(f"Merging files in folder {input_folder}")
    print(f"Output file is {output_file}")

    dir_list = os.listdir(input_folder)
    files = sorted(dir_list, key=lambda f: os.path.getmtime(os.path.join(input_folder, f)))

    dfs = []
    for f in files:
        tdms = TdmsFile.read(os.path.join(input_folder, f))
        dfs.append(tdms.as_dataframe())

    df = pd.concat(dfs)

    with TdmsWriter(output_file) as tdms_writer:
        channels = []
        for column in df.columns:
            _, group, channel_name = column.split("/")
            channel_name = channel_name.replace("'","")
            group = group.replace("'", "")
            data = df[column]
            channels.append(ChannelObject(group, channel_name, data.tolist()))

        tdms_writer.write_segment(channels)

    print("== All done ==")
