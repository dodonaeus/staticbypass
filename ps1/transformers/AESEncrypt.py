import random
import string
from utils.utils import bytes_to_ps1
import os
from Crypto.Cipher import AES
from Crypto.Util import Padding

class AESEncrypt:

    def __init__(self):
        self.name = ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(16))
        self.key = os.urandom(16)
        self.iv = os.urandom(16)

    def compilerOptions(self):
        return []

    def imports(self):
        return []

    def codeblock(self):
        return """
function {name} {{
    [CmdletBinding()]
    [OutputType([byte[]])]
    param(
        [Parameter(Mandatory, ValueFromPipeline)]
        [byte[]]$CipherBytes,

        [System.Security.Cryptography.CipherMode]$Mode =
            [System.Security.Cryptography.CipherMode]::CBC,

        [System.Security.Cryptography.PaddingMode]$Padding =
            [System.Security.Cryptography.PaddingMode]::PKCS7
    )
    begin {{
        $buffer = [System.Collections.Generic.List[byte]]::new()
    }}
    process {{
        $buffer.AddRange($CipherBytes)
    }}
    end {{
        $cipher = $buffer.ToArray()
        {key}
        {iv}

        $aes = [System.Security.Cryptography.Aes]::Create()
        $aes.Key     = $Key
        $aes.Mode    = $Mode
        $aes.Padding = $Padding
        $aes.IV = $IV

        $decryptor = $aes.CreateDecryptor()
        return $decryptor.TransformFinalBlock($cipher, 0, $cipher.Length)
    }}
}}
""".format(name = self.name, key=bytes_to_ps1(self.key, 'Key'), iv=bytes_to_ps1(self.iv, 'IV'))

    def encode(self, plaintext):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        self.plaintextSize = len(plaintext)
        encrypted = cipher.encrypt(Padding.pad(plaintext, 16, style='pkcs7'))
        self.ciphertextSize = len(encrypted)
        return encrypted

    def transformer(self, shellcodestring):
        return shellcodestring.format(shellcode=f'{{shellcode}} | {self.name}')