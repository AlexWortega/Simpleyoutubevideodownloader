from importlib.util import find_spec as find_lib
from os.path import expandvars as os_vars
from urllib.request import urlopen
from PIL import Image, ImageTk
import tkinter.filedialog
import tkinter
import pafy
import pip
import io

ret_values = {};
# чтобы все работало скачайте либы : PILLOW  pafy youtube-dl
# pip install pafy
# pip install pillow
# pip install youtube-dl
def getThumbnailURL(url):
    counter = 0;
    pos = 0;

    for char in url:
        if char == '?':
            counter = 1;
        if char == 'v':
            if counter == 1:
                counter = 2;
                break;
        pos += 1;

    video_id = url[pos + 2:];

    return "http://img.youtube.com/vi/%s/0.jpg" % video_id;


def downloadVideo():
    choice = DVVar.get();

    if choice == '':
        return;

    counter = 0;
    for i in ret_values['videostreams']:
        if str(i.resolution) + ', ' + i.extension == choice:
            break;
        counter += 1;

    if counter >= len(ret_values['videostreams']):
        return;
#выгружаем видео
    ret_values['videostreams'][counter].download(quiet=True, filepath=video_dir.get());


def downloadAudio():
    choice = DAVar.get();
#аудио парсер
    if choice == '':
        return;

    counter = 0;
    for i in ret_values['audiostreams']:
        if str(i.bitrate) + ', ' + i.extension == choice:
            break;
        counter += 1;

    if counter >= len(ret_values['audiostreams']):
        return;

    ret_values['audiostreams'][counter].download(quiet=True, filepath=audio_dir.get());


def getVideoDir():
    # DirDialog window options
    options = {};
    # options['initialdir'] = 'C:\\'; # это в корень не трогать блять
    options['mustexist'] = False;
    options['title'] = 'Download folder';
#куды качать

    dir_path = tkinter.filedialog.askdirectory(**options);
    video_dir.config(state='normal');
    video_dir.delete(0, 'end');
    video_dir.insert(0, dir_path);
    video_dir.config(state='disabled');


def getAudioDir():
    # DirDialog window options
    options = {};
    # options['initialdir'] = 'C:\\'; # аудио в корень
    options['mustexist'] = False;
    options['title'] = 'Download folder';

    # Get the source dir path
    dir_path = tkinter.filedialog.askdirectory(**options);
    audio_dir.config(state='normal');
    audio_dir.delete(0, 'end');
    audio_dir.insert(0, dir_path);
    audio_dir.config(state='disabled');


def get(a, b, c):
    url = url_entry.get();
    tnURL = getThumbnailURL(url);
    #парсим красоту для ui

    image_bytes = urlopen(tnURL).read();
    im = Image.open(io.BytesIO(image_bytes));
    tk_image = ImageTk.PhotoImage(im.resize((140, 110), Image.ANTIALIAS));
    ret_values['photoholder'].configure(image=tk_image, width="140", height="110");
    ret_values['photoholder'].image = tk_image;

    if url == '':
        return

    video = pafy.new(url);

    attr = {};

    attr['title'] = video.title;
    attr['rating'] = video.rating;
    attr['viewcount'] = video.viewcount;
    attr['author'] = video.author;
    attr['length'] = video.length;
    attr['duration'] = video.duration;
    attr['likes'] = video.likes;
    attr['dislikes'] = video.dislikes;

    titlelbl.config(text="Title: " + attr['title']);
    authorlbl.config(text="Author: " + attr['author']);
    durationlbl.config(text="Duration: " + attr['duration']);
    viewcountlbl.config(text="Views: " + str(attr['viewcount']));
    likeslbl.config(text="Likes: " + str(attr['likes']));
    dislikeslbl.config(text="Dislikes: " + str(attr['dislikes']));


    videoStreams = video.streams;
    audioStreams = video.audiostreams;


    DVList = [str(i.resolution) + ', ' + i.extension for i in videoStreams];
    DAList = [str(i.bitrate) + ', ' + i.extension for i in audioStreams];

    DVDrop['menu'].delete(0, 'end');
    DVDrop['menu'].delete(0, 'end');

    DVVar.set('');
    DAVar.set('');

    for i in DVList:
        DVDrop['menu'].add_command(label=i, command=tkinter._setit(DVVar, i));

    for i in DAList:
        DADrop['menu'].add_command(label=i, command=tkinter._setit(DAVar, i));

    DVVar.set(DVList[0]);
    DAVar.set(DAList[0]);

    ret_values['videostreams'] = videoStreams;
    ret_values['audiostreams'] = audioStreams;
    ret_values['video'] = video;


if __name__ == '__main__':
    master = tkinter.Tk();
    master.title("YouTube Downloader");
    master.minsize(width="800", height="270");
    master.resizable(width=False, height=False);
    master.geometry('800x270');
    master.geometry('800x270+0+0');

    ret_values['master'] = master;

    tkinter.Label(master, text="Url").place(x=20, y=20);

    url_var = tkinter.StringVar();
    url_var.trace('w', get);
    url_entry = tkinter.Entry(master, textvariable=url_var, width=120);
    url_entry.place(x=50, y=20);

    titlelbl = tkinter.Label(master, text="Title: ");
    titlelbl.place(x=180, y=58);

    authorlbl = tkinter.Label(master, text="Author: ");
    authorlbl.place(x=180, y=78);

    durationlbl = tkinter.Label(master, text="Duration: ");
    durationlbl.place(x=180, y=98);

    viewcountlbl = tkinter.Label(master, text="Views: ");
    viewcountlbl.place(x=180, y=118);

    likeslbl = tkinter.Label(master, text="Likes: ");
    likeslbl.place(x=180, y=138);

    dislikeslbl = tkinter.Label(master, text="Dislikes: ");
    dislikeslbl.place(x=180, y=158);

    DVList = [''];
    DAList = [''];

    DVVar = tkinter.StringVar(master);
    DVVar.set('Quality');
    DAVar = tkinter.StringVar(master);
    DAVar.set('Quality');

    DVDrop = tkinter.OptionMenu(master, DVVar, *DVList);
    DVDrop.configure(width="12");
    DVDrop.place(x=135, y=192);

    DADrop = tkinter.OptionMenu(master, DAVar, *DAList);
    DADrop.configure(width="12");
    DADrop.place(x=135, y=222);

    tkinter.Button(master, text="Download Video", command=downloadVideo, width=15, height=1).place(x=20, y=195);
    tkinter.Button(master, text="Download Audio", command=downloadAudio, width=15, height=1).place(x=20, y=225);

    video_dir = tkinter.Entry(master, width=80);
    video_dir.insert(0, os_vars("%userprofile%") + '\\Downloads\\');
    video_dir.config(state='disabled');
    video_dir.place(x=260, y=197);

    audio_dir = tkinter.Entry(master, width=80);
    audio_dir.insert(0, os_vars("%userprofile%") + '\\Downloads\\');
    audio_dir.config(state='disabled');
    audio_dir.place(x=260, y=227);

    tkinter.Button(master, text="...", command=getVideoDir, width=4, height=1).place(x=755, y=195);
    tkinter.Button(master, text="...", command=getAudioDir, width=4, height=1).place(x=755, y=225);

    im = ImageTk.PhotoImage(Image.frombytes('L', (140, 110), str.encode(''.join(['\x00' for i in range(140 * 110)]))));
    photoHolder = tkinter.Label(master, image=im, bg='white', width="140", height="110");
    photoHolder.place(x=20, y=60);

    ret_values['photoholder'] = photoHolder;

    master.mainloop();
