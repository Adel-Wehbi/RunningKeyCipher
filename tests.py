from unittest import TestCase, main
from io import StringIO
from runningkeycipher import perform, Action

class Tests(TestCase):
    '''Wikipedia Example on Running Key Cipher'''

    def setUp(self):
        self.outputStream = StringIO()
        self.keyStream = StringIO('errors can occur in several places. A label has...') 

    def test_encrypt(self):
        self.inputStream = StringIO('Flee At Once. We are discovered.')
        perform(Action.ENCRYPT, self.inputStream, self.keyStream, self.outputStream)
        self.assertEqual('JCVSRLQNPSYGUIMQAWXSMECTO', self.outputStream.getvalue())

    def test_decrypt(self):
        self.inputStream = StringIO('JCVSRLQNPSYGUIMQAWXSMECTO')
        perform(Action.DECRYPT, self.inputStream, self.keyStream, self.outputStream)
        self.assertEqual('FLEEATONCEWEAREDISCOVERED', self.outputStream.getvalue())
    
    def tearDown(self):
        self.inputStream.close()
        self.keyStream.close()
        self.outputStream.close()

if __name__ == '__main__':
    main()
