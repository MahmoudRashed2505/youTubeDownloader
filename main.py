import os
from pytube import YouTube
import googleapiclient.discovery
from urllib.parse import  parse_qs, urlparse


#main Function that the program will start from
def main():

    #trying to move to the app's download folder and if it is not there
    #we will create it
    try:
        os.chdir('C:\\Users\\{YOUR_USERNAME}\\Videos\\ytDownloader')
    except:
        os.chdir('C:\\Users\\{YOUR_USERNAME}\\Videos')
        os.mkdir('ytDownloader')
        os.chdir('C:\\Users\\{YOUR_USERNAME}\\Videos\\ytDownloader')

    #clearing the console and taking the Video/Playlist URL from the user
    os.system('cls')
    url = input("Please Enter the URL: ")

    #Check if the link is playlist or a single video by passing the URL to
    #checkLink Function and the download process will continue from there
    checkLink(url)

    #After the Download process ends we will ask the user if he want download
    #anything else
    choice = input("Do you want to Download anything else [y/n]: ")
    if choice == 'y' or choice == 'Y': main()
    else:
        os.system('cls')
        exit()


#CheckLink Function that is responsible for checking the url if it is a single
#video or a playlist and redirct the process according to that
def checkLink(url):
    if url.find('playlist') != -1:
        download_playlist(url)
    else:
        download_video(url)

#download_playlist function that is responsible for downloading playlists
def download_playlist(url):
    playlistName = input("Please Enter the playlist Name: ")
    os.mkdir(playlistName)
    os.chdir("C:\\Users\\MahmoudHossamEldenIb\\Videos\\ytDownloader\\"+playlistName)
    query = parse_qs(urlparse(url).query, keep_blank_values=True)
    playlist_id = query["list"][0]
    print('get all playlist items links from {}'.format(playlist_id))
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = "AIzaSyDll68Dzb-TliDCtFswncilmcMAhmaxoZA")
    request = youtube.playlistItems().list(
        part = "snippet",
        playlistId = playlist_id,
        maxResults = 50
        )
    response = request.execute()
    playlist_items = []
    while request is not None:
        response = request.execute()
        playlist_items += response["items"]
        request = youtube.playlistItems().list_next(request, response)

    print("total videos: {}".format(len(playlist_items)))
    playlist_urls = list()
    for t in playlist_items:
        playlist_urls.append(f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&t=0s')
    VideoQualities = list()
    VidQuality = None
    vidStreams = YouTube(playlist_urls[0]).streams.filter(progressive="True",type='video')
    for stream in vidStreams:
        quaility = str(stream)
        quaility = quaility[quaility.find('res=')+5:quaility.find('res=')+10].strip()
        quaility.strip('""')
        VideoQualities.append(quaility)
    print("\n\nChoose the Quality:\n")
    counter = 1
    for i in VideoQualities:
        print("{}-) {}".format(counter,i.strip('""')))
        counter +=1
    choice = int(input("\nYour Choice: "))
    VidQuality = VideoQualities[choice-1]
    print()
    counter = 0
    for video in playlist_urls:
        streams = YouTube(playlist_urls[counter]).streams.filter(progressive="True")
        for stream in streams:
            if VidQuality in str(stream):
                print("Downloading {}".format(str(YouTube(video).title)))
                stream.download()
                counter+=1
                print("Done\n")
                break
    print("\n\n~~~ Playlist Downloaded Successfully ~~~\n\n")
    os.chdir('..')
    os.system('pause')
    os.system('cls')


#download_video The function that is responsible for downloading a single video
def download_video(url):
    ytd = YouTube(url)
    streams = ytd.streams.filter(progressive='True')
    counter = 1
    for stream in streams:
        st = str(stream)
        print("{}-) {}".format(counter,st[st.find('res=')+5:st.find('res=')+9]))
        counter +=1
    choice = int(input("Choose the quaility: "))
    counter =1
    for stream in streams:
        if counter == choice:
            stream.download()
            print("DONE")
            break
        counter+=1


main()
