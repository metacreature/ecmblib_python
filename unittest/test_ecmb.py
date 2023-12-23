import unittest, io, os
from PIL import Image

# only for relative import if you cloned the project
import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent.parent)

# you have to change this if ecmblib is installed as a module
from ecmblib.ecmb import ecmbBook, ecmbUtils, ecmbException, BOOK_TYPE, AUTHOR_TYPE, CONTENT_WARNING, BASED_ON_BOOK_TYPE, TARGET_SIDE

class testEcmb(unittest.TestCase):

    _test_filename = None
    _source_dir = None

    def setUp(self):
        self._test_filename = str(path.Path(__file__).abspath().parent) + '\\testfile.ecmb'
        self._source_dir = str(path.Path(__file__).abspath().parent) + '\\source_images\\'


    def test_metadata(self):
        result = self._metadata()
        if result != True:
            self.fail(result)

    def _metadata(self):
        try:
            book = ecmbBook(BOOK_TYPE.MANGA, 'en', 'bestmangapublisherinc_98a2cd52fea1168d', 900, 1200)

            # metadata
            book.metadata.set_isbn('0123456789')
            book.metadata.set_publisher('BestMangaPublisher Inc.')
            book.metadata.set_publisher('BestMangaPublisher Inc.', href='https://www.bestmangapublisher-inc.com')
            book.metadata.set_publishdate('2023')
            book.metadata.set_publishdate('2023-01-18')
            book.metadata.set_title('The Big Trip')
            book.metadata.set_volume(1)
            book.metadata.set_description('A stick figure goes on a big thrilling hiking-trip.')

            book.metadata.add_author('Clemens K.')
            book.metadata.add_author('Clemens K.', AUTHOR_TYPE.ILLUSTRATIONS)
            book.metadata.add_author('Clemens K.', 'Story')
            book.metadata.add_author('Clemens K.', AUTHOR_TYPE.COAUTHOR, href='https://github.com/metacreature')

            book.metadata.add_genre('Adventure')
            book.metadata.add_genre('Summer')

            warning_list = ecmbUtils.enum_values(CONTENT_WARNING)
            for warning in warning_list:
                book.metadata.add_content_warning(warning)

            # based on
            book.based_on.set_type(BASED_ON_BOOK_TYPE.LIGHTNOVEL)
            book.based_on.set_isbn('9876543210')
            book.based_on.set_publisher('BestNovelPublisher Inc.')
            book.based_on.set_publisher('BestNovelPublisher Inc.', href='https://www.bestnovelpublisher-inc.com')
            book.based_on.set_publishdate('1986')
            book.based_on.set_title('The Scary Hiking')

            book.based_on.add_author('Clemens K.')
            book.based_on.add_author('Clemens K.', AUTHOR_TYPE.ILLUSTRATIONS)
            book.based_on.add_author('Clemens K.', 'Story')
            book.based_on.add_author('Clemens K.', AUTHOR_TYPE.COAUTHOR, href='https://github.com/metacreature')

            # cover
            book.content.set_cover_front(self._source_dir + 'front.jpg')
            book.content.set_cover_rear(self._source_dir + 'rear.jpg')

            # write
            book.content.add_image(self._source_dir + 'img_1.jpg')
            book.write(self._test_filename, False)

            os.unlink(self._test_filename)

            return True
        except ecmbException as e:
            return str(e)
        

    def test_none(self):
        result = self._none()
        if result != True:
            self.fail(result)

    def _none(self):
        try:
            book = ecmbBook(BOOK_TYPE.COMIC, 'en', 'bestmangapublisherinc_98a2cd52fea1168d', 900, 1200)

            # metadata
            book.metadata.set_isbn(None)
            book.metadata.set_publisher(None)
            book.metadata.set_publisher(None, href=None)
            book.metadata.set_publishdate(None)
            book.metadata.set_title('The Big Trip')
            book.metadata.set_volume(None)
            book.metadata.set_description(None)

            # based on
            book.based_on.set_type(None)
            book.based_on.set_isbn(None)
            book.based_on.set_publisher(None)
            book.based_on.set_publisher(None, href=None)
            book.based_on.set_publishdate(None)
            book.based_on.set_title(None)

            # cover
            book.content.set_cover_front(None)
            book.content.set_cover_rear(None)

            # write
            book.content.add_image(self._source_dir + 'img_1.jpg')
            book.write(self._test_filename, False)

            os.unlink(self._test_filename)

            return True
        except ecmbException as e:
            return str(e)
        

    def test_empty(self):
        result = self._empty()
        if result != True:
            self.fail(result)

    def _empty(self):
        try:
            book = ecmbBook(BOOK_TYPE.COMIC, 'en', 'bestmangapublisherinc_98a2cd52fea1168d', 900, 1200)

            # metadata
            book.metadata.set_isbn('')
            book.metadata.set_publisher('')
            book.metadata.set_publisher('', href='')
            book.metadata.set_publishdate('')
            book.metadata.set_title('The Big Trip')
            book.metadata.set_description('')

            # based on
            book.based_on.set_type('')
            book.based_on.set_isbn('')
            book.based_on.set_publisher('')
            book.based_on.set_publisher('', href='')
            book.based_on.set_publishdate('')
            book.based_on.set_title('')

            # cover
            book.content.set_cover_front('')
            book.content.set_cover_rear('')

            # write
            book.content.add_image(self._source_dir + 'img_1.jpg')
            book.write(self._test_filename, False)
            
            os.unlink(self._test_filename)

            return True
        except ecmbException as e:
            return str(e)
        

    def test_content(self):
        result = self._content()
        if result != True:
            self.fail(result)

    def _content(self):
        try:
            book = ecmbBook(BOOK_TYPE.MANGA, 'en', 'bestmangapublisherinc_98a2cd52fea1168d', 900, 1200)
            book.metadata.set_title('The Big Trip')

            img_str = self._source_dir + 'img_1.jpg'
            img_str_full = self._source_dir + 'img_7.jpg'

            img_full = Image.open(img_str_full)
            img_left = img_full.crop((0, 0, 900, 1200))
            img_right = img_full.crop((900, 0, 1800, 1200))
            fp_full = io.BytesIO()
            fp_left = io.BytesIO()
            fp_right = io.BytesIO()      
            img_full.save(fp_full, 'webp', quality= 85)
            img_left.save(fp_left, 'webp', quality= 85)
            img_right.save(fp_right, 'webp', quality= 85)

            image1 = book.content.add_image(img_str)
            book.content.add_image(img_str, unique_id='img_1')
            image2 = book.content.add_image(fp_left)
            book.content.add_image(fp_left, unique_id='img_2')

            image3 = book.content.add_image(img_str_full, img_str, img_str)
            book.content.add_image(img_str_full, img_str, img_str, unique_id='img_3')
            image4 = book.content.add_image(fp_full, fp_left, fp_right)
            book.content.add_image(fp_full, fp_left, fp_right, unique_id='img_4')

            folder1 = book.content.add_folder()
            sub1 = folder1.add_folder()
            sub2 = sub1.add_folder()
            image5 = sub2.add_image(img_str)
            sub2.add_image(img_str, unique_id='img_5')

            folder2 = book.content.add_folder('dir_2')
            image6 = folder2.add_image(img_str)
            folder2.add_image(img_str, unique_id='img_6')

            folder3 = book.content.add_folder('dir_3')
            image7 = folder3.add_image(fp_full, fp_left, fp_right)
            folder3.add_image(fp_full, fp_left, fp_right, unique_id='img_7')


            nav1 = book.navigation.add_headline('aaaaaaaa')
            nav1.add_item('bbbbbbb', image1)
            nav1.add_item('cccccc', 'img_1')
            nav1.add_chapter('dddddd', folder1)
            nav1.add_chapter('eeeee', sub2, image5)
            nav1.add_chapter('fffff', 'dir_2', 'img_6')

            nav2 = book.navigation.add_headline('gggg', 'hhhhh')
            nav2.add_item('iiiiii', image1, title='jjjjj')
            nav2.add_item('kkkkkkk', 'img_1', title='llllllll')
            nav2.add_chapter('mmmmm', folder1, title='nnnnnnnn')
            nav2.add_chapter('ooooooo', sub2, image5, title='ppppp')
            nav2.add_chapter('qqqqq', 'dir_2', 'img_6', title='rrrrr')

            nav3 = book.navigation.add_chapter('sssss', folder1)
            nav4 = nav3.add_chapter('tttttt', sub1)

            nav5 = book.navigation.add_chapter('uuuuuu', folder3, image7, TARGET_SIDE.RIGHT)
            nav5.add_item('vvvvvv', image7, TARGET_SIDE.RIGHT)

            nav6 = book.navigation.add_chapter('uuuuuu', folder3, 'img_7', TARGET_SIDE.LEFT)
            nav6.add_item('vvvvvv', 'img_7', TARGET_SIDE.LEFT)

            nav7 = book.navigation.add_chapter('uuuuuu', folder3, 'img_7')
            nav7.add_item('vvvvvv', 'img_7')

            book.write(self._test_filename, False)
            
            os.unlink(self._test_filename)

            img_full.close()
            img_left.close()
            img_right.close()

            return True
        except ecmbException as e:
            return str(e)


if __name__ == '__main__':
    unittest.main()