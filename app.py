from nptdms import TdmsFile, TdmsWriter, RootObject, ChannelObject
import nptdms
import numpy as np
import pandas as pd
import sys
import os

if __name__ == "__main__":
    input_folder = sys.argv[1]
    output_file = sys.argv[2]
    print("== Welcome to this Amazing TDMS Merge Tool ==")
    print(f"Merging files in folder {input_folder}")
    print(f"Output file is {output_file}")

    dir_list = os.listdir(input_folder)
    dir_list.sort()

    dfs = []
    for f in dir_list:
        tdms = TdmsFile.read(f"{input_folder}/{f}")
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
