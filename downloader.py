import requests
import os

"""
File name range settings
"""
begin_from = 0
end_at = 1

"""
Download URL settings
"""
base_url = "https://vip.lz-cdn3.com/20220917/13686_3a348bc0/1000k/hls/579503717ad"
counter_prefix = 6
extension = ".ts"

"""
Save to WHICH dir?
"""
save_to_dir = "E20"

# ==============================================================================

def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


def generate_file_list(destination_path):
    """
    Generate file list for ffmpegs' concatenate process

    Args:
        destination_path (str): e.g. "/User/trump/Documents/GimyDownloader/E08"
    """
    path_filelist = '{}/{}'.format(destination_path, 'filelist.txt')
    
    # Create file if not exists
    if os.path.isfile(path_filelist) == False:
        with open(path_filelist , 'w') as ff:
            pass

    all_content = ''
    for count in range(begin_from, end_at + 1):
        file_count = str(count).zfill(counter_prefix)
        all_content = all_content +  "file '{}.ts'\n".format(file_count)
        with open(path_filelist , 'w') as ff:
            ff.write(all_content)

    notify("GimyDownloader", "filelist.txt generated!")


def start_download(destination_path):
    """
    Download some shits

    Args:
        destination_path (str): e.g. "/User/trump/Documents/GimyDownloader/E08"
    """
    retry_list = []
    for count in range(begin_from, end_at + 1):
        file_count = str(count).zfill(counter_prefix)
        url = base_url + file_count + extension

        print("[I] Downloading {} from \n{}".format(file_count, url))

        try:
            ts_file = requests.get(url, timeout = (10, 10))
            file_save_location = "{}/{}{}".format(destination_path, file_count, extension)
            open(file_save_location , 'wb').write(ts_file.content)
        except:
            # TODO: Auto retry
            retry_list.append(url)
    
    if len(retry_list) != 0:
        print('[E] Download failed list\n{}'.format(retry_list))

    notify("GimyDownloader", "Download finished!")


if __name__ == '__main__':
    cwd = os.getcwd()

    # Make destination dir
    destination_path = "{}/{}".format(cwd, save_to_dir)
    if os.path.isdir(destination_path) == False:
        os.makedirs(destination_path)

    # Make file list
    generate_file_list(destination_path)

    # Download
    start_download(destination_path)
