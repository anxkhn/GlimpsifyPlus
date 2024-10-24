import os
import shutil

from directory_manager import DirectoryManager
from random_generator import RandomGenerator

def get_named_pdfs(input, new_directory):
    print(input)
    input = input.split(" -> ")
    print(input)

    directory = input[0]
    directory = directory.split("/")[1]
    print(directory)

    video_name = input[1]
    video_name = video_name.split("/")[-1]
    video_name = video_name.split(".")[0]
    print(video_name)

    pdf_path = f"data/{directory}.pdf"



    output_path = f"{new_directory}/{video_name}.pdf"

    shutil.copy(pdf_path, output_path)



if __name__ == "__main__":
    new_directory = RandomGenerator.generate_random_word(3)
    new_directory = f"scripts/data/{new_directory}"
    DirectoryManager.create_directory(new_directory)

    inputs = []
    with open("scripts/data/results.txt", "r") as file:
        inputs = file.readlines()

    print(inputs)
    
    for input in inputs:
        try:
            get_named_pdfs(input, new_directory)
        except Exception as e:
            print(input)
            print(e)