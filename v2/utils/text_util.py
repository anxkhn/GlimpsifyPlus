class TextUtil:
    @staticmethod
    def get_directory_and_video_name(input):
        input = input.split(" -> ")

        directory = input[0]
        directory = directory.split("/")[1]

        video_name = input[1]
        video_name = video_name.split("/")[-1]
        video_name = video_name.split(".")[0]

        return directory, video_name