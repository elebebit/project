import base64 
from icrawler import ImageDownloader
from icrawler.builtin import GoogleImageCrawler
from six.moves.urllib.parse import urlparse

search='炸鸡'# name of search

class PrefixNameDownloader(ImageDownloader):

    def get_filename(self, task, default_ext):
        filename = super(PrefixNameDownloader, self).get_filename(
            task, default_ext)
        return search+'_'+ filename


class Base64NameDownloader(ImageDownloader):

    def get_filename(self, task, default_ext):
        url_path = urlparse(task['file_url'])[2]
        if '.' in url_path:
            extension = url_path.split('.')[-1]
            if extension.lower() not in ['jpg', 'jpeg', 'png', 'bmp', 'tiff', 'gif', 'ppm', 'pgm']:
                extension = default_ext        
        else:
            extension = default_ext        
        # works for python 3
        filename = base64.b64encode(url_path.encode()).decode()
        return '{}.{}'.format(filename, extension)



google_crawler = GoogleImageCrawler(downloader_cls=PrefixNameDownloader,
                                   # downloader_cls=Base64NameDownloader,
                                    downloader_threads=4,
                                    storage={'root_dir': 'images/'+search})

google_crawler.crawl(search, max_num=50)
