# only for relative import if you cloned the project
# you have to delete this if ecmblib is installed as a module
import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(str(directory.parent.parent.parent) + '/src/')


from ecmblib import ecmbBook, BOOK_TYPE


print('\n', flush=True)


# create book-obj
###################################################

# book-type, language, unique-id, width of the images, height of the images
# all images have to have the width and height you've defined here. Of course except of double-pages which have double-width
# the minimun length of the unique_id is 16 - its recommended to use a md5-hash with a prefix of the publishers name 
book = ecmbBook(BOOK_TYPE.MANGA, 'en', 'bestmangapublisherinc_98a2cd52fea1168d', 900, 1200)

# title is mandatory
book.metadata.set_title('The Big Trip')

# add at least one image
book.content.add_image('../source_images/img_1.jpg')

# thats all, navigation and cover are not mandatory, but of course recommended
book.write('minimum_required_book.ecmb', warnings=True, demo_mode=True)



print('  "minimum_required_book.ecmb" was generated successfull!', flush=True)


print('\n', flush=True)