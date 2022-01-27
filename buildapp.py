import osnap.installer
import opinsuomea

APPLICATION_NAME = 'OpinSuomea'
AUTHOR = 'MarcPerkins'

def make_installer(verbose):
    osnap.installer.make_installer(AUTHOR, APPLICATION_NAME, 'this is my test example', 'www.mydomain.com',
                                   [APPLICATION_NAME], test_example.__version__, verbose=verbose)

if __name__ == '__main__':
    make_installer(True)